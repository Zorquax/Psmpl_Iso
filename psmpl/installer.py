import os
import sys
import subprocess
import urllib.request
import platform
import time

SETUP_FLAG_PATH = os.path.join(os.getcwd(), ".setup_done")

def is_windows():
    return platform.system() == "Windows"

def is_mac():
    return platform.system() == "Darwin"

def get_real_python_exec():
    if is_mac():
        return "/usr/bin/python3" if os.path.exists("/usr/bin/python3") else "python3"
    elif is_windows():
        return "python"  # Default should work after install
    return sys.executable  # fallback

def check_python():
    try:
        version = sys.version_info
        if version.major == 3 and version.minor >= 7:
            print("Python 3.7+ is already installed.")
            return True
    except:
        return False
    return False

def install_python_windows():
    try:
        print("Downloading Python installer for Windows...")
        python_url = "https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe"
        installer_path = os.path.join(os.getcwd(), "python_installer.exe")

        if os.path.exists(installer_path):
            os.remove(installer_path)

        urllib.request.urlretrieve(python_url, installer_path)

        if not os.path.exists(installer_path):
            raise FileNotFoundError("Installer download failed!")

        print("Running the installer (requires admin)...")
        subprocess.run([
            installer_path,
            "/quiet",
            "InstallAllUsers=1",
            "PrependPath=1",
            "Include_pip=1"
        ], check=True)

        os.remove(installer_path)
        print("Python installed successfully.")
        return True
    except Exception as e:
        print(f"Error installing Python: {e}")
        return False

def check_pip():
    try:
        python_exec = get_real_python_exec()
        subprocess.run([python_exec, "-m", "pip", "--version"], check=True)
        return True
    except Exception as e:
        print(f"check_pip error: {e}")
        return False

def install_pip():
    try:
        python_exec = get_real_python_exec()
        subprocess.run([python_exec, "-m", "ensurepip", "--default-pip"], check=True)
        return True
    except Exception as e:
        print(f"Error installing pip: {e}")
        return False

def install_requirements():
    try:
        print("Installing required packages...")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        requirements_path = os.path.join(script_dir, "requirements.txt")

        if not os.path.exists(requirements_path):
            print("requirements.txt not found. Creating a default one...")
            with open(requirements_path, "w") as f:
                f.write("requests\n")  # Change this to your real requirements

        python_exec = get_real_python_exec()
        subprocess.run([python_exec, "-m", "pip", "install", "-r", requirements_path], check=True)
        print("All requirements installed successfully.")
        return True
    except Exception as e:
        print(f"Error installing requirements: {e}")
        return False

def run_main_app():
    try:
        print(f"Current working directory: {os.getcwd()}")
        
        if getattr(sys, 'frozen', False):
            if hasattr(sys, '_MEIPASS'):
                base_dir = sys._MEIPASS
                print(f"Using PyInstaller temp directory: {base_dir}")
            else:
                base_dir = os.path.dirname(sys.executable)
                print(f"Using executable directory: {base_dir}")
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            print(f"Using script directory: {base_dir}")

        main_path = os.path.join(base_dir, 'src', 'main.py')
        print(f"Looking for main.py at: {main_path}")

        if not os.path.exists(main_path):
            print(f"Main application not found at: {main_path}")
            return False

        # Instead of running as a subprocess, import and run directly
        import importlib.util
        spec = importlib.util.spec_from_file_location("main", main_path)
        main_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_module)
        
        # Call the main function
        if hasattr(main_module, 'main'):
            main_module.main()
        return True
    except Exception as e:
        print(f"Error launching application: {e}")
        return False
    
def setup_already_done():
    return os.path.exists(SETUP_FLAG_PATH)

def mark_setup_done():
    with open(SETUP_FLAG_PATH, "w") as f:
        f.write("done")

def setup():
    print("Starting PSMPL ISO Tool setup...\n")

    if not check_python():
        if is_windows():
            print("Python 3.7+ not found. Installing...")
            if not install_python_windows():
                print("Failed to install Python. Please install Python 3.7+ manually.")
                return False
        elif is_mac():
            print("Python 3.7+ not found. Please install it manually from https://www.python.org or with Homebrew.")
            return False

    if not check_pip():
        print("pip not found. Installing...")
        if not install_pip():
            print("Failed to install pip.")
            return False

    if not install_requirements():
        print("Failed to install requirements.")
        return False

    return True

if __name__ == "__main__":
    print(f"\n[DEBUG] Running: {__file__}")
    print(f"[DEBUG] sys.executable: {sys.executable}")
    print(f"[DEBUG] args: {sys.argv}\n")

    if not setup_already_done():
        if setup():
            print("Setup completed successfully!")
            mark_setup_done()
            time.sleep(2)
            run_main_app()
    else:
        print("Setup already done. Launching app.")
        run_main_app()

    input("Press Enter to exit...")
