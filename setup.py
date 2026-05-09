import os
import subprocess
import sys

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

import json

def validate_gemini(key):
    if not key: return True
    import google.generativeai as genai
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        model.generate_content("test", generation_config={"max_output_tokens": 1})
        return True
    except Exception as e:
        print(f"\033[91mGemini Error: {e}\033[0m")
        return False

def validate_openai(key):
    if not key: return True
    from openai import OpenAI
    try:
        client = OpenAI(api_key=key)
        client.models.list()
        return True
    except Exception as e:
        print(f"\033[91mOpenAI Error: {e}\033[0m")
        return False

def main():
    clear_screen()
    print_banner()

    print("\n[1/3] Configuring AI Services")
    print("-" * 30)
    
    while True:
        gemini_key = input("Enter Gemini API Key (press Enter to skip): ").strip()
        if validate_gemini(gemini_key): break
        print("\033[91mInvalid Gemini Key. Please try again.\033[0m")

    while True:
        openai_key = input("Enter OpenAI API Key (press Enter to skip): ").strip()
        if validate_openai(openai_key): break
        print("\033[91mInvalid OpenAI Key. Please try again.\033[0m")

    pref_provider = input("\nWhich provider do you prefer as default? (Gemini/OpenAI): ").strip().lower()
    if pref_provider not in ["gemini", "openai"]:
        pref_provider = "gemini"

    # Create .env file
    print("\n[2/3] Saving Configuration...")
    with open(".env", "w") as f:
        if gemini_key:
            f.write(f"GEMINI_API_KEY={gemini_key}\n")
        if openai_key:
            f.write(f"OPENAI_API_KEY={openai_key}\n")
    
    with open("config.json", "w") as f:
        json.dump({"default_provider": pref_provider}, f)
        
    print("\033[92m✔ Configuration saved.\033[0m")

    print("\n[3/3] Installing Dependencies (on D: drive)")
    print("-" * 30)
    
    # Set TEMP and TMP for D: drive to avoid C: space issues
    os.environ['TEMP'] = 'D:\\temp'
    os.environ['TMP'] = 'D:\\temp'
    
    venv_cmd = "python -m venv venv"
    pip_cmd = ".\\venv\\Scripts\\pip install pyautogui pillow google-generativeai psutil python-dotenv pywin32 customtkinter openai"
    
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

    print("\n" + "="*50)
    print("\033[92m🎉 SETUP COMPLETE!\033[0m")
    print("You can now start Adaptix using:")
    print("\033[94m  npm start\033[0m")
    print("="*50)

if __name__ == "__main__":
    main()
