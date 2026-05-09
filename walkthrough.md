# Adaptix Walkthrough

I have successfully built **Adaptix** as a standalone desktop application on your **D: drive**.

## Features Implemented
- **Dual AI Support**: Choose between **Gemini 2.0 Flash** or **OpenAI GPT-4o**.
- **NPM Integration**: You can now manage and launch the app using standard `npm` commands.
- **Syntax Fixes**: Resolved all "Problem" markers by fixing invalid Python grid arguments.

## How to Run Adaptix

### Option A: Using NPM (Recommended)
1.  Open your terminal in `d:\adaptix\adaptix`.
2.  Run `npm run setup` to install all Python dependencies.
3.  Run `npm start` to launch the application.

### Option B: Using the Batch File
1.  Double-click the `run_adaptix.bat` file in the project folder.

## AI Configuration
- **Gemini**: Get a key from [Google AI Studio](https://aistudio.google.com/).
- **OpenAI**: Get a key from [OpenAI Dashboard](https://platform.openai.com/).
- Select your provider from the dropdown menu in the app before clicking "Start Observing".

## File Structure
- `main.py`: The UI and main application loop.
- `collector.py`: The background logic for capturing screenshots and window titles.
- `venv/`: A local Python environment containing all dependencies.
- `run_adaptix.bat`: A simple shortcut to start the app.

> [!TIP]
> You can pause or stop the observation at any time using the big red "Stop Observing" button. All analysis happens locally on your machine (via the API you provided).
