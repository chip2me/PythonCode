// ConsoleApplication1.cpp : Defines the entry point for the console application.
//


/**
Test program for network adapter info
*/

#include "stdafx.h"
#include <windows.h>
#include <iphlpapi.h>

#pragma comment(lib, "iphlpapi.lib")

int main(int argc, char** argv)
{
  PIP_ADAPTER_INFO pAdapterInfo;
  pAdapterInfo = (IP_ADAPTER_INFO *)malloc(sizeof(IP_ADAPTER_INFO));
  ULONG buflen = sizeof(IP_ADAPTER_INFO);

  if(GetAdaptersInfo(pAdapterInfo, &buflen) == ERROR_BUFFER_OVERFLOW)
  {
    free(pAdapterInfo);
    pAdapterInfo = (IP_ADAPTER_INFO *)malloc(buflen);
  }

  if(GetAdaptersInfo(pAdapterInfo, &buflen) == NO_ERROR)
  {
    PIP_ADAPTER_INFO pAdapter = pAdapterInfo;
    while (pAdapter)
    {
      //printf("\tAdapter Name: \t%s\n", pAdapter->AdapterName);
      //printf("\tAdapter Desc: \t%s\n", pAdapter->Description);
      //printf("\tAdapter Addr: \t%ld\n", pAdapter->Address);
          printf("%s,", pAdapter->IpAddressList.IpAddress.String);
      //printf("\tIP Mask: \t%s\n", pAdapter->IpAddressList.IpMask.String);
      //printf("\tGateway: \t%s\n", pAdapter->GatewayList.IpAddress.String);
	    printf("%i\n", pAdapter->DhcpEnabled);
        pAdapter = pAdapter->Next;
    }
  }
  else
  {
    printf("Call to GetAdaptersInfo failed.\n");
  }
  //system("pause");  //getch();
}


