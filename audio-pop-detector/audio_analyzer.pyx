import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from datetime import datetime, timedelta
import librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import concurrent.futures
import threading
import os
import sys



class AudioPopDetector:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Pop Sound Detector")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window close

        # Frame for instructions
        self.instructions_frame = tk.Frame(self.root)
        self.instructions_frame.pack(pady=10)
        self.instructions_label = tk.Label(self.instructions_frame, text="Instructions: Load an audio file, set the amplitude threshold, and detect pop sounds.")
        self.instructions_label.pack()

        # Frame for audio controls
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(pady=10)

        # Load Audio Button
        self.load_button = tk.Button(self.controls_frame, text="Load Audio File", command=self.load_audio)
        self.load_button.grid(row=0, column=0, padx=10)

        # Detect Button
        self.detect_button = tk.Button(self.controls_frame, text="Detect Pop Sound", command=self.detect_pop_sound_parallel)
        self.detect_button.grid(row=0, column=1, padx=10)

        # Threshold Scale
        self.threshold_label = tk.Label(self.controls_frame, text="Amplitude Threshold")
        self.threshold_label.grid(row=1, column=0, padx=10)
        self.threshold_scale = tk.Scale(self.controls_frame, from_=0, to=1, resolution=0.01, orient="horizontal", length=300)
        self.threshold_scale.set(0.4)
        self.threshold_scale.grid(row=1, column=1, padx=10)

        # Frame for additional info
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=10)

        self.file_info_label = tk.Label(self.info_frame, text="Audio File Information:")
        self.file_info_label.pack()

        self.audio_duration_label = tk.Label(self.info_frame, text="Duration: N/A")
        self.audio_duration_label.pack()

        self.sampling_rate_label = tk.Label(self.info_frame, text="Sampling Rate: N/A")
        self.sampling_rate_label.pack()

        self.pop_count_label = tk.Label(self.info_frame, text="Detected Pops: N/A")
        self.pop_count_label.pack()

        # Filename Label
        self.file_name_label = tk.Label(self.info_frame, text="File Name: N/A")
        self.file_name_label.pack()

        # Canvas for matplotlib graph
        self.figure, self.ax = plt.subplots(figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack()

        # Add Navigation Toolbar
        self.toolbar_frame = tk.Frame(self.root)
        self.toolbar_frame.pack(pady=5, fill=tk.X)
        self.navigation_toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.navigation_toolbar.update()

        # Add canvas to toolbar frame
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Progress bars with labels
        self.graph_progress_frame = tk.Frame(self.root)
        self.graph_progress_frame.pack(pady=5)
        self.graph_progress_label = tk.Label(self.graph_progress_frame, text="Generating Graph:")
        self.graph_progress_label.pack(side=tk.LEFT)
        self.graph_progress_bar = ttk.Progressbar(self.graph_progress_frame, orient="horizontal", length=400, mode="determinate")
        self.graph_progress_bar.pack(side=tk.LEFT)

        # self.pop_progress_frame = tk.Frame(self.root)
        # self.pop_progress_frame.pack(pady=5)
        # self.pop_progress_label = tk.Label(self.pop_progress_frame, text="Detecting Pop Sounds:")
        # self.pop_progress_label.pack(side=tk.LEFT)
        # self.pop_progress_bar = ttk.Progressbar(self.pop_progress_frame, orient="horizontal", length=400, mode="determinate")
        # self.pop_progress_bar.pack(side=tk.LEFT)

        # Details panel for pop sounds
        self.details_frame = tk.Frame(self.root)
        self.details_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        self.details_label = tk.Label(self.details_frame, text="Detected Pop Sounds:")
        self.details_label.pack()

        self.details_tree = ttk.Treeview(self.details_frame, columns=("Index", "Time", "Absolute Time"), show="headings")
        self.details_tree.heading("Index", text="Index")
        self.details_tree.heading("Time", text="Time (s)")
        self.details_tree.heading("Absolute Time", text="Absolute Time")
        self.details_tree.pack(fill=tk.BOTH, expand=True)

        # Variables for audio data
        self.y = None
        self.sr = None
        self.file_path = None
        self.recording_datetime = None
        
        # For .asc file for logging
        self.log_file = None

    def load_audio(self):
        threading.Thread(target=self._load_audio, daemon=True).start()

    def _load_audio(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.m4a"),("All files", "*.*")])
        if self.file_path:
            # Prompt user for creation date and time
            self.recording_datetime = self.prompt_for_creation_datetime()
            
            if not self.recording_datetime:
                return  # Abort if no valid date and time is provided
            
            self.graph_progress_bar['value'] = 0
            self.root.update_idletasks()
            self.sr = 11025
            self.y = self.load_audio_in_chunks(self.file_path, self.sr)
            duration = librosa.get_duration(y=self.y, sr=self.sr)
            self.audio_duration_label.config(text=f"Duration: {duration:.2f} seconds")
            self.sampling_rate_label.config(text=f"Sampling Rate: {self.sr} Hz")
            self.file_name_label.config(text=f"File Name: {os.path.basename(self.file_path)}")
            if self.recording_datetime:
                self.file_info_label.config(text=f"Recording DateTime: {self.recording_datetime.strftime('%d/%m/%Y %H:%M:%S')}")
            threading.Thread(target=self.plot_waveform_with_progress, daemon=True).start()
        self.log_file = open(f"{self.file_path[:-4]}__pop_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.asc", "w")

    def prompt_for_creation_datetime(self):
        # Create a new top-level window for date and time entry
        dialog = tk.Toplevel(self.root)
        dialog.title("Enter Creation Date and Time")

        # Get current date and time
        now = datetime.now()
        day = now.strftime("%d")
        month = now.strftime("%m")
        year = now.strftime("%Y")
        hour = now.strftime("%H")
        minute = now.strftime("%M")
        second = now.strftime("%S")

        # Create a label for the date
        date_label = tk.Label(dialog, text="Enter Date (DD MM YYYY):")
        date_label.grid(row=0, column=0, padx=10, pady=5)

        # Create entry widgets for day, month, and year with current date
        self.day_entry = tk.Entry(dialog, width=5)
        self.day_entry.grid(row=0, column=1)
        self.day_entry.insert(0, day)
        
        self.month_entry = tk.Entry(dialog, width=5)
        self.month_entry.grid(row=0, column=2)
        self.month_entry.insert(0, month)
        
        self.year_entry = tk.Entry(dialog, width=7)
        self.year_entry.grid(row=0, column=3)
        self.year_entry.insert(0, year)

        # Create a label for the time
        time_label = tk.Label(dialog, text="Enter Time (HH:MM:SS):")
        time_label.grid(row=1, column=0, padx=10, pady=5)

        # Create entry widgets for hour, minute, and second with current time
        self.hour_entry = tk.Entry(dialog, width=5)
        self.hour_entry.grid(row=1, column=1)
        self.hour_entry.insert(0, hour)
        
        self.minute_entry = tk.Entry(dialog, width=5)
        self.minute_entry.grid(row=1, column=2)
        self.minute_entry.insert(0, minute)
        
        self.second_entry = tk.Entry(dialog, width=5)
        self.second_entry.grid(row=1, column=3)
        self.second_entry.insert(0, second)

        # Create a button to submit the date and time
        submit_button = tk.Button(dialog, text="Submit", command=lambda: self.submit_datetime(dialog))
        submit_button.grid(row=2, column=0, columnspan=4, pady=10)

        dialog.grab_set()
        self.root.wait_window(dialog)

        return self.recording_datetime

    def submit_datetime(self, dialog):
        try:
            day = int(self.day_entry.get())
            month = int(self.month_entry.get())
            year = int(self.year_entry.get())
            hour = int(self.hour_entry.get())
            minute = int(self.minute_entry.get())
            second = int(self.second_entry.get())
            self.recording_datetime = datetime(year, month, day, hour, minute, second)
            dialog.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "The date or time format is incorrect. Please enter valid integers.")

    def load_audio_in_chunks(self, file_path, sr):
        y = []
        total_length = librosa.get_duration(path=file_path)
        chunk_duration = 600
        chunk_samples = int(sr * chunk_duration)
        offset = 0

        while offset < total_length:
            chunk, _ = librosa.load(file_path, sr=sr, offset=offset, duration=chunk_duration)
            y.extend(chunk)
            offset += chunk_duration
            progress = min(50, (offset / total_length) * 50)
            self.graph_progress_bar['value'] = progress
            self.root.update_idletasks()

        return np.array(y)

    def plot_waveform_with_progress(self):
        if self.y is not None:
            self.ax.clear()
            times = np.arange(len(self.y)) / self.sr
            total_points = len(times)
            chunk_size = total_points // 100
            for i in range(0, total_points, chunk_size):
                self.ax.plot(times[i:i + chunk_size], self.y[i:i + chunk_size], color='blue')
                self.ax.set_xlabel('Time (s)')
                self.ax.set_ylabel('Amplitude')
                self.ax.set_title('Audio Amplitude Over Time')
                self.canvas.draw()
                progress = 50 + (i / total_points) * 50
                self.graph_progress_bar['value'] = progress
                self.root.update_idletasks()

            self.ax.legend()

    def detect_pop_in_chunk(self, chunk, start_idx):
        times = np.arange(start_idx, start_idx + len(chunk)) / self.sr
        threshold = self.threshold_scale.get()
        pop_indices = np.where(np.abs(chunk) > threshold)[0]
        return times[pop_indices]

    def detect_pop_sound_parallel(self):
        threading.Thread(target=self._detect_pop_sound_parallel, daemon=True).start()

    def _detect_pop_sound_parallel(self):
        chunk_duration = 600
        chunk_size = int(self.sr * chunk_duration)
        total_chunks = len(self.y) // chunk_size

        all_pop_times = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i in range(total_chunks + 1):
                start_idx = i * chunk_size
                end_idx = min((i + 1) * chunk_size, len(self.y))
                chunk = self.y[start_idx:end_idx]
                futures.append(executor.submit(self.detect_pop_in_chunk, chunk, start_idx))

            pop_count = 0
            for future in concurrent.futures.as_completed(futures):
                all_pop_times.extend(future.result())
                pop_count += len(future.result())
                if pop_count % 5 == 0:
                    progress = (pop_count / len(self.y)) * 100
                    # self.pop_progress_bar['value'] = min(progress, 100)
                    self.root.update_idletasks()

        pop_half_seconds = set(int(t // 0.5) * 0.5 for t in all_pop_times)
        self.pop_count_label.config(text=f"Detected Pops: {len(pop_half_seconds)}")
        self.update_details_panel(pop_half_seconds)
        self.highlight_pop_sounds(pop_half_seconds)

    def update_details_panel(self, pop_times):
        for item in self.details_tree.get_children():
            self.details_tree.delete(item)

        for idx, pop_time in enumerate(sorted(pop_times)):
            absolute_time = self.recording_datetime + timedelta(seconds=pop_time) if self.recording_datetime else None
            absolute_time_str = absolute_time.strftime('%d/%m/%Y %H:%M:%S') if absolute_time else "N/A"
            self.details_tree.insert("", "end", values=(idx + 1, f"{pop_time:.2f}", absolute_time_str))
            
            # Log the pop details into the .asc log file
            log_entry = f"Pop {idx + 1},            Time (s) = {pop_time:.2f},              Absolute Time = {absolute_time_str}\n"
            self.log_file.write(log_entry)
            self.log_file.flush()  # Ensure the data is written immediately to the file    

    def highlight_pop_sounds(self, pop_times):
        if self.y is not None:
            self.ax.clear()
            times = np.arange(len(self.y)) / self.sr
            self.ax.plot(times, self.y, label='Audio Waveform')

            for pop_time in pop_times:
                self.ax.axvline(x=pop_time, color='r', linestyle='--', label=f'Pop at {pop_time:.1f}s')

            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Amplitude')
            self.ax.set_title('Audio Amplitude Over Time with Pop Sounds Highlighted')
            self.ax.legend()
            self.canvas.draw()

    def on_closing(self):
        # Perform cleanup before closing
        if hasattr(self, 'log_file') and self.log_file:
            self.log_file.close()
        self.root.destroy()
        sys.exit()

    def __del__(self):
        if hasattr(self, 'log_file') and self.log_file:
            self.log_file.close()

# Create the main window
root = tk.Tk()
app = AudioPopDetector(root)
root.mainloop()
