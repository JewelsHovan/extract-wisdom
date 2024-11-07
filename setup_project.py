import os
import subprocess
from pathlib import Path
from config import PAPER_DIR, OUTPUT_DIR

def create_directories():
    """Create necessary project directories if they don't exist."""
    directories = [PAPER_DIR, OUTPUT_DIR]
    
    for directory in directories:
        dir_path = Path(directory)
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Directory ready: {directory}")
        except Exception as e:
            print(f"✗ Error creating directory {directory}: {e}")
            raise

def install_dependencies():
    """Install project dependencies using pip."""
    try:
        subprocess.check_call(["pip", "install", "-e", "."])
        print("✓ Successfully installed project dependencies")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        raise

def setup_project():
    """Run all setup steps."""
    print("\n=== Setting up Academic Paper Analyzer ===")
    create_directories()
    install_dependencies()
    print("\n=== Setup completed successfully ===")

if __name__ == "__main__":
    try:
        setup_project()
    except Exception as e:
        print(f"\n✗ Setup failed: {e}")
        exit(1)
