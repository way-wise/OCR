import os
import sys
import logging
import subprocess
from pathlib import Path

def check_ghostscript():
    """Check if Ghostscript is installed and accessible"""
    try:
        # Try to find gswin64c in common installation paths
        common_paths = [
            r"C:\Program Files\gs\gs10.02.1\bin",  # Latest version path
            r"C:\Program Files\gs\gs10.02.0\bin",
            r"C:\Program Files\gs\gs10.01.2\bin",
            r"C:\Program Files\gs\gs10.01.1\bin",
            r"C:\Program Files\gs\gs10.01.0\bin",
            r"C:\Program Files\gs\gs10.00.0\bin",
            r"C:\Program Files\gs\gs9.56.1\bin",
            r"C:\Program Files\gs\gs9.56.0\bin",
        ]
        
        # Check if gswin64c is in PATH
        gs_path = None
        try:
            subprocess.run(['gswin64c', '--version'], capture_output=True)
            return True
        except FileNotFoundError:
            # Not in PATH, check common locations
            for path in common_paths:
                gs_exe = Path(path) / 'gswin64c.exe'
                if gs_exe.exists():
                    gs_path = str(gs_exe.parent)
                    break
        
        if gs_path:
            # Add to PATH
            os.environ['PATH'] = gs_path + os.pathsep + os.environ['PATH']
            return True
        
        # If not found, provide installation instructions
        print("\nGhostscript is not installed. Please follow these steps:")
        print("1. Download Ghostscript from: https://ghostscript.com/releases/gsdnld.html")
        print("2. Install for your system (choose 64-bit Windows version)")
        print("3. The installer should automatically add Ghostscript to your PATH")
        print("4. If not, add the bin directory (e.g., C:\\Program Files\\gs\\gs10.02.1\\bin) to your PATH manually")
        print("\nAfter installation, restart the program.")
        return False
        
    except Exception as e:
        logging.error(f"Error checking Ghostscript: {str(e)}")
        return False

def check_system_dependencies():
    """Check all required system dependencies"""
    checks = {
        "Ghostscript": check_ghostscript(),
    }
    
    # Log results
    logging.info("System dependency check results:")
    for dep, status in checks.items():
        logging.info(f"{dep}: {'[OK]' if status else '[MISSING]'}")
    
    # Return True only if all checks pass
    return all(checks.values()) 