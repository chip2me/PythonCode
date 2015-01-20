//---------------------------------------------------------------------
#include <vcl.h>
#pragma hdrstop

#include "SDIMain.h"
#include "About.h"
//---------------------------------------------------------------------
#pragma resource "*.dfm"
TSDIAppForm *SDIAppForm;


//Globals
int g_iCount = 1;

//---------------------------------------------------------------------
__fastcall TSDIAppForm::TSDIAppForm(TComponent *AOwner) : TForm(AOwner)
{
}
//---------------------------------------------------------------------

void __fastcall TSDIAppForm::FileNew1Execute(TObject *Sender)
{
  //Do nothing
}
//---------------------------------------------------------------------------









void __fastcall TSDIAppForm::UpDown1Click(TObject *Sender, TUDBtnType Button)
{
  if (Button == 0)
    g_iCount++;
  if (Button == 1)
    g_iCount--;

  if (g_iCount <1)
  {
    g_iCount = 1;
  }
  if (g_iCount > 20)
  {
    g_iCount = 20;
  }

  UnicodeString ucTmp = "Shimoda ";
  this->Edit3->Text = ucTmp + g_iCount;
}

void __fastcall TSDIAppForm::FormCreate(TObject *Sender)
{
  UnicodeString ucTmp = "Shimoda ";
  this->Edit3->Text = ucTmp + g_iCount;
}
//---------------------------------------------------------------------------



//MOXA Button
void __fastcall TSDIAppForm::Button3Click(TObject *Sender)
{
static int counter;
switch (counter++)
{
case 0:
    fVal = 355.0/113.0;
    break;
case 1:
    fVal = 455.0/113.0;
    break;
case 2:
    fVal = 555.0/113.0;
    break;
default
    fVal = 999.0;
    counter=0;
}
Edit1->Text=fVal;
}
//---------------------------------------------------------------------------

