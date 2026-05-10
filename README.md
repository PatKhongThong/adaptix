
**Adaptix** - Open source tool that tracks your habits on your computer by taking screenshots every 2 seconds

How to setup -
Click code
Download zip file
Extract all from zip file
After clicking into the adaptix file folder, you should see another file folder called adaptix. Right click that folder and open in terminal.

Windows (Make sure you have Python3 and Node.js installed) ---In terminal type in npm run setup, then after entering an API key and finishing setup, run npm run build. Once build is done, click into adaptix folder till you see a folder called Adaptix_App and click into it. You should see an application called Adaptix_App, now you can start it. To update adaptix, run npm run update

MacOS (Make sure you have Python3 and Node.js installed) --- In terminal type in npm run setup, then after entering an API key and finishing setup, run npm run build-macos. Once build is done, click into adaptix folder till you see a folder called Adaptix_App and click into it. You should see an application called Adaptix_App, now you can start it. To update adaptix, run npm run update-macos

Ubuntu/Linux (Make sure you have Python3 and Node.js installed) --- In terminal, first install system dependencies: `sudo apt-get update && sudo apt-get install scrot python3-tk python3-dev x11-utils`. Then type `npm run setup`, finish the configuration, and run `npm run build-linux`. Once the build is complete, you will see an `Adaptix_App` executable in the folder. To update, run `npm run update-linux`.



## 📄 License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.
