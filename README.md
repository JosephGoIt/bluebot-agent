# Bluebot Agent

An autonomous browser automation agent powered by Gemini and browser-use.

---

## Option A — Windows Installer (Recommended)

No Python or dependencies needed. Everything is bundled.

1. Go to [Releases](https://github.com/JosephGoIt/bluebot-agent/releases/latest)
2. Download `Bluebot-Setup.exe` and run it
3. Open `config.txt` — the installer shows you the exact path, but it's always at:
   `C:\Users\<you>\AppData\Roaming\Bluebot Agent\config.txt`
4. Fill in your credentials:

```
GEMINI_API_KEY=your_key_here
CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
```

5. Launch **Bluebot Agent** from the desktop shortcut

Get a free Gemini API key at https://aistudio.google.com/apikey

**Requirements:** Windows 10/11 (64-bit) · Google Chrome · Gemini API key

---

## Option B — Run from Source (Developers / Power Users)

Requires Python 3.12+.

```
git clone https://github.com/JosephGoIt/bluebot-agent.git
cd bluebot-agent
setup.bat
```

`setup.bat` handles everything automatically:
- Creates a virtual environment
- Installs all dependencies
- Force-reinstalls pydantic/pydantic-core compiled extensions
- Installs Playwright Chromium as a fallback browser
- Creates a `config.txt` template

Then edit `config.txt` and run:

```
venv\Scripts\python.exe main.py
```

---

## Usage

Enter your task in the text box and click **Execute Task**. The agent will open Chrome, perform the task autonomously, and display the result in the app.
