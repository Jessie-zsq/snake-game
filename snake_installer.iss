[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName=Snake
AppVersion=1.0.0
AppPublisher=Snake Game
DefaultDirName={autopf}\Snake
DefaultGroupName=Snake
OutputDir=installer_output
OutputBaseFilename=Snake-Installer
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce
Name: "startmenuicon"; Description: "Create Start Menu shortcut"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce

[Files]
Source: "dist\Snake\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Snake"; Filename: "{app}\Snake.exe"
Name: "{group}\Uninstall Snake"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Snake"; Filename: "{app}\Snake.exe"; Tasks: desktopicon
Name: "{userprograms}\Snake"; Filename: "{app}\Snake.exe"; Tasks: startmenuicon

[Run]
Filename: "{app}\Snake.exe"; Description: "Launch Snake now"; Flags: nowait postinstall skipifsilent
