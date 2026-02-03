import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import subprocess
from tkinter import messagebox
import imageio_ffmpeg
import stat

class VideoProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SOP Video Processor")
        self.root.geometry("600x400")
        
        # 1. GET FFMPEG & FIX PERMISSIONS
        try:
            self.ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            
            # CRITICAL FIX: Grant execute permission to the engine
            st = os.stat(self.ffmpeg_path)
            os.chmod(self.ffmpeg_path, st.st_mode | stat.S_IEXEC)
            
            status_text = "System Ready"
            status_color = "green"
        except Exception as e:
            self.ffmpeg_path = None
            status_text = f"Error: Engine not found ({str(e)})"
            status_color = "red"

        # GUI Setup
        self.label = tk.Label(root, text="Drag & Drop Video Files Here", bg="lightgray")
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
        for f in files:
            self.process_video(f)

    def process_video(self, file_path):
        try:
            # Handle output filename
            directory = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            name, ext = os.path.splitext(filename)
            output_file = os.path.join(directory, f"{name}_processed.mp4")
            
            # Simple process command
            cmd = [self.ffmpeg_path, "-y", "-i", file_path, "-c", "copy", output_file]
            
            # Windows hide console logic
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTUPINFO.dwFlags
            
            subprocess.run(cmd, check=True, startupinfo=startupinfo)
            messagebox.showinfo("Success", f"Processed: {os.path.basename(output_file)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {str(e)}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = VideoProcessorApp(root)
    root.mainloop()
