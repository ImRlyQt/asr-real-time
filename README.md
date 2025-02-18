# ASR Whisper gRPC - Real-time Speech Transcription

## Project Description

A desktop application for **Windows** that transcribes speech in **Polish** in real time. It utilizes **OpenAI Whisper** to convert audio into text and **gRPC** for communication between the ASR server and the GUI client.

---

## Features

✅ **Live speech transcription** – continuously displays spoken words in the GUI.\
✅ **No repeated words** – prevents looping in transcription.\
✅ **Polish language support** – Whisper operates exclusively in Polish mode.\
✅ **Simple user interface** – lightweight GUI using Tkinter.\
✅ **Modular architecture** – the gRPC server can operate independently from the client.

---

## Requirements

🔹 **Python 3.8+ up to 3.11**\ 
🔹 **Windows 10/11**\
🔹 **Microphone**

### Installing Dependencies

```bash
pip install torch openai-whisper sounddevice numpy grpcio grpcio-tools protobuf tkinter
```

## Running the Application

### **1️⃣ Start the gRPC Server**

```bash
python asr_server.py
```

### **2️⃣ Start the GUI Client**

```bash
python asr_client.py
```


