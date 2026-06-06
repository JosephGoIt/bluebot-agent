#define MyAppName "Bluebot Agent"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "JosephGoIt"
#define MyAppURL "https://github.com/JosephGoIt/bluebot-agent"
#define MyAppExeName "Bluebot.exe"
#define MyAppId "{{A3F2D1B9-8C4E-4F7A-9E2B-1D3C5A6B8F0E}"

[Setup]
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=
OutputDir=Output
OutputBaseFilename=Bluebot-Setup
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\Bluebot\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
procedure CreateConfigTemplate();
var
  ConfigPath: string;
  Lines: TStringList;
begin
  ConfigPath := ExpandConstant('{app}\config.txt');
  if not FileExists(ConfigPath) then
  begin
    Lines := TStringList.Create;
    try
      Lines.Add('# Bluebot Configuration File');
      Lines.Add('# Replace the placeholder below with your actual Gemini API key');
      Lines.Add('# Get your key at: https://aistudio.google.com/apikey');
      Lines.Add('');
      Lines.Add('GEMINI_API_KEY=your_gemini_api_key_here');
      Lines.Add('CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe');
      Lines.SaveToFile(ConfigPath);
    finally
      Lines.Free;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
    CreateConfigTemplate();
end;
