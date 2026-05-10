import os
import subprocess
import sys
import json

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print("\033[94m" + "="*50)
    print("   🚀 ADAPTIX AI SETUP")
    print("   Learning your habits, one snapshot at a time.")
    print("="*50 + "\033[0m")

def run_command(command):
    print(f"\033[90mRunning: {command}...\033[0m")
    try:
        subprocess.check_call(command, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def validate_key_via_venv(provider, key):
    """Runs a tiny script inside the venv to validate the key."""
    if not key: return True
    
    if sys.platform == "win32":
        python_exe = os.path.join("venv", "Scripts", "python.exe")
    else:
        python_exe = os.path.join("venv", "bin", "python")
    script = f"""
import sys
try:
    if "{provider}" == "gemini":
        import google.generativeai as genai
        genai.configure(api_key="{key}")
        model = genai.GenerativeModel('gemini-2.0-flash')
        model.generate_content("test", generation_config={{"max_output_tokens": 1}})
    else:
        from openai import OpenAI
        client = OpenAI(api_key="{key}")
        client.models.list()
    sys.exit(0)
except Exception as e:
    print(e)
    sys.exit(1)
"""
    with open("temp_val.py", "w") as f:
        f.write(script)
    
    result = subprocess.run([python_exe, "temp_val.py"], capture_output=True, text=True)
    if os.path.exists("temp_val.py"): os.remove("temp_val.py")
    
    if result.returncode == 0:
        return True
    else:
        print(f"\033[91mValidation Error: {result.stdout.strip()}\033[0m")
        return False

def main():
    clear_screen()
    print_banner()

    print("\n[1/3] Installing Dependencies (on D: drive)")
    print("-" * 30)
    
    # Set TEMP and TMP for D: drive to avoid C: space issues (Windows only)
    if sys.platform == "win32":
        os.environ['TEMP'] = 'D:\\temp'
        os.environ['TMP'] = 'D:\\temp'
    
    venv_cmd = f"{sys.executable} -m venv venv"
    
    deps = "pyautogui pillow google-generativeai psutil python-dotenv customtkinter openai"
    if sys.platform == "win32":
        pip_cmd = f".\\venv\\Scripts\\pip install {deps} pywin32"
    else:
        pip_cmd = f"./venv/bin/pip install {deps}"
    
    if not os.path.exists("venv"):
        if run_command(venv_cmd):
            print("\033[92m✔ Virtual environment created.\033[0m")
        else:
            print("\033[91m✘ Failed to create virtual environment.\033[0m")
            return

    if run_command(pip_cmd):
        print("\033[92m✔ Dependencies installed successfully.\033[0m")
    else:
        print("\033[91m✘ Failed to install dependencies.\033[0m")
        return

    print("\n[2/3] Configuring AI Services")
    print("-" * 30)
    
    while True:
        gemini_key = input("Enter Gemini API Key (press Enter to skip): ").strip()
        if validate_key_via_venv("gemini", gemini_key): break
        print("\033[91mInvalid Gemini Key. Please try again.\033[0m")

    while True:
        openai_key = input("Enter OpenAI API Key (press Enter to skip): ").strip()
        if validate_key_via_venv("openai", openai_key): break
        print("\033[91mInvalid OpenAI Key. Please try again.\033[0m")

    # Default to Gemini if available, else OpenAI
    pref_provider = "gemini" if gemini_key else ("openai" if openai_key else "gemini")

    print("\n[3/3] Saving Configuration...")
    with open(".env", "w") as f:
        if gemini_key:
            f.write(f"GEMINI_API_KEY={gemini_key}\n")
        if openai_key:
            f.write(f"OPENAI_API_KEY={openai_key}\n")
    
    with open("config.json", "w") as f:
        json.dump({"default_provider": pref_provider}, f)
        
    print("\033[92m✔ Configuration saved.\033[0m")

    print("\n" + "="*50)
    print("\033[92m🎉 SETUP COMPLETE!\033[0m")
    print("You can now build and run Adaptix:")
    if sys.platform == "win32":
        print("\033[94m  1. npm run build\033[0m")
        print("\033[94m  2. Open Adaptix_App folder and run Adaptix_App.exe\033[0m")
    else:
        print("\033[94m  1. npm run build-macos\033[0m")
        print("\033[94m  2. Run the Adaptix_App executable in the current folder\033[0m")
    print("="*50)

if __name__ == "__main__":
    main()
