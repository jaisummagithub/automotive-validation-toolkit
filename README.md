# Automotive Validation Toolkit

A collection of desktop utilities built to support automotive validation, diagnostics, and test-data analysis workflows.

The toolkit currently contains two independent tools, each in its own folder with its own detailed documentation:

| Tool | Folder | Purpose |
|------|--------|---------|
| **DTC Parser** | [`dtc-parser/`](./dtc-parser) | Extracts and tabulates Diagnostic Trouble Codes (DTCs) from ECU diagnostic logs exported by a **Bosch UDS diagnostic tool**. |
| **Audio Pop Sound Detector** | [`audio-pop-detector/`](./audio-pop-detector) | Analyses audio recordings to detect amplitude "pop" events and timestamp them against real time. |

## Repository layout

```
automotive-validation-toolkit/
├── README.md                  ← you are here (overview)
├── dtc-parser/
│   ├── README.md              ← detailed DTC Parser docs
│   ├── DTC_PARSER.py          ← source
│   └── sample_logs/           ← synthetic example ECU diagnostic logs
└── audio-pop-detector/
    ├── README.md              ← detailed Audio Pop Detector docs
    ├── audio_analyzer.py      ← source (main)
    ├── audio_analyzer.pyx     ← Cython source
    ├── audio_analyzer.c       ← generated C (Cython)
    ├── setup.py               ← Cython build script
    └── audio_analyzer.spec    ← PyInstaller build spec
```

## Getting started

Each tool is self-contained. See the README inside each folder for full setup, requirements, usage, and build instructions:

- **DTC Parser →** [`dtc-parser/README.md`](./dtc-parser/README.md)
- **Audio Pop Sound Detector →** [`audio-pop-detector/README.md`](./audio-pop-detector/README.md)

## Common requirements

- **Python 3.x**
- Tool-specific Python packages are listed in each tool's README.

---

*Internal tooling for ECU diagnostic log analysis and audio anomaly detection.*
