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

A small command-line browser tab manager implemented in Python. It implements a circular doubly-linked list of tabs and supports grouping, LRU-based automatic closing when exceeding a maximum number of tabs, session snapshots/restores, duplicate-pruning, and simple tab navigation.

This README describes how to run and use the manager, the available commands, design notes, limitations, and suggestions for improvement.

## Features

- Open and close tabs (with optional groups)
- Circular navigation (next / previous)
- Switch directly to a tab by ID
- LRU enforcement: automatically close least-recently-used tab when exceeding max tabs
- Snapshot and restore session state
- Prune duplicate URLs, keeping the most recently active one
- Simple status listing including tab groups

## Requirements

- Python 3.7+

No third-party packages required.

## Running

Run the manager from the repo root:

```bash
python BrowserTabManager.py
```

You will see a prompt (`>`) to enter commands.

## Commands

- OPEN <url> [group]  
  Open a new tab for the given URL. Optionally specify a group name.
  Example: `OPEN https://example.com work`

- CLOSE  
  Close the currently active tab.

- NEXT  
  Move to the next tab (circular).

- PREV  
  Move to the previous tab (circular).

- SWITCH <tab_id>  
  Switch directly to the tab with the given tab id (e.g., `T1`, `T2`).

- SNAPSHOT  
  Save a deep-copied snapshot of the current session (tabs, groups, current position).

- RESTORE  
  Restore the last saved snapshot.

- PRUNE  
  Remove duplicate tabs that share the same URL, keeping the most recently active tab.

- STATUS  
  Print all open tabs and groups. The active tab is marked with `*`.

- (CTRL+C or CTRL+D)  
  Exit the program.

## Example session

```
> OPEN https://example.com
Tab T1 opened: https://example.com
> OPEN https://example.org work
Tab T2 opened: https://example.org (Group: work)
> OPEN https://example.com
Tab T3 opened: https://example.com
> STATUS
Tabs:
  T1 | https://example.com | Group: None
  * T3 | https://example.com | Group: None
  T2 | https://example.org | Group: work
Groups: {'work': ['T2']}
> PRUNE
Removed duplicate tab T1
Remaining: 2 tabs.
> SNAPSHOT
Session saved (2 tabs).
> CLOSE
T3 closed.
> RESTORE
Session restored (2 tabs).
> STATUS
Tabs:
* T3 | https://example.com | Group: None
  T2 | https://example.org | Group: work
Groups: {'work': ['T2']}
```
