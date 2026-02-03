import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import subprocess
from tkinter import messagebox
import imageio_ffmpeg
import stat
import threading

class VideoProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SOP Video Cutter (720p + 15min)")
        self.root.geometry("600x400")
        
        # 1. GET FFMPEG & FIX PERMISSIONS
        try:
            self.ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            # CRITICAL FIX: Grant execute permission
            st = os.stat(self.ffmpeg_path)
            os.chmod(self.ffmpeg_path, st.st_mode | stat.S_IEXEC)
            status_text = "System Ready"
            status_color = "green"
        except Exception as e:
            self.ffmpeg_path = None
            status_text = f"Error: Engine not found ({str(e)})"
            status_color = "red"

        # GUI Setup
        self.label = tk.Label(root, text="Drag & Drop Video Here\n(Auto-converts to 720p & Splits into 15 min chunks)", bg="lightgray", font=("Arial", 14))
        self.label.pack(pady=20, padx=20, expand=True, fill=tk.BOTH)
        self.label.drop_target_register(DND_FILES)
        self.label.dnd_bind('<<Drop>>', self.drop)

        self.status_label = tk.Label(root, text=status_text, fg=status_color, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def drop(self, event):
        files = self.root.tk.splitlist(event.data)
        if not self.ffmpeg_path:
            messagebox.showerror("Error", "Video engine (FFmpeg) not found.")
            return
        
        # Run in background thread so app doesn't freeze
        threading.Thread(target=self.start_processing, args=(files,), daemon=True).start()

    def start_processing(self, files):
        self.status_label.config(text="Processing... This may take a while. Do not close.", fg="blue")
        for f in files:
            self.process_video(f)
        self.status_label.config(text="Done! Ready for more.", fg="green")

    def process_video(self, file_path):
        try:
            directory = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            
            # Output pattern: myvideo_part000.mp4, myvideo_part001.mp4
            output_pattern = os.path.join(directory, f"{name}_part%03d.mp4")
            
            # COMMAND EXPLANATION:
            # -vf scale=-2:720  -> Resize height to 720p (keep aspect ratio)
            # -segment_time 900 -> Split every 900 seconds (15 mins)
            # -f segment        -> Enable splitting mode
            cmd = [
                self.ffmpeg_path, "-y", 
                "-i", file_path,
                "-vf", "scale=-2:720", 
                "-c:v", "libx264", "-preset", "fast", "-crf", "23",
                "-c:a", "aac",
                "-f", "segment", 
                "-segment_time", "900", 
                "-reset_timestamps", "1", 
                output_pattern
            ]
            
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTUPINFO.dwFlags
            
            subprocess.run(cmd, check=True, startupinfo=startupinfo)
            self.root.after(0, lambda: messagebox.showinfo("Success", f"Finished: {filename}"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed: {str(e)}"))

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = VideoProcessorApp(root)
    root.mainloop()
