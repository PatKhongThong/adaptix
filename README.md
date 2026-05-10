# 🧠 Adaptix AI

**Adaptix** is a premium, open-source AI tool that learns your computer habits and behaviors to provide insights into your productivity and workflow. It runs locally on your machine, capturing screen context to build a behavioral profile using state-of-the-art AI.

---

## ✨ Features

- **Deep Content Analysis**: AI inspects your window content (searches, messages, videos) for a true understanding of your work.
- **Session Summarization**: Hierarchical reports (App > Action > Detail) provide granular insights.
- **Long-Term Memory**: The AI learns your habits over time and remembers you across restarts.
- **History Dashboard**: A dedicated archive browser to review all your past sessions in detail.
- **Privacy First**: All data is processed using your personal API keys. Data stays on your machine.
- **Premium Desktop UI**: A sleek, dark-mode interface with a custom logo.

---

## 🚀 Quick Start

Follow these steps to get Adaptix running:

### 1. Initial Setup
Configure your API keys (Gemini or OpenAI) and install dependencies automatically:
```bash
npm run setup
```

### 2. Build or Update
Compile the project into a professional standalone application, or update it after code changes:

**Windows:**
```bash
# First time build
npm run build

# Update after changes
npm run update
```

**macOS:**
```bash
# First time build
npm run build-macos

# Update after changes
npm run update-macos
```

### 3. Run Adaptix
- **Windows**: Open the **`Adaptix_App`** folder and double-click **`Adaptix_App.exe`**.
- **macOS**: Open the **`Adaptix_App`** folder and double-click the **`Adaptix_App`** executable.

---

## ⚙️ Configuration

- **API Keys**: Managed via the setup script or manually in the `.env` file.
- **Memory**: Your behavioral history is stored locally in `D:\temp\adaptix_memory.json`.
- **Default Provider**: Set automatically during setup, can be changed in `config.json`.

---

## 🛠️ How It Works

1. **Collector**: A background agent captures your screen every 2 seconds.
2. **AI Engine**: Snapshots are analyzed by Gemini 2.0 or GPT-4o to identify specific tasks and context.
3. **Archive**: Every session is summarized and stored in a historical archive for you to review later.

---

## 📄 License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.
