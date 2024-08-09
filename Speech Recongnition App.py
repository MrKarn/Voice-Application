import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext

class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        
        # Create a scrolled text widget for displaying the recognized text
        self.text_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=50)
        self.text_display.pack(padx=10, pady=10)
        
        # Create a button to start listening
        self.listen_button = tk.Button(root, text="Listen", command=self.start_listening)
        self.listen_button.pack(pady=5)
        
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        self.end_program = False
    
    def capture_voice_input(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        return audio
    
    def convert_voice_to_text(self, audio):
        try:
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Sorry, my speech service is down."
    
    def speak_text(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
    
    def process_voice_command(self, text):
        if "stop" in text.lower():
            self.speak_text("Stopping the program.")
            self.end_program = True
        else:
            self.speak_text("You said: " + text)
        self.text_display.insert(tk.END, text + '\n')
        self.text_display.yview(tk.END)  # Scroll to the end
    
    def start_listening(self):
        if not self.end_program:
            self.text_display.insert(tk.END, "Listening...\n")
            self.text_display.yview(tk.END)
            audio = self.capture_voice_input()
            text = self.convert_voice_to_text(audio)
            self.process_voice_command(text)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
