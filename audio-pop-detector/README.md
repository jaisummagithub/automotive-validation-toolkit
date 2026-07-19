# Audio Pop Sound Detector

A desktop GUI tool that loads an audio recording, visualises its waveform, and automatically detects **"pop" sounds** — samples whose amplitude exceeds a user-defined threshold — then maps each detected event to a real-world timestamp.

Built with Python + Tkinter, using **librosa** for audio handling and **matplotlib** for visualisation. Ships with a Cython variant and a PyInstaller build spec for producing a standalone executable.

---

## What it does

1. **Load audio** — supports `.wav`, `.mp3`, and `.m4a`. Audio is resampled to **11,025 Hz** and read in **600-second chunks** so that very long recordings can be processed without exhausting memory.
2. **Recording timestamp** — prompts for the recording's real start date & time (defaults to now), so every detected event can be reported as an **absolute timestamp**, not just an offset.
3. **Waveform display** — plots amplitude vs. time in an embedded matplotlib canvas, complete with a navigation toolbar (zoom/pan) and a progress bar during rendering.
4. **Pop detection (parallel)** — the signal is split into chunks and processed concurrently via a `ThreadPoolExecutor`. Any sample with `|amplitude| > threshold` is flagged. Detected events are de-duplicated into **0.5-second buckets** to avoid counting a single pop many times.
5. **Adjustable sensitivity** — an **Amplitude Threshold** slider (range 0–1, default **0.4**) controls detection sensitivity.
6. **Results** — detected pops are:
   - listed in a table (Index, Time in seconds, Absolute Time),
   - marked on the waveform with red dashed vertical lines,
   - written to a timestamped `.asc` log file created next to the source recording.

---

## Requirements

- **Python 3.x**
- Third-party packages:
  - `librosa` — audio loading & duration
  - `numpy` — signal processing
  - `matplotlib` — waveform plotting
  - `tkinter` — GUI (standard library)

```bash
pip install librosa numpy matplotlib
```

---

## Usage

### From source
```bash
python audio_analyzer.py
```

### Steps
1. Launch the app.
2. Click **Load Audio File** and choose a `.wav` / `.mp3` / `.m4a` recording.
3. Enter or confirm the recording's **start date & time** (used for absolute timestamps).
4. Optionally adjust the **Amplitude Threshold** slider.
5. Click **Detect Pop Sound**.
6. Review results in the table and on the highlighted waveform. A `.asc` log is saved automatically.

### Output log
A file named `<audio>__pop_log_<YYYYMMDD_HHMMSS>.asc` is created alongside the input audio, with one line per detected pop:
```
Pop 1,   Time (s) = 12.50,   Absolute Time = 14/06/2024 10:32:12
```

---

## Building

### Cython extension (performance)
`audio_analyzer.pyx` is a Cython version of the detector. Compile it in place with:
```bash
python setup.py build_ext --inplace
```
This uses `cythonize` with `language_level=3` and includes NumPy headers. `audio_analyzer.c` is the generated C output.

### Windows executable (PyInstaller)
`audio_analyzer.spec` is a PyInstaller build spec. Produce a standalone console executable with:
```bash
pyinstaller audio_analyzer.spec
```
The spec builds a single `audio_analyzer` binary with UPX compression enabled.

---

## How it works (technical notes)

- **Chunked loading** (`load_audio_in_chunks`) streams the file in 10-minute segments and drives the first half of the progress bar, keeping memory bounded for long recordings.
- **Parallel detection** (`detect_pop_sound_parallel`) fans chunks out to worker threads; each returns the times where the amplitude threshold was exceeded.
- **Bucketing** collapses raw detections into unique 0.5-second slots, giving a stable pop count regardless of how many raw samples exceeded the threshold within that window.
- **Absolute time mapping** adds each pop's offset to the user-supplied recording start time via `timedelta`.
- **Threaded UI** — audio loading, plotting, and detection each run on background threads so the Tkinter window stays responsive.

## Files

| File | Description |
|------|-------------|
| `audio_analyzer.py` | Main application (Python). |
| `audio_analyzer.pyx` | Cython source variant. |
| `audio_analyzer.c` | Generated C from the Cython build. |
| `setup.py` | Cython build script. |
| `audio_analyzer.spec` | PyInstaller build spec. |

## Limitations

- Sampling rate is fixed at 11,025 Hz — adequate for pop/transient detection, not for high-fidelity spectral analysis.
- Detection is purely amplitude-threshold based; it does not distinguish pop type or frequency content.
- The recording start time must be entered manually (it is not read from file metadata).
