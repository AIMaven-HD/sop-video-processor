import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import shutil
import subprocess
from tkinter import messagebox, filedialog
import sys

def find_ffmpeg():
    ffmpeg_exe = "ffmpeg.exe" if os.name == 'nt' else "ffmpeg"
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ffmpeg_exe)
    local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg", ffmpeg_exe)
    if os.path.exists(local_path):
        return local_path
    return shutil.which(ffmpeg_exe)

class VideoProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SOP Video Processor")
        self.root.geometry("600x400")
        self.ffmpeg_path = find_ffmpeg()
        status_text = f"FFmpeg Status: {'Found' if self.ffmpeg_path else 'Missing'}"
        self.label = tk.Label(root, text="Drag & Drop Video Files Here", bg="lightgray")
        self.label.pack(pady=20, padx=20, expand=True, fill=tk.BOTH)
        self.label.drop_target_register(DND_FILES)
        self.label.dnd_bind('<<Drop>>', self.drop)
        self.status_label = tk.Label(root, text=status_text, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def drop(self, event):
        files = self.root.tk.splitlist(event.data)
        if not self.ffmpeg_path:
            messagebox.showerror("Error", "FFmpeg not found.")
            return
        for f in files:
            self.process_video(f)

    def process_video(self, file_path):
        try:
            output_file = os.path.splitext(file_path)[0] + "_processed.mp4"
            cmd = [self.ffmpeg_path, "-i", file_path, "-c", "copy", output_file]
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTUPINFO.dwFlags
            subprocess.run(cmd, check=True, startupinfo=startupinfo)
            messagebox.showinfo("Success", f"Processed: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = VideoProcessorApp(root)
    root.mainloop()
