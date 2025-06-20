#!/usr/bin/env python3
"""
LepmonOS Main Launcher

A pythonic launcher for the LepmonOS application that replaces the bash script.
This script runs the main application modules in sequence with proper error handling.
"""

import os
import sys
import time
import subprocess
from pathlib import Path
import importlib.util

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

def enable_i2c():
    """Enable I2C interface using raspi-config if available."""
    try:
        print("Enabling I2C interface...")
        result = subprocess.run(
            ["sudo", "raspi-config", "nonint", "do_i2c", "0"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("I2C interface enabled successfully")
        else:
            print(f"Warning: Could not enable I2C interface: {result.stderr}")
    except FileNotFoundError:
        print("Warning: raspi-config not found - I2C setup skipped")
    except subprocess.TimeoutExpired:
        print("Warning: I2C configuration timed out")
    except Exception as e:
        print(f"Warning: I2C configuration failed: {e}")

def run_script(script_name, description):
    """
    Run a Python script by importing and executing it.
    
    Args:
        script_name (str): Name of the script file (without .py extension)
        description (str): Human-readable description of the script
    
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"\n{'='*50}")
    print(f"Running {description}")
    print(f"Script: {script_name}.py")
    print(f"{'='*50}")
    
    try:
        # Import and run the script
        script_path = current_dir / f"{script_name}.py"
        
        if not script_path.exists():
            print(f"Error: Script {script_path} not found!")
            return False
            
        # Load the module
        spec = importlib.util.spec_from_file_location(script_name, script_path)
        module = importlib.util.module_from_spec(spec)
        
        # Execute the module
        spec.loader.exec_module(module)
        
        print(f"✓ {description} completed successfully")
        return True
        
    except KeyboardInterrupt:
        print(f"\n⚠ {description} interrupted by user")
        raise
    except Exception as e:
        print(f"✗ Error in {description}: {e}")
        print(f"Script {script_name}.py failed - continuing with next script...")
        return False

def main():
    """Main launcher function."""
    print("="*60)
    print("🚀 Starting LepmonOS Application")
    print("="*60)
    print(f"Working directory: {current_dir}")
    print(f"Python version: {sys.version}")
    print()
    
    # Change to the script directory
    os.chdir(current_dir)
    
    # Enable I2C interface (if on Raspberry Pi)
    enable_i2c()
    
    # Define the scripts to run in sequence
    scripts = [
        ("00_start_up", "System Startup & Initialization"),
        ("02_trap_hmi", "Human Machine Interface"),
        ("03_capturing", "Image Capturing Service"),
        ("04_end", "Shutdown Sequence"),
    ]
    
    success_count = 0
    
    try:
        for script_name, description in scripts:
            try:
                if run_script(script_name, description):
                    success_count += 1
                time.sleep(1)  # Brief pause between scripts
            except KeyboardInterrupt:
                print("\n⚠ Application interrupted by user")
                break
                
    except Exception as e:
        print(f"✗ Critical error in launcher: {e}")
    
    finally:
        print(f"\n{'='*60}")
        print(f"🏁 LepmonOS Application Finished")
        print(f"Successfully completed: {success_count}/{len(scripts)} scripts")
        print(f"{'='*60}")
        
        if success_count < len(scripts):
            print("⚠ Some scripts failed - check logs for details")
            sys.exit(1)
        else:
            print("✓ All scripts completed successfully")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Application terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        sys.exit(1)