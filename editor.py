#!/usr/bin/env python3
import sys

class Editor:
    def __init__(self):
        self.left, self.right = [], []    # left (in order), right (stack: top is next char)
        self.undo, self.redo = [], []

    def write(self, ch):
        if not ch: return
        self.left.append(ch); self.redo.clear()
        self.undo.append(("ins", ch))

    def delete(self):
        if not self.left: return
        ch = self.left.pop(); self.redo.clear()
        self.undo.append(("del", ch))

    def move_left(self):
        if self.left: self.right.append(self.left.pop())

    def move_right(self):
        if self.right: self.left.append(self.right.pop())

    def undo_op(self):
        if not self.undo: return
        t, data = self.undo.pop()
        if t == "ins":
            for _ in data: 
                if self.left: self.left.pop()
        else:  # del
            for ch in data: self.left.append(ch)
        self.redo.append((t, data))

    def redo_op(self):
        if not self.redo: return
        t, data = self.redo.pop()
        if t == "ins":
            for ch in data: self.left.append(ch)
        else:
            for _ in data:
                if self.left: self.left.pop()
        self.undo.append((t, data))

    def display(self):
        return "".join(self.left) + "|" + "".join(reversed(self.right))

    def process(self, line):
        if not line: return
        cmd, *rest = line.strip().split(maxsplit=1)
        arg = rest[0] if rest else ""
        c = arg.strip()
        if cmd.upper() == "WRITE":
            if (c.startswith("'") and c.endswith("'")) or (c.startswith('"') and c.endswith('"')):
                c = c[1:-1]
            if c: self.write(c[0])
        elif cmd.upper() == "DELETE":
            self.delete()
        elif cmd.upper() == "MOVE":
            d = arg.lower().strip()
            self.move_left() if d=="left" else self.move_right()
        elif cmd.upper() == "UNDO":
            self.undo_op()
        elif cmd.upper() == "REDO":
            self.redo_op()
        elif cmd.upper() == "DISPLAY":
            print(self.display())
        elif cmd.upper() in ("EXIT","QUIT"):
            sys.exit(0)
        else:
            print("Unknown command")

def repl():
    e = Editor()
    print("Commands: WRITE <char>, DELETE, MOVE <left|right>, UNDO, REDO, DISPLAY, EXIT")
    try:
        while True:
            s = input("> ").strip()
            if not s: continue
            for part in s.split(";"):
                e.process(part.strip())
    except (EOFError, KeyboardInterrupt):
        print("\nBye")

if __name__ == "__main__":
    repl()