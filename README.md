[README.md](https://github.com/user-attachments/files/29678747/README.2.md)
# 🔊 Text-to-Speech Converter

A simple desktop application that converts typed text into natural-sounding speech, built with **Python**, **pyttsx3**, and a **Tkinter** GUI.

<!-- Add a demo GIF or screenshot here once available -->
<!-- ![Demo](screenshots/demo.gif) -->

---

## 📌 Overview

This application lets you type or paste any text and have it read aloud using your system's built-in text-to-speech voices — no internet connection required, since `pyttsx3` works fully offline. It includes adjustable speech rate and volume, voice selection, and the ability to export the spoken text as an MP3 file.

## ✨ Features

- 🗣️ **Text-to-Speech** — Converts any typed or pasted text into spoken audio
- 🎚️ **Adjustable Speed & Volume** — Fine-tune how fast and how loud the speech plays
- 🎙️ **Voice Selection** — Choose between all voices installed on your system (e.g. male/female, different languages)
- ⏹️ **Stop Anytime** — Instantly stop playback mid-sentence
- 💾 **Save as MP3** — Export the spoken text as an audio file to keep or share
- 🖥️ **Simple GUI** — Built with Tkinter for an easy, no-frills desktop experience
- ⚡ **Fully Offline** — No internet or API key required

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Speech Synthesis | [pyttsx3](https://pyttsx3.readthedocs.io/) |
| GUI | Tkinter (Python standard library) |
| Language | Python 3.8+ |

## ⚙️ How It Works

1. Tkinter renders a simple window with a text box, sliders for speed/volume, a voice dropdown, and control buttons.
2. When you click **Speak**, the app applies your selected voice, rate, and volume settings to the `pyttsx3` engine, then runs speech synthesis in a background thread so the GUI doesn't freeze while speaking.
3. **Stop** immediately halts the engine's current speech.
4. **Save as MP3** uses `pyttsx3`'s `save_to_file()` method to render the same text to an audio file instead of playing it live.

## 📂 Project Structure

```
text-to-speech-converter/
├── main.py             # Main application script
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- **Windows**: works out of the box (uses SAPI5 voices)
- **macOS**: works out of the box (uses NSSpeechSynthesizer)
- **Linux**: requires `espeak` installed — `sudo apt-get install espeak`

### Installation

```bash
# Clone the repository
git clone https://github.com/LokavarapuGovindu1/text-to-speech-converter.git
cd text-to-speech-converter

# (Optional but recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
python main.py
```

- Type or paste text into the text box.
- Adjust **Voice**, **Speed**, and **Volume** as desired.
- Click **▶ Speak** to hear it read aloud.
- Click **■ Stop** to stop playback immediately.
- Click **💾 Save as MP3** to export the speech as an audio file.
- Click **Clear** to reset the text box.

## 🧗 Challenges & Learnings

- Running speech synthesis on the main thread froze the Tkinter GUI, so speech playback was moved to a background thread using Python's `threading` module.
- `pyttsx3` doesn't support true pause/resume — only stop — which shaped the UI to offer Speak/Stop instead of Play/Pause.
- Voice availability differs by operating system, so the voice list is populated dynamically from `engine.getProperty("voices")` rather than hardcoded.

## 🔮 Future Improvements

- [ ] Add support for reading text directly from uploaded `.txt` or `.pdf` files
- [ ] Add a true pause/resume feature using audio segment chunking
- [ ] Add highlighting of the currently spoken word/sentence
- [ ] Package as a standalone `.exe` / `.app` using PyInstaller

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Connect

**Lokavarapu Govindu**
[LinkedIn](https://linkedin.com/in/lokavarapugovindu) • [GitHub](https://github.com/LokavarapuGovindu1)
