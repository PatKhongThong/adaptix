# 🧠 Adaptix AI

**Adaptix** is a premium, open-source AI tool that learns your computer habits and behaviors to provide insights into your productivity and workflow. It runs locally on your machine, capturing screen context and active application data to build a behavioral profile using state-of-the-art AI.

---

## ✨ Features

- **Ultra-Fast Observation**: Captures snapshots of your screen every **2 seconds** for high-fidelity behavior tracking.
- **Session Summarization**: Generate deep psychological profiles and productivity summaries at the end of every session.
- **Dual AI Engine**: Support for both **Gemini 2.0 Flash** and **OpenAI GPT-4o**.
- **Privacy First**: All data is processed using your personal API keys. Snapshots are stored locally on your machine.
- **Premium Desktop UI**: A sleek, dark-mode interface built with CustomTkinter.

---

## 🚀 Installation

Adaptix is designed to be managed easily through **npm**.

### Prerequisites
- [Python 3.10+](https://www.python.org/)
- [Node.js & npm](https://nodejs.org/)

### Setup
1. Clone the repository to your local machine (recommended on `D:` drive if `C:` is low on space).
2. Open your terminal in the project directory.
3. Run the interactive setup to configure your AI keys and install dependencies:
   ```bash
   npm run setup
   ```
   *The setup will prompt you for your Gemini/OpenAI keys and handle all installation automatically.*

---

## ⚙️ Configuration

1. **API Keys**:
   - For **Gemini**: Get a free key at [Google AI Studio](https://aistudio.google.com/).
   - For **OpenAI**: Get a key at [OpenAI Platform](https://platform.openai.com/).
2. **Environment File**:
   - Rename `.env.example` to `.env`.
   - Add your key to the file (optional, you can also enter it directly in the app).

---

## 🎮 Usage

You can launch Adaptix via terminal:

```bash
npm start
```

### Build a Standalone Windows App (.exe)
If you want to run Adaptix as a standard Windows application without using the terminal, run:
```bash
npm run build
```
This will create an `Adaptix.exe` file inside the `dist/` folder.

---

## 🛠️ How It Works

1. **Collector**: A background Python agent uses `PyAutoGUI` and `pywin32` to capture the current screen and the active window title.
2. **AI Analysis**: The snapshot is sent to your chosen AI provider (Gemini or OpenAI).
3. **Timeline**: The resulting insight is displayed in the "Behavior Timeline," allowing you to see patterns in your computer usage over time.

---

## 📄 License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.
