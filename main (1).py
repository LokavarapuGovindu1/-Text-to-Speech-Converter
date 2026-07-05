"""
Text-to-Speech Converter
--------------------------
A simple desktop application that converts typed text into natural-sounding
speech using the pyttsx3 speech synthesis engine, with a Tkinter GUI for
easy interaction.

Features:
  - Type or paste any text and have it read aloud
  - Adjustable speech rate (speed) and volume
  - Choose between available system voices (e.g. male/female)
  - Pause is simulated via stop (pyttsx3 does not support true pause/resume)
  - Save the spoken text as an audio (.mp3) file

Author: Lokavarapu Govindu
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyttsx3
import threading


class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Converter")
        self.root.geometry("560x480")
        self.root.resizable(False, False)

        # Initialize the TTS engine
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty("voices")
        self.is_speaking = False

        self._build_ui()

    # ------------------------------------------------------------------
    # UI Construction
    # ------------------------------------------------------------------
    def _build_ui(self):
        title_label = tk.Label(
            self.root, text="Text-to-Speech Converter",
            font=("Segoe UI", 16, "bold")
        )
        title_label.pack(pady=(15, 5))

        # Text input box
        text_frame = tk.Frame(self.root)
        text_frame.pack(padx=15, pady=10, fill="both", expand=True)

        self.text_box = tk.Text(text_frame, wrap="word", font=("Segoe UI", 11), height=12)
        self.text_box.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.text_box.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_box.config(yscrollcommand=scrollbar.set)

        # Controls frame
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(padx=15, pady=10, fill="x")

        # Voice selection
        tk.Label(controls_frame, text="Voice:").grid(row=0, column=0, sticky="w", pady=5)
        voice_names = [voice.name for voice in self.voices] if self.voices else ["Default"]
        self.voice_var = tk.StringVar(value=voice_names[0])
        voice_dropdown = ttk.Combobox(
            controls_frame, textvariable=self.voice_var,
            values=voice_names, state="readonly", width=30
        )
        voice_dropdown.grid(row=0, column=1, sticky="w", padx=10)

        # Speech rate slider
        tk.Label(controls_frame, text="Speed:").grid(row=1, column=0, sticky="w", pady=5)
        self.rate_var = tk.IntVar(value=175)
        rate_slider = tk.Scale(
            controls_frame, from_=100, to=300, orient="horizontal",
            variable=self.rate_var, length=220
        )
        rate_slider.grid(row=1, column=1, sticky="w", padx=10)

        # Volume slider
        tk.Label(controls_frame, text="Volume:").grid(row=2, column=0, sticky="w", pady=5)
        self.volume_var = tk.DoubleVar(value=1.0)
        volume_slider = tk.Scale(
            controls_frame, from_=0.0, to=1.0, resolution=0.1, orient="horizontal",
            variable=self.volume_var, length=220
        )
        volume_slider.grid(row=2, column=1, sticky="w", padx=10)

        # Buttons frame
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=15)

        self.speak_btn = tk.Button(
            buttons_frame, text="▶ Speak", width=12, bg="#4CAF50", fg="white",
            font=("Segoe UI", 10, "bold"), command=self.speak_text
        )
        self.speak_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = tk.Button(
            buttons_frame, text="■ Stop", width=12, bg="#f44336", fg="white",
            font=("Segoe UI", 10, "bold"), command=self.stop_speaking
        )
        self.stop_btn.grid(row=0, column=1, padx=5)

        self.save_btn = tk.Button(
            buttons_frame, text="💾 Save as MP3", width=14,
            font=("Segoe UI", 10), command=self.save_as_audio
        )
        self.save_btn.grid(row=0, column=2, padx=5)

        self.clear_btn = tk.Button(
            buttons_frame, text="Clear", width=10,
            font=("Segoe UI", 10), command=self.clear_text
        )
        self.clear_btn.grid(row=0, column=3, padx=5)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root, textvariable=self.status_var, bd=1, relief="sunken",
            anchor="w", font=("Segoe UI", 9)
        )
        status_bar.pack(side="bottom", fill="x")

    # ------------------------------------------------------------------
    # Core Functionality
    # ------------------------------------------------------------------
    def _apply_settings(self):
        """Apply the currently selected voice, rate, and volume to the engine."""
        selected_voice_name = self.voice_var.get()
        for voice in self.voices:
            if voice.name == selected_voice_name:
                self.engine.setProperty("voice", voice.id)
                break

        self.engine.setProperty("rate", self.rate_var.get())
        self.engine.setProperty("volume", self.volume_var.get())

    def speak_text(self):
        """Speak the text currently in the text box (runs in a separate thread)."""
        text = self.text_box.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("No Text", "Please enter some text to speak.")
            return

        if self.is_speaking:
            messagebox.showinfo("Already Speaking", "Please stop the current speech first.")
            return

        self._apply_settings()
        self.status_var.set("Speaking...")
        self.is_speaking = True

        # Run speech in a background thread so the GUI doesn't freeze
        thread = threading.Thread(target=self._run_speech, args=(text,), daemon=True)
        thread.start()

    def _run_speech(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        finally:
            self.is_speaking = False
            self.status_var.set("Ready")

    def stop_speaking(self):
        """Stop any ongoing speech immediately."""
        self.engine.stop()
        self.is_speaking = False
        self.status_var.set("Stopped")

    def save_as_audio(self):
        """Save the current text as an MP3 audio file."""
        text = self.text_box.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("No Text", "Please enter some text to save.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 Audio", "*.mp3")],
            title="Save Speech As"
        )
        if not file_path:
            return

        self._apply_settings()
        self.status_var.set("Saving audio...")
        try:
            self.engine.save_to_file(text, file_path)
            self.engine.runAndWait()
            self.status_var.set(f"Saved to {file_path}")
            messagebox.showinfo("Saved", f"Audio saved successfully:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save audio:\n{e}")
            self.status_var.set("Ready")

    def clear_text(self):
        """Clear the text box."""
        self.text_box.delete("1.0", tk.END)
        self.status_var.set("Ready")


def main():
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
