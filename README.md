# 🎨 Wordle Art Solver

This is a custom **Wordle pattern solver** designed to help you create visual "art" using specific feedback patterns from the popular Wordle game.

## 📌 What is this?

The **Wordle Art Solver** is a playful tool that lets you:
- Input the actual Wordle answer of the day.
- Configure custom feedback patterns (green, yellow, grey, and half-green-yellow).
- Automatically fill in candidate words that match those patterns.
- Build 5x6 "Wordle boards" using rules you control — useful for making visual patterns or stylized art using valid Wordle mechanics.

## 🤔 Why I created this

I got tired of manually crafting fake Wordle boards to troll my friends on Discord — it was fun, but time-consuming.  
So I built a UI that automates the process and lets me design weird and funny Wordle "artboards" quickly and easily.

This tool saves time, keeps it valid with real words, and still lets me have fun being chaotic.

## 🎮 Try It Online

You can use the Wordle Art Generator directly in your browser — no installation needed:

👉 [Launch WordleArt on Streamlit Cloud](https://wordleart.streamlit.app/)

## 🖥️ Run It Locally

Prefer to run it on your own machine or make custom tweaks? Follow the instructions below to get set up.

## 🧰 How to Run It

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/wordle-art.git
cd wordle-art
```
2. Install Requirements

Make sure you have Python 3.8+ and Streamlit:
```bash
pip install streamlit
```
3. Add Word List

Download valid-wordle-words.txt from this source for updated list:
🔗 https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93 

Place it in the same directory as the code.
4. Run the App
```bash
streamlit run WordleArtUI.py
```
5. Use It

    Enter the Wordle answer of the day (used to simulate feedback).

    Click on boxes to cycle through colors:
    grey → half (green/yellow) → yellow → green → back to grey.

    Matching candidate words will appear inside the boxes and in a list below.

🎨 Features

    5x6 Wordle grid layout

    Visual feedback via clickable color tiles

    Supports custom feedback logic including hybrid (green/yellow)

    Automatically finds valid words based on the pattern

    Real-time updates with Streamlit

📁 Project Structure
```bash
.
├── WordleArt.py              # Backend logic
├── WordleArtUI.py            # Streamlit frontend
├── valid-wordle-words.txt    # Word list (required)
└── README.md
```
📃 License

MIT License. Free to use, modify, or remix.
