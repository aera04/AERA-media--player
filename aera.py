import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import vlc
from PIL import Image, ImageTk
import os

class MediaPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("NEON A/V Player")
        self.root.geometry("800x480")
        self.root.configure(bg="#141e30")

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = None

        # Title
        self.title = tk.Label(root, text="NEON AUDIO/VIDEO PLAYER", font=("Orbitron", 18, "bold"),
                              fg="#00ffe7", bg="#141e30")
        self.title.pack(pady=12)

        # Video frame
        self.video_panel = tk.Frame(root, bg="#262a36", width=640, height=320)
        self.video_panel.pack(pady=5)
        self.video_panel.pack_propagate(False)

        # Song/Video Label
        self.media_label = tk.Label(root, text="No file loaded", font=("Orbitron", 12),
                                    fg="#fff", bg="#141e30")
        self.media_label.pack(pady=6)

        # Controls Frame
        controls = tk.Frame(root, bg="#141e30")
        controls.pack(pady=5)

        self.play_btn = tk.Button(controls, text="▶", font=("Orbitron", 16, "bold"), fg="#00ffe7", bg="#141e30", bd=0, command=self.play)
        self.pause_btn = tk.Button(controls, text="⏸", font=("Orbitron", 16, "bold"), fg="#00ffe7", bg="#141e30", bd=0, command=self.pause)
        self.stop_btn = tk.Button(controls, text="⏹", font=("Orbitron", 16, "bold"), fg="#00ffe7", bg="#141e30", bd=0, command=self.stop)
        self.open_btn = tk.Button(controls, text="📂", font=("Orbitron", 16), fg="#00ffe7", bg="#141e30", bd=0, command=self.open_file)

        self.open_btn.grid(row=0, column=0, padx=10)
        self.play_btn.grid(row=0, column=1, padx=10)
        self.pause_btn.grid(row=0, column=2, padx=10)
        self.stop_btn.grid(row=0, column=3, padx=10)

        # Volume control
        self.volume = tk.Scale(root, from_=0, to=200, orient=tk.HORIZONTAL, length=300,
                               label="VOLUME", font=("Orbitron", 10), fg="#00ffe7",
                               bg="#141e30", troughcolor="#00ffe7", highlightbackground="#141e30")
        self.volume.set(200)
        self.volume.pack(pady=8)
        self.volume.bind("<B1-Motion>", self.set_volume)

        # Footer
        self.footer = tk.Label(root, text="Futuristic UI • github.com/aera04", font=("Orbitron", 8),
                               fg="#00ffe7", bg="#141e30")
        self.footer.pack(side=tk.BOTTOM, pady=8)

        self.filename = None

    def set_video_window(self):
        # Set video output window for different OS
        if os.name == "nt":  # for Windows
            self.player.set_hwnd(self.video_panel.winfo_id())
        else:
            self.player.set_xwindow(self.video_panel.winfo_id())

    def open_file(self):
        self.filename = filedialog.askopenfilename(
            title="Select Media File",
            filetypes=(("Media Files", "*.mp4 *.avi *.mkv *.mp3 *.wav *.ogg"),)
        )
        if self.filename:
            basename = os.path.basename(self.filename)
            self.media_label.config(text=f"Loaded: {basename}")
            self.media = self.instance.media_new(self.filename)
            self.player.set_media(self.media)
            self.set_video_window()  # Set the video output to the tkinter frame

    def play(self):
        if self.filename:
            self.set_video_window()
            self.player.play()
            self.media_label.config(text=f"Playing: {os.path.basename(self.filename)}")

    def pause(self):
        self.player.pause()
        self.media_label.config(text="Paused")

    def stop(self):
        self.player.stop()
        self.media_label.config(text="Stopped")

    def set_volume(self, event):
        self.player.audio_set_volume(self.volume.get())

if __name__ == "__main__":
    root = tk.Tk()
    MediaPlayer(root)
    root.mainloop()
