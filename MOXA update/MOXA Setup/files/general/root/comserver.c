/*******************************************************************************
File name:	comserver.c
    	          -- UDP Server Client + Data Packing Example For firmware AP
      -- if receive data from[p] serial port, send data to LAN with destination IP.
      -- if receive data from[p] LAN, write data to serial port.

Description:
	This program create UDP socket and 
	exchange data between serial port and Ethernet.

	Use SOCKET Library,the header file sys/socket.h must be included.
UDPPORT
	1	Open serial port.
	2	Configure serial port to 9600bps, N81, no flow control.
	3	Read remote IP address and UDP port settings.
	4	Create UDP socket and receive data on Port 5001. 
	5	Exchange data between serial port and Ethernet. 


History:    
    	Version		Author		Date		Comment
grung        1.0		Victor Yu.	01-16-2004      Wrote it.
	0.0		Kaj Verner Madsen	29-10-2005	Under udarbejdelse	

*******************************************************************************/
#include        <stdio.h>
#include        <stdlib.h>
#include	<fcntl.h>
#include	<errno.h>
#include        <sys/types.h>
#include        <sys/socket.h>
#include        <sys/fcntl.h>
#include        <termios.h>
#include        <netinet/in.h>
#include	<time.h>
#include	<moxadevice.h>


static int	fd_keypad;
void		KEYPAD_has_press(int *);
void		KEYPAD_get_key(int *);
void		Buzzer_sound(int);

// flag > 1 ==> means how many keys pressed, flag = 0 ==> no key pressed
void KEYPAD_has_press(int * flag) {ioctl(fd_keypad, IOCTL_KEYPAD_HAS_PRESS,flag);}

// key = 0~4 ==> F1~F5 function key, key = -1 ==> no key pressed
void KEYPAD_get_key(int * key) {ioctl(fd_keypad, IOCTL_KEYPAD_GET_KEY,key);}

#define SPORT	"/dev/ttyM0"
#define ver	"UC7420 comsever v. 1.0\r"
#define UDPPORT	5000
#define DEST_IP	"192.168.4.140"
#define PN	8
#define str 	1
#define slt 	8
const char prtnm[PN][11] = {"/dev/ttyM0","/dev/ttyM1","/dev/ttyM2","/dev/ttyM3",
               "/dev/ttyM4","/dev/ttyM5","/dev/ttyM6","/dev/ttyM7"};
//const char prtnm[PN][10] = {"/dev/ttyM0"};

#define	DEL_CH		'b'
#define	BUF_LEN		10

#define	BUFFER_LEN	1024

char 	sbuf[BUFFER_LEN],databuf[BUFFER_LEN],rbuf[BUFFER_LEN],bbuf[BUFFER_LEN];

int main()
{
	int	flag,key;
	time_t  keytm[5];
	time_t  tm, sttm;
	int 	a,p;
	int	sfd[PN+1], afd[PN+1];
	struct sockaddr_in 	from[PN+1], to[PN+1], m;
	int 			size,i,ret,len,data_i=0;
	struct termios		tty;

	for(a=0;a<5;a++) {
		keytm[a]=0;
	}
	

	printf("start\n");
	fd_keypad = open("/dev/keypad",O_RDWR);
	if ( fd_keypad < 0 ) {
		printf("Open keypad device node fail [%d]\n", errno);
		return 0 ;
	}

	do {
		KEYPAD_has_press(&flag);
		if (flag) {
			KEYPAD_get_key(&key);
		}
	}
	while (flag);
	for(a=0;a<5;a++) {
		keytm[a]=0;
	}
	

	/* set serial port baud rate */
	tty.c_cflag = CREAD | CLOCAL | B9600 | CS8;
	tty.c_oflag = 0;
	tty.c_lflag = 0;
	tty.c_iflag = 0;
	tty.c_cc[VMIN] = 0;
	tty.c_cc[VTIME] = 0;
	

	for (p=str;p<slt+1;p++) {
	
		/* open serial port */
		printf("open asyc port [%s] nr [%d]\n", prtnm[p-1], p);
		if ( (afd[p]=open(prtnm[p-1], O_RDWR|O_NDELAY)) < 0 ) {
			printf("open asyc port [%s] fail [%d]\n", prtnm[p-1], errno);
			return 0;
		}
		tcsetattr(afd[p], TCSANOW, &tty);
	}
        for (p=str-1;p<slt+1;p++) {
		from[p].sin_addr.s_addr = htonl(INADDR_ANY);
		from[p].sin_family = AF_INET;
		from[p].sin_port = htons((unsigned short)(UDPPORT+p));
 
		to[p].sin_addr.s_addr = inet_addr(DEST_IP);
		to[p].sin_family = AF_INET;
		to[p].sin_port = htons((unsigned short)(UDPPORT+p));
			
		/* create socket */
		if ( (sfd[p]=socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0 ){
			printf("open socket fail [%d]\n", errno);
			close(afd[p]);
			goto exit_program;
		}

		/* associates a local address with a socket */
		if ( bind(sfd[p], (struct sockaddr *)&from[p], sizeof(from[p])) < 0 ) {
			printf("socket bind fail [%d]\n", errno);
	    		goto exit_program;
		}

		/* set socket to nonblock */
		ret = fcntl(sfd[p], F_GETFL);
		ret |= O_NONBLOCK;
		if ( fcntl(sfd[p], F_SETFL, ret) < 0 ) {
			printf("set socket to nonblock fail [%d] !\n", errno);
			goto exit_program;
		}
		from[p].sin_addr.s_addr = inet_addr(DEST_IP);
	}
	size = sizeof(m);
	while(1) {
	KEYPAD_has_press(&flag);
	if ( flag ) {
	        KEYPAD_get_key(&key);
		tm=time(NULL);
		if (key>-1) keytm[key]=tm; 
		for(a=0;a<5;a++) {
			if (tm>keytm[a]+5) {
				keytm[a]=0;
			}
		}
		if ((keytm[0]>0) && (keytm[1]>0) && (keytm[2]==0) && (keytm[3]>0) && (keytm[4]>0)) {
			goto exit_program;
			}
		}
	/* receive data form LAN port 5000*/
	ret = recvfrom(sfd[0], rbuf, BUFFER_LEN, 0, (struct sockaddr *)&m,&size);
	if ((ret<0) && (errno != EAGAIN)) {
		if ( errno == ENOTCONN )
			goto exit_program;
		printf("socket recvfrom[0] fail [%d]\n", errno);
		break;	KEYPAD_has_press(&flag);
	if ( flag ) {
	        KEYPAD_get_key(&key);
		tm=time(NULL);
		if (key>-1) keytm[key]=tm; 
		for(a=0;a<5;a++) {
			if (tm>keytm[a]+5) {
				keytm[a]=0;
			}
		}
		if ((keytm[0]>0) && (keytm[1]>0) && (keytm[2]==0) && (keytm[3]>0) && (keytm[4]>0)) {
			goto exit_program;
			}
		}

	}else if (ret>0) { 
		from[0]=m;
	        printf("read from lan %d bytes on port %d fra ip %d\n", ret,UDPPORT,from[0].sin_addr.s_addr);
		/* write back version to lan */
		to[0].sin_addr.s_addr = from[0].sin_addr.s_addr;
		if (to[0].sin_addr.s_addr==0) {
			to[0].sin_addr.s_addr = inet_addr(DEST_IP);
			printf("socket read ip %d  write ip %d \n",from[0].sin_addr.s_addr ,to[0].sin_addr.s_addr);
			}
		if(ret!= 0){
			/* send data to LAN */
			printf("socket write  %d bytes on port %d ip %d\n", sizeof(ver),UDPPORT,to[0].sin_addr.s_addr);
			if((ret = sendto(sfd[0],ver,sizeof(ver),0, (struct sockaddr *)&(to[0]),size)) < 0 ){
					printf("socket sendto fail [%d]  ip port %d\n", errno,m.sin_port);
					goto exit_program;
				}
			}
	}
	for (p=str;p<slt+1;p++) {
		/* read data from[p] serial port */
		if ( (len=read(afd[p],sbuf,BUFFER_LEN)) < 0 ) {
			printf("async port read data fail [%d]  port %d\n", errno,p);
			goto exit_program;
		}else if(len >0){
			printf("async port read  %d bytes on port %d\n", len,p);
//			continue;
		} 	
		
		for(i=0; i<len; i++) 
			databuf[data_i++] = sbuf[i];
	            
		if (len>0) {
			to[p].sin_addr.s_addr = from[p].sin_addr.s_addr;
			if (to[p].sin_addr.s_addr==0) {
				to[p].sin_addr.s_addr = inet_addr(DEST_IP);
				printf("socket read ip %d  write ip %d \n",from[p].sin_addr.s_addr ,to[p].sin_addr.s_addr);
			}
			if(data_i != 0){
				/* send data to LAN */
			        printf("socket write  %d bytes on port %d ip %d\n", data_i,p,to[p].sin_addr.s_addr);
//				m=to[p];
				if((ret = sendto(sfd[p],databuf,data_i,0, (struct sockaddr *)&(to[p]),size)) < 0 ){
					printf("socket sendto fail [%d]  ip port %d\n", errno,m.sin_port);
					goto exit_program;
				}else{
					if(ret == data_i){
						data_i = data_i - ret;
					}else{ 
						data_i = 0;	
						break;
					}
				}
			}else 	break; 
		}
		/* receive data form LAN */
		m=from[p];
		m.sin_addr.s_addr = htonl(INADDR_ANY);
		ret = recvfrom(sfd[p], rbuf, BUFFER_LEN, 0, (struct sockaddr *)&m,&size);
		if ((ret<0) && (errno != EAGAIN)) {
			if ( errno == ENOTCONN )
				goto exit_program;
			printf("socket recvfrom[p] fail [%d]\n", errno);
			break;
		}else if (ret>0) { 
			from[p]=m;
		        printf("async port send  %d bytes on port %d fra ip %d\n", ret,p,from[p].sin_addr.s_addr);
			/* write data to serial port */
			if ( (len=write(afd[p],rbuf,ret)) < 0 ) {
				printf("async port write data fail [%d]", errno);
				goto exit_program;
			}
			ret=0;
		}
        }		    
	}
exit_program:
	close(fd_keypad);
	for (p=str;p<slt+1;p++) {
		close(sfd[p]);
		close(afd[p]);
	}
	printf("exit\n");
	return 0;
}
