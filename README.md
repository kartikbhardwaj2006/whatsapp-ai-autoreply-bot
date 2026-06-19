# WhatsApp AI Auto Reply Bot

## Overview

WhatsApp AI Auto Reply Bot is a Python-based desktop automation project that automatically reads WhatsApp Desktop conversations, generates AI-powered responses using Large Language Models (LLMs), and sends replies without manual intervention.

The project combines desktop automation, clipboard management, and conversational AI to create a smart automated messaging assistant.

---

## Features

* Automatic WhatsApp Desktop interaction
* Reads chat messages directly from the screen
* Copies conversation history
* AI-generated replies using Groq LLM API
* Personalized response generation
* Supports Hindi and English conversations
* Desktop automation using PyAutoGUI
* Lightweight Python implementation

---

## Tech Stack

### Programming Language

* Python

### Libraries

* PyAutoGUI
* Pyperclip
* PyGetWindow
* OpenAI SDK
* pywin32

### AI Model

* Llama 3.3 70B Versatile (Groq API)

---

## Project Workflow

1. Open WhatsApp Desktop.
2. Read recent chat messages.
3. Copy conversation history.
4. Send chat context to the AI model.
5. Generate a human-like response.
6. Automatically paste and send the message.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/whatsapp-ai-autoreply-bot.git
cd whatsapp-ai-autoreply-bot
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure API Key

Create a `.env` file and add your API key:

```env
GROQ_API_KEY=your_api_key
```

### Run Bot

```bash
python 03_bot.py
```

---

## Project Structure

```text
├── 01_get_cursor.py
├── 02_openai.py
├── 03_bot.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Future Improvements

* Dynamic chat detection
* Multi-contact support
* Voice message support
* Sentiment analysis
* Automatic contact selection
* Web dashboard
* Memory-based conversations
* OCR-based chat extraction

---

## Learning Outcomes

* Desktop automation
* LLM integration
* Prompt engineering
* API handling
* Python scripting
* Human-computer interaction

---

## Author

Kartik Bhardwaj
