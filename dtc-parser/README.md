# DTC Parser

A desktop GUI tool that scans a folder of ECU diagnostic logs, extracts every reported **Diagnostic Trouble Code (DTC)**, and presents the results in a sortable table.

Built with Python + Tkinter. Run directly from source (`DTC_PARSER.py`).

---

## Tool context — where the logs come from

The log files this parser consumes are produced by a **Bosch UDS diagnostic tool** — a dealer/engineering diagnostic system that communicates with vehicle ECUs over UDS.

Key characteristics of these logs:

- **Protocol:** UDS — Unified Diagnostic Services (ISO 14229) — transported over **CAN ISO-TP (ISO 15765)**.
- **Diagnostic services captured:** DTC reads, Data Identifier (DID) reads, software part-number reads, and Mode 6 MIDs.
- Captures typically include **before-run** and **after-run** DTC snapshots taken during vehicle testing/validation.

This parser targets the **`DTC_*.txt`** exports produced by that tool.

> **Note:** The sample logs in this repository are **synthetic** — they use generic ECU names and fabricated DTC codes/descriptions purely to demonstrate the expected file format. No real vehicle, diagnostic-database, or manufacturer data is included.

---

## What it does

1. **Folder scan** — you select a directory; the tool processes every file named `DTC_*.txt`.
2. **ECU identification** — for each log, a regular expression captures the **ECU name** and **ECU code** from the log's header block:
   ```
   Reading DTCs from <ECU Name>
       Filter set OK for ECU: <ECU Code>
   ```
3. **DTC extraction** — a second regex captures the number of DTCs the ECU reports and each **DTC code** (format `[A-Z][0-9]{6}`, e.g. `P012345`).
4. **Aggregation** — each finding is stored as:
   `(ECU Name, ECU Code, DTC Code, Occurrences, File Name, File Path)`
5. **Sorting** — results are ordered by file name, then by occurrence count (highest first).
6. **Display** — everything is shown in a scrollable `ttk.Treeview` table with columns for ECU Name, ECU Code, DTC Code, Occurrences, File Name and File Path.

---

## Requirements

- **Python 3.x** — uses only the standard library:
  - `os`, `re`, `tkinter` (with `ttk`, `filedialog`)

No third-party packages required.

---

## Usage

### From source
```bash
python DTC_PARSER.py
```

### Steps
1. Launch the app.
2. Click **Browse Folder**.
3. Select a directory that contains `DTC_*.txt` diagnostic logs.
4. The table populates automatically with all parsed DTCs, sorted by file and occurrence count.

---

## Input log format

The parser expects the plain-text `DTC_*.txt` diagnostic logs exported by a **Bosch UDS tool** — filenames start with `DTC_` and end with `.txt`. Each log contains ECU header blocks in the form:

```
Reading DTCs from <ECU Name>
    Filter set OK for ECU: <ECU_CODE>
    ...
    ECU Reports <N> DTCs   <DTCCODE> ( ...
```

- **ECU Name** — free text after "Reading DTCs from".
- **ECU Code** — alphanumeric token after "Filter set OK for ECU:".
- **DTC code** — one uppercase letter followed by six digits (e.g. `U101010`).
- **Occurrences** — the integer count reported before the DTC.

## Sample data

The [`sample_logs/`](./sample_logs) folder contains **synthetic** example captures that demonstrate the file format the parser expects:

- `DTC_SampleVehicle_BeforeRun.txt` — a clean before-run snapshot (no DTCs stored).
- `DTC_SampleVehicle_AfterRun.txt` — an after-run snapshot containing example DTCs across several ECUs.

All ECU names and DTC codes/descriptions in these files are fabricated for demonstration only.

---

## How it works (technical notes)

- **Regex-driven parsing** keeps the tool robust to surrounding log noise; only the ECU header and DTC-report patterns are matched.
- **DTC code pattern:** `ECU Reports\s+(\d+)\s+DTCs\s+([A-Z][0-9]{6})\s+[(]` — captures the occurrence count and the DTC code together.
- **Threaded-free, synchronous UI** — parsing runs on folder selection and repopulates the tree in place.
- The source file also retains earlier iterations of the parsing regex (commented out) documenting the evolution of the DTC-matching logic.

## Limitations

- Only files matching `DTC_*.txt` are parsed; other captures in the folder are ignored.
- The DTC code regex assumes the `[A-Z][0-9]{6}` format; codes in other formats won't match.
- Paths and display widths are tuned for a desktop screen (window is 1500×500).
