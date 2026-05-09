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

def main():
    clear_screen()
    print_banner()

    print("\n[1/3] Configuring AI Services")
    print("-" * 30)
    
    gemini_key = input("Enter Gemini API Key (press Enter to skip): ").strip()
    openai_key = input("Enter OpenAI API Key (press Enter to skip): ").strip()

    # Create .env file
    print("\n[2/3] Generating .env file...")
    with open(".env", "w") as f:
        if gemini_key:
            f.write(f"GEMINI_API_KEY={gemini_key}\n")
        if openai_key:
            f.write(f"OPENAI_API_KEY={openai_key}\n")
    print("\033[92m✔ .env created successfully.\033[0m")

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
