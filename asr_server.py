import grpc
import whisper
import numpy as np
import sounddevice as sd
import asr_pb2
import asr_pb2_grpc
from concurrent import futures

# Wczytaj model Whisper z wymuszeniem języka polskiego
model = whisper.load_model("medium")  # Możesz użyć "medium" lub "large"

class ASRService(asr_pb2_grpc.ASRServicer):
    def __init__(self):
        self.previous_text = ""  # Przechowuje ostatnią transkrypcję

    def Transcribe(self, request_iterator, context):
        buffer = bytearray()
        
        for chunk in request_iterator:
            buffer.extend(chunk.audio_data)

            if len(buffer) > 16000 * 2:  # Przetwarzaj co ~1 sekundę
                audio = np.frombuffer(buffer, dtype=np.int16).astype(np.float32) / 32768.0
                result = model.transcribe(audio, language="pl")  # Wymuszenie języka polskiego
                
                new_text = result["text"].strip()
                
                # Usuwamy powtarzające się słowa
                if new_text.startswith(self.previous_text):
                    new_text = new_text[len(self.previous_text):].strip()
                
                self.previous_text += " " + new_text if new_text else ""
                
                yield asr_pb2.Transcription(text=new_text)
                buffer.clear()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    asr_pb2_grpc.add_ASRServicer_to_server(ASRService(), server)
    server.add_insecure_port("[::]:50051")
    print("Serwer gRPC uruchomiony na porcie 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
