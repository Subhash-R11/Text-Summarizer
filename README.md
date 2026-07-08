# Text Summarizer

A Streamlit app that summarizes text using Llama 3.3 (70B) via the Groq API.

## Demo

<img width="1817" height="867" alt="Screenshot 2026-07-08 183911" src="https://github.com/user-attachments/assets/fa937349-0410-423a-8a6f-6376fb39becc" />

## Features

- Paste any text and get a summary
- Choose summary style: Concise Prose, Bullet Points, Explain Simply, Academic
- Choose length: Short, Medium, Long
- Word count stats and compression ratio
- Key points extracted separately
- Download summary as a `.txt` file

## Setup

1. Clone the repo and install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
   Get a key from [console.groq.com](https://console.groq.com/keys).

3. Run the app:
   ```
   streamlit run app.py
   ```

## Files

- `app.py` — Streamlit UI
- `summarizer.py` — Groq API call and response parsing
- `requirements.txt` — dependencies
