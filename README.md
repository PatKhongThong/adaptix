
**Adaptix** - Open source tool that tracks your habits on your computer by taking screenshots every 2 seconds

How to setup -
Click code
Download zip file
Extract all from zip file
After clicking into the adaptix file folder, you should see another file folder called adaptix. Right click that folder and open in terminal.

Windows (Make sure you have Python3 and Node.js installed) ---In terminal type in npm run setup, then after entering an API key and finishing setup, run npm run build. Once build is done, click into adaptix folder till you see a folder called Adaptix_App and click into it. You should see an application called Adaptix_App, now you can start it. To update adaptix, run npm run update

MacOS (Make sure you have Python3 and Node.js installed) --- In terminal type in npm run setup, then after entering an API key and finishing setup, run npm run build-macos. Once build is done, click into adaptix folder till you see a folder called Adaptix_App and click into it. You should see an application called Adaptix_App, now you can start it. To update adaptix, run npm run update-macos

### 3. Run Adaptix
- **Windows**: Open the **`Adaptix_App`** folder and double-click **`Adaptix_App.exe`**.
- **macOS**: Open the **`Adaptix_App`** folder and double-click the **`Adaptix_App`** executable.

---

## ⚙️ Configuration

- **API Keys**: Managed via the setup script or manually in the `.env` file.
- **Memory**: Your behavioral history is stored locally in `~/.adaptix/adaptix_memory.json`.
- **Default Provider**: Set automatically during setup, can be changed in `config.json`.

---

## 🛠️ How It Works

1. **Collector**: A background agent captures your screen every 2 seconds.
2. **AI Engine**: Snapshots are analyzed by Gemini 2.0 or GPT-4o to identify specific tasks and context.
3. **Archive**: Every session is summarized and stored in a historical archive for you to review later.

---

## 📄 License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.
