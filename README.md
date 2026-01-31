# Simple Editor — Project 1 README

Small cursor-based editor with undo/redo and a tiny Tk GUI.

This repository contains three small problems/features contributed by team members. This README marks ownership for each part and provides brief usage instructions.

Ownership
- Editor (this part: `editor.py`, `tk_editor.py`, `test_run.py`) — implemented by: lisa-lilu
- Problem 41 — GPS Retracer (`gps_retracer.py`) — implemented by: essete7
- Problem 32 — Session-aware Browser Tab Manager — jose-19

---

## Editor (lisa-lilu)

Files
- `editor.py` — editor implementation
- `tk_editor.py` — simple Tkinter GUI demo
- `test_run.py` — reproducible script/test

How to run
- REPL:
  ```bash
  python editor.py
  ```
- Scripted test:
  ```bash
  python test_run.py
  ```
- GUI demo:
  ```bash
  python tk_editor.py
  ```
---

## GPS Retracer — Problem 41 (essete7)

GPS Retracer is a simple Python program that retraces a hiker’s path using a stack-based approach. The system records each movement action and then calculates the return path by reading the actions in reverse order and inverting direction changes. This project runs entirely in the terminal and demonstrates basic data structures and control flow in Python.

How it works
- Movement actions are stored in a stack (LIFO).
- The return path is calculated by processing the stack in reverse order and inverting directions:
  - `LEFT` → `RIGHT`
  - `RIGHT` → `LEFT`
  - `FWD <distance>` keeps the same distance (e.g., `FWD 50`).
- The output is a list of actions representing the path back to the start.

How to run
```bash
python gps_retracer.py
```
The sample usage in the module's `__main__` will execute automatically and display the calculated return path.

Example output
```
CALCULATE_RETURN
1. FWD 50
2. RIGHT
3. FWD 100
```

Files
- `gps_retracer.py` — contains the `GPSRetracer` class and terminal-based execution logic.

Tests
- You can add test cases using `unittest` or `pytest`.

To run tests with pytest:
```bash
pip install pytest
pytest -q
```

Requirements
- Python 3.x
- No external libraries required

---

# Browser Tab Manager

Simple CLI tab manager (Python). Uses a circular doubly‑linked list of tabs with optional groups, LRU auto‑close, in‑memory snapshots, and duplicate pruning.

Requirements
- Python 3.7+

Quick start
- Run: `python BrowserTabManager.py`
- Interactive prompt: enter commands below.

Commands (brief)
- OPEN <url> [group] — open a new tab
- CLOSE — close current tab
- NEXT / PREV — navigate circularly
- SWITCH <tab_id> — go to a tab (e.g., T1)
- SNAPSHOT / RESTORE — save/restore session (in memory)
- PRUNE — remove duplicate URLs (keep most recently active)
- STATUS — list tabs (active marked with *)