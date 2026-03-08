# Build Scripts

This folder contains all build-related files and outputs.

## Scripts

- **build.bat** - Build single executable file
- **build_portable.bat** - Build portable installer package
- **clean.bat** - Clean all build artifacts

## Output Folders

All build outputs are created in this folder:

- `build/` - Temporary build files
- `dist/` - Built executables
- `ApexSender_Installer/` - Portable installer package
- `*.spec` - PyInstaller spec files

## Usage

### Build Portable Version (Recommended)
```bash
cd build_scripts
build_portable.bat
```

### Build Single Executable
```bash
cd build_scripts
build.bat
```

### Clean Build Files
```bash
cd build_scripts
clean.bat
```

## Notes

- All build artifacts stay in this folder
- Root directory remains clean
- Easy to gitignore entire folder
