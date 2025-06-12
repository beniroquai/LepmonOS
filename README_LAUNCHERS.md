# LepmonOS Python Launchers

This directory now includes two Python-based launchers that replace the bash script `LepmonOS_start.sh` with more pythonic approaches.

## Launchers Available

### 1. `main.py` - Advanced Launcher
The primary launcher that imports and executes modules directly for better integration.

**Usage:**
```bash
python3 main.py
```

**Features:**
- Direct module imports for better error handling
- Comprehensive logging and status reporting
- Automatic I2C configuration
- Progress tracking with emoji indicators
- Graceful error handling and recovery

### 2. `lepmon_launcher.py` - Simple Launcher
A simpler launcher that uses subprocess to run scripts independently.

**Usage:**
```bash
python3 lepmon_launcher.py
```

**Features:**
- Script isolation using subprocess
- Cleaner separation between modules
- Simple progress reporting
- Robust error handling
- Good for debugging individual scripts

## Script Execution Order

Both launchers execute the following scripts in sequence:

1. **`00_start_up.py`** - System Startup & Initialization
2. **`02_trap_hmi.py`** - Human Machine Interface
3. **`03_capturing.py`** - Image Capturing Service
4. **`04_end.py`** - Shutdown Sequence

## Advantages over Bash Script

- **Portable**: Works from any directory, not just `/home/pi/LepmonOS`
- **Better Error Handling**: Python's exception handling provides clearer error messages
- **Progress Tracking**: Visual feedback on script execution
- **Modular**: Easy to modify, extend, or debug individual components
- **Cross-platform**: Can run on different operating systems
- **Maintainable**: Python code is easier to read and modify than bash

## Migration from Bash

To migrate from the old bash script:

1. **Replace bash execution** with Python:
   ```bash
   # Old way
   ./LepmonOS_start.sh
   
   # New way
   python3 main.py
   # or
   python3 lepmon_launcher.py
   ```

2. **Environment Variables**: The Python launchers automatically handle directory changes and don't require the complex environment setup of the bash script.

3. **I2C Configuration**: Automatic I2C setup is included in both launchers.

## System Requirements

- Python 3.6 or higher
- All dependencies from `requirements.txt`
- `sudo` access for I2C configuration (optional)

## Troubleshooting

### Script Not Found Error
Make sure you're running from the LepmonOS directory:
```bash
cd /path/to/LepmonOS
python3 main.py
```

### Permission Errors
Make sure the launcher is executable:
```bash
chmod +x main.py
chmod +x lepmon_launcher.py
```

### I2C Warnings
I2C configuration requires `raspi-config` and `sudo` access. Warnings are normal on non-Raspberry Pi systems.

## Choosing Between Launchers

- **Use `main.py`** for production deployment - better integration and error handling
- **Use `lepmon_launcher.py`** for development and debugging - better script isolation