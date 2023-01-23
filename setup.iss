; Setup script for release versions of Spine Toolbox

; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Spine Toolbox"
#define MyAppVersion "0.6.0-final.0"
#define MyAppPublisher "Spine Project Consortium"
#define MyAppURL "https://github.com/spine-tools"
#define MyAppExeName "spinetoolbox.exe"
#define MyAppRegKey "Software\SpineProject"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
SignTool=signtool
AppId={{6E794A8A-E508-47C4-9319-1113852224D3}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={commonpf}\Spine Toolbox
DefaultGroupName=Spine Toolbox
AllowNoIcons=yes
LicenseFile=COPYING.LESSER
OutputBaseFilename=spine-toolbox-{#MyAppVersion}-x64
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
UsePreviousPrivileges=no
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=dist
ArchitecturesInstallIn64BitMode=x64 ia64
ArchitecturesAllowed=x64 ia64 arm64
UsePreviousAppDir=yes
SignedUninstaller=yes
AlwaysShowDirOnReadyPage=yes
DisableDirPage=no
WizardStyle=modern

[Code]
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    if RegKeyExists(HKEY_CURRENT_USER, '{#MyAppRegKey}') then
      if MsgBox('Do you want to delete Spine Toolbox settings from registry?',
        mbConfirmation, MB_YESNO) = IDYES
      then
        RegDeleteKeyIncludingSubkeys(HKEY_CURRENT_USER, '{#MyAppRegKey}');
  end;
end;

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "build\exe.win-amd64-3.7\spinetoolbox.exe"; DestDir: "{app}"; Flags: ignoreversion sign
Source: "build\exe.win-amd64-3.7\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Dirs]
Name: "{app}\projects"; Permissions: users-full
Name: "{app}\work"; Permissions: users-full

[Icons]
Name: "{group}\{#MyAppName} {#MyAppVersion}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName} {#MyAppVersion}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[InstallDelete]
Type: filesandordirs; Name: "{app}\lib\numpy"
Type: filesandordirs; Name: "{app}\lib\spinedb_api\alembic"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

