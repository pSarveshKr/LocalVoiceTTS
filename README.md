# 🎙️ LocalVoice TTS
 
**Give any voice to any text — for free, on your own computer.**
 
LocalVoice TTS lets you type dialog lines, assign a different voice to each line, preview them one by one, and combine everything into a single audio file — ready to download.
 
No internet required. No subscription. No data leaves your computer. Ever.
 
---
 
## ✅ What You Can Do
 
- Upload any voice sample and clone it instantly
- Assign a different voice to each line of dialog
- Preview each line before combining
- Combine all lines into one complete audio file
- Download the final audio as a `.wav` file
- Works on **Windows, Mac, and Linux**
---
 
## 💻 What You Need Before Starting
 
You only need to install two things — both are free.
 
### 1. Python 3.10 or higher
1. Go to https://www.python.org/downloads/
2. Download and run the installer
3. **Important:** On the first screen, check the box that says **"Add Python to PATH"**
4. Click Install Now
To confirm it worked, open your terminal and type:
```
python --version
```
You should see something like `Python 3.10.x`
 
---
 
### 2. ffmpeg
ffmpeg handles audio processing behind the scenes.
 
**Windows:**
1. Go to https://ffmpeg.org/download.html
2. Download the Windows build
3. Extract the ZIP file
4. Copy the path to the `bin` folder inside
5. Search for **"Environment Variables"** in Windows search
6. Open it → under **System Variables**, click **Path** → **Edit** → **New**
7. Paste the path → click OK
8. Restart your terminal and type `ffmpeg -version` to confirm
**Mac:**
```
brew install ffmpeg
```
 
**Linux:**
```
sudo apt install ffmpeg
```
 
---
 
## 🚀 Getting Started
 
### Step 1 — Download the project
 
**Option A — Using Git:**
```
git clone https://github.com/YOUR_USERNAME/LocalVoiceTTS.git
cd LocalVoiceTTS
```
 
**Option B — Download ZIP:**
1. Click the green **"Code"** button on GitHub
2. Click **"Download ZIP"**
3. Extract it and open the folder
---
 
### Step 2 — Set up the environment
 
Open your terminal inside the project folder and run these commands one by one:
 
```
python -m venv venv
```
 
**Activate it:**
 
Windows:
```
venv\Scripts\activate
```
 
Mac / Linux:
```
source venv/bin/activate
```
 
---
 
### Step 3 — Install dependencies
 
```
pip install -r requirements.txt
```
 
This will take a few minutes the first time.
 
---
 
### Step 4 — Start the app
 
```
python start.py
```
 
That's it. Your browser will open automatically and the app will be ready to use.
 
To close the app, press `Ctrl + C` in the terminal.
 
---
 
## 🎤 How to Use
 
### Add a Voice
1. At the top of the app, type a name for your voice (e.g. `John` or `Narrator`)
2. Click **"Choose File"** and select a `.wav` or `.mp3` recording (5- 10 second)
3. Click **"Upload Voice"**
4. Your voice will appear as a tag at the top
> **Tip:** Use a clean, clear recording of at least 5–10 seconds for the best results.
 
---
 
### Write Your Dialog
1. Click **"+ Add Line"**
2. Select a voice from the dropdown on the left
3. Type what you want that voice to say
4. Press **Enter** to add the next line
5. Repeat for as many lines as you need
---
 
### Preview a Line
- Click the **▶ Play** button next to any line
- It will speak that line in the selected voice
- Adjust the text or voice and preview again until it sounds right
---
 
### Combine and Download
1. When all lines are ready, click **▶ Combine & Play**
2. The app will process all lines and play the full dialog
3. Click **⬇ Download** to save the final audio as `dialog.wav`
---
 
## ⚠️ First Launch Note
 
The first time you start the app, it will automatically download the AI voice model (~2 GB).
 
- This requires an internet connection — only for the first launch
- It may take 5 to 15 minutes depending on your connection speed
- After that, the app works completely offline
---
 
## 🔧 Something Not Working?
 
**Browser did not open?**
 
Open it manually at:
```
http://127.0.0.1:8000/app
```
 
**"Could not connect to backend" error?**
 
Make sure you ran `python start.py` and it is still running in the terminal.
 
**ffmpeg error?**
 
Make sure ffmpeg is installed and added to PATH. Type `ffmpeg -version` to check.
 
**Synthesis is very slow?**
 
If your computer does not have a dedicated GPU, the app runs on CPU which is slower. Shorter lines will process faster.
 
**Voice quality is not great?**
 
Use a recording that is at least 5–10 seconds long with no background noise. `.wav` format gives the best results.
 
---
 
## ❓ Common Questions
 
**Is this really free?**
Yes. The app is free, open source, and uses free AI models. No subscriptions, no hidden costs.
 
**Does it work without internet?**
Yes — after the first launch (model download), it works completely offline.
 
**How many voices can I add?**
As many as you want. There is no limit.
 
**What languages are supported?**
English, Hindi, Spanish, French, German, Italian, Portuguese, Polish, Turkish, Russian, Dutch, Czech, Arabic, Chinese, Japanese, Korean, and more.
 
**Can I use it on my phone?**
If your phone is on the same Wi-Fi as your computer, open your phone browser and go to:
```
http://YOUR_COMPUTER_IP:8000/app
```
To find your computer's IP: type `ipconfig` on Windows or `ifconfig` on Mac/Linux.
 
**Is my data private?**
Completely. Everything runs on your computer. Nothing is sent to any server.
 
**What audio format is the output?**
The final file is saved as `.wav`. You can convert it to `.mp3` using any free audio converter.
 
---
 
## 📄 License
 
MIT License — free to use, modify, and share.
 
---
 
## 🙏 Credits
 
- [Coqui TTS](https://github.com/coqui-ai/TTS) — AI voice model
- [FastAPI](https://fastapi.tiangolo.com/) — Backend framework
- [pydub](https://github.com/jiaaro/pydub) — Audio processing
---
 
*LocalVoice TTS — Your voice. Your computer. Your control.*