import tkinter as tk
from editor import Editor

class EditorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Editor Demo")
        self.geometry("480x200")
        self.ed = Editor()

        self.display_var = tk.StringVar()
        tk.Label(self, textvariable=self.display_var, font=("Consolas", 14), anchor="w").pack(fill="x", padx=8, pady=8)

        ctrl_frame = tk.Frame(self)
        ctrl_frame.pack(fill="x", padx=8)

        self.char_entry = tk.Entry(ctrl_frame, width=4, font=("Consolas", 12))
        self.char_entry.grid(row=0, column=0, padx=4)
        tk.Button(ctrl_frame, text="Write", command=self.do_write).grid(row=0, column=1, padx=4)
        tk.Button(ctrl_frame, text="Delete", command=self.do_delete).grid(row=0, column=2, padx=4)
        tk.Button(ctrl_frame, text="Move←", command=self.do_left).grid(row=0, column=3, padx=4)
        tk.Button(ctrl_frame, text="Move→", command=self.do_right).grid(row=0, column=4, padx=4)
        tk.Button(ctrl_frame, text="Undo", command=self.do_undo).grid(row=0, column=5, padx=4)
        tk.Button(ctrl_frame, text="Redo", command=self.do_redo).grid(row=0, column=6, padx=4)
        tk.Button(ctrl_frame, text="Display", command=self.update_display).grid(row=0, column=7, padx=4)

        self.update_display()

    def do_write(self):
        ch = self.char_entry.get()
        if ch:
            self.ed.write(ch[0])
            self.char_entry.delete(0, "end")
            self.update_display()

    def do_delete(self):
        self.ed.delete()
        self.update_display()

    def do_left(self):
        self.ed.move_left()
        self.update_display()

    def do_right(self):
        self.ed.move_right()
        self.update_display()

    def do_undo(self):
        self.ed.undo()
        self.update_display()

    def do_redo(self):
        self.ed.redo()
        self.update_display()

    def update_display(self):
        self.display_var.set(self.ed.display())

if __name__ == "__main__":
    app = EditorGUI()
    app.mainloop()