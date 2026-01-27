from editor import Editor

e = Editor()
e.process("WRITE 'A'")
e.process("WRITE 'B'")
e.process("WRITE 'C'")
print(e.display())   # expected: ABC|
e.process("UNDO")
print(e.display())   # expected: |
e.proeditcess("REDO")
print(e.display())   # expected: ABC|
e.process("MOVE left")
print(e.display())   # expected: AB|C
e.process("DELETE")
print(e.display())   # expected: A|C
e.process("UNDO")
print(e.display())   # expected: AB|C