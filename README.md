# Simple Editor — Project 1 README

Small cursor-based editor with undo/redo and a tiny Tk GUI.

This repository contains three small problems/features contributed by team members. This README marks ownership for each part and provides brief usage instructions.

Ownership
- Editor (this part: `editor.py`, `tk_editor.py`, `test_run.py`) — implemented by: lisa-lilu
- Problem 41 — GPS Retracer (`gps_retracer.py`) — implemented by: essete7
- Problem 32 — Session-aware Browser Tab Manager (Java) — jose-19

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

## Session-aware Browser Tab Manager — Problem 32 (jose-19)

Session-aware Browser Tab Manager is a command-line Java program that manages browser tabs with features such as circular tab navigation, tab grouping, session snapshots for crash recovery, duplicate pruning, and LRU-based tab eviction. It demonstrates classic data structures and session management in Java.

Summary / Key Features
- Circular tab navigation (next/previous wraps around).
- Tab grouping for organizing related tabs.
- Session snapshots (stack) to save/restore sessions (crash recovery).
- Duplicate pruning (remove older duplicate URLs, keep most recent).
- LRU-based tab eviction (evict least recently used tabs when limits are reached).
- Command-line interface for interacting with the manager.

How to run
- Run from IntelliJ:
  - Open the project in IntelliJ IDEA
  - Run `Main.java` (entry point)

- Run from terminal (after compiling):
  ```bash
  javac -d out src/manager/*.java
  java -cp out manager.Main
  ```

Commands (CLI)
- `OPEN <url> [group]`   : Open a new tab (optional group)
- `CLOSE`                : Close current tab
- `NEXT`                 : Switch to next tab (circular)
- `PREV`                 : Switch to previous tab
- `SWITCH <tab_id>`      : Jump to a specific tab by id
- `SNAPSHOT`             : Save current session state
- `RESTORE`              : Restore last saved session
- `PRUNE`                : Remove duplicate URLs (keep most recent)
- `STATUS`               : Show all tabs and active tab

Data Structures Used
- Circular Doubly Linked List: tab navigation and ordering
- Stack: session snapshots (LIFO for save/restore)
- HashMap / ArrayList: tab lookup, grouping, and LRU tracking
- (Optional) Priority/linked structure for efficient LRU maintenance

Project Structure
- `src/manager/Main.java`               : CLI entry point
- `src/manager/BrowserManager.java`    : Core logic and operations
- `src/manager/Tab.java`               : Tab data structure
- `src/manager/SessionSnapshot.java`   : Session state container
- `out/`                               : (recommended) compiled classes

Example usage
- Open tabs and view status:
  ```
  > OPEN https://example.com
  > OPEN https://example.org work
  > STATUS
  Tab 1: https://example.com (active)
  Tab 2: https://example.org [group: work]
  ```
- Snapshot and restore:
  ```
  > SNAPSHOT
  Session saved
  > CLOSE
  > RESTORE
  Session restored, Tab 2 active
  ```

