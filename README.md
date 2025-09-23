# ✋ Hand Gesture Recognition (with Gen Z Voice 😎)

This project is a **fun hand gesture recognition app** built with **Streamlit + OpenCV + MediaPipe**.
It detects your hand gestures via webcam, then responds with **Gen Z-style funny voice lines** using gTTS (Google Text-to-Speech).
Perfect for demos, learning computer vision, or just vibing with your camera 🤙.

---

## 🚀 Features

* Detects common hand gestures:

  * 🤏 Pinch → "Ayo, tiny heart vibes!"
  * ✌️ Peace → "Peace out, homie!"
  * 👉 Wrong finger → "Oops! Wrong finger bro 😂👉"
  * 👌 OK sign → "OK dokie, let's gooo!"
  * 👍 Thumbs up → "Big W! You're awesome"
* Plays back **voice lines automatically** 🎧
* Built with **Streamlit**, so it runs easily in the browser
* Fun, light, and no toxic words 💯

---

## ⚙️ Installation

Clone the repo:

```bash
git clone https://github.com/username/hand-gesture-genz.git
cd hand-gesture-genz
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Steps to use:

1. Allow camera access 📷
2. Show your hand gesture in front of the camera ✋
3. See the detected gesture + hear the funny voice 🎤
4. Enjoy and share with your friends! 😆

---

## 📦 Requirements

* Python 3.8+
* Libraries:

  * `streamlit`
  * `opencv-python`
  * `mediapipe`
  * `numpy`
  * `gTTS`

---

## 📚 How It Works

1. **MediaPipe Hands** → Detects hand landmarks (21 points per hand).
2. **Gesture Recognition Logic** → Classifies gestures based on finger positions & distances.
3. **gTTS + Streamlit** → Converts response text into speech and auto-plays it in the browser.

---

## 🤝 Contributing

Pull requests are welcome!
If you have funny Gen Z catchphrases or want to add more gestures, feel free to contribute 🎉

---

## 📜 License

MIT License – free to use, share, and remix.

---

⚡ *Made with love, code, and too much caffeine ☕.*
