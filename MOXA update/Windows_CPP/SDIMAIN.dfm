object SDIAppForm: TSDIAppForm
  Left = 197
  Top = 111
  Caption = 'SDI Application'
  ClientHeight = 306
  ClientWidth = 404
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -13
  Font.Name = 'System'
  Font.Style = []
  OldCreateOrder = False
  Visible = True
  OnCreate = FormCreate
  PixelsPerInch = 96
  TextHeight = 16
  object Label1: TLabel
    Left = 136
    Top = 74
    Width = 48
    Height = 16
    Caption = 'Label1:'
  end
  object Button3: TButton
    Left = 136
    Top = 104
    Width = 145
    Height = 33
    Caption = 'Update'
    TabOrder = 0
    OnClick = Button3Click
  end
  object Edit1: TEdit
    Left = 136
    Top = 136
    Width = 121
    Height = 24
    TabOrder = 1
    Text = 'Edit1'
  end
end
