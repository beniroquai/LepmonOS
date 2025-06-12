#!/usr/bin/env python3
"""
LepmonOS Simple Launcher

A simple Python launcher that runs the LepmonOS scripts using subprocess.
This provides better isolation between scripts and cleaner error handling.
"""

import os
import sys
import time
import subprocess
from pathlib import Path

# Get the directory where this script is located
current_dir = Path(__file__).parent.absolute()

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
            print("✓ I2C interface enabled successfully")
        else:
            print(f"⚠ Warning: Could not enable I2C interface: {result.stderr}")
    except FileNotFoundError:
        print("⚠ Warning: raspi-config not found - I2C setup skipped")
    except subprocess.TimeoutExpired:
        print("⚠ Warning: I2C configuration timed out")
    except Exception as e:
        print(f"⚠ Warning: I2C configuration failed: {e}")

def run_python_script(script_name, description):
    """
    Run a Python script using subprocess.
    
    Args:
        script_name (str): Name of the script file (with .py extension)
        description (str): Human-readable description of the script
    
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"\n{'='*50}")
    print(f"🔄 Running {description}")
    print(f"Script: {script_name}")
    print(f"{'='*50}")
    
    script_path = current_dir / script_name
    
    if not script_path.exists():
        print(f"✗ Error: Script {script_path} not found!")
        return False
    
    try:
        # Run the script
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=current_dir,
            check=False  # Don't raise exception on non-zero exit
        )
        
        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            return True
        else:
            print(f"✗ {description} exited with code {result.returncode}")
            return False
            
    except KeyboardInterrupt:
        print(f"\n⚠ {description} interrupted by user")
        raise
    except Exception as e:
        print(f"✗ Error running {description}: {e}")
        return False

def main():
    """Main launcher function."""
    print("="*60)
    print("🚀 LepmonOS Simple Launcher")
    print("="*60)
    print(f"Working directory: {current_dir}")
    print(f"Python executable: {sys.executable}")
    print()
    
    # Change to the script directory
    os.chdir(current_dir)
    
    # Enable I2C interface (if on Raspberry Pi)
    enable_i2c()
    
    # Define the scripts to run in sequence
    scripts = [
        ("00_start_up.py", "System Startup & Initialization"),
        ("02_trap_hmi.py", "Human Machine Interface"),
        ("03_capturing.py", "Image Capturing Service"),
        ("04_end.py", "Shutdown Sequence"),
    ]
    
    success_count = 0
    total_scripts = len(scripts)
    
    try:
        for i, (script_name, description) in enumerate(scripts, 1):
            print(f"\n📋 Progress: {i}/{total_scripts}")
            try:
                if run_python_script(script_name, description):
                    success_count += 1
                time.sleep(0.5)  # Brief pause between scripts
            except KeyboardInterrupt:
                print("\n⚠ Application interrupted by user")
                break
                
    except Exception as e:
        print(f"✗ Critical error in launcher: {e}")
    
    finally:
        print(f"\n{'='*60}")
        print(f"🏁 LepmonOS Application Summary")
        print(f"{'='*60}")
        print(f"Successfully completed: {success_count}/{total_scripts} scripts")
        
        if success_count == total_scripts:
            print("✅ All scripts completed successfully!")
        elif success_count > 0:
            print("⚠ Some scripts completed with errors - check output above")
        else:
            print("❌ No scripts completed successfully")
        
        print(f"{'='*60}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 LepmonOS launcher terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Fatal launcher error: {e}")
        sys.exit(1)