import grpc
import tkinter as tk
import sounddevice as sd
import numpy as np
import asr_pb2
import asr_pb2_grpc
import threading
import queue

BUFFER_SIZE = 1024  
SAMPLE_RATE = 16000
CHANNELS = 1

class ASRClient:
    def __init__(self, gui_callback):
        self.gui_callback = gui_callback
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = asr_pb2_grpc.ASRStub(self.channel)
        self.audio_queue = queue.Queue()
        self.running = False

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status, flush=True)
        self.audio_queue.put(indata.copy())

    def stream_audio(self):
        with sd.InputStream(callback=self.audio_callback, samplerate=SAMPLE_RATE, channels=CHANNELS, dtype="int16"):
            self.running = True
            request_iterator = self.generate_audio_chunks()
            for response in self.stub.Transcribe(request_iterator):
                if response.text.strip():  # Wyeliminowanie pustych transkrypcji
                    self.gui_callback(response.text)

    def generate_audio_chunks(self):
        while self.running:
            chunk = self.audio_queue.get()
            yield asr_pb2.AudioChunk(audio_data=chunk.tobytes())

    def start(self):
        threading.Thread(target=self.stream_audio, daemon=True).start()

class TranscriptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ASR Whisper gRPC")
        self.text_box = tk.Text(root, wrap="word", font=("Arial", 14))
        self.text_box.pack(expand=True, fill="both")
        self.client = ASRClient(self.update_text)
        self.client.start()

    def update_text(self, text):
        self.text_box.insert("end", text + " ")
        self.text_box.see("end")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriptionApp(root)
    root.mainloop()
