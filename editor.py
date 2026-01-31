import time
from dataclasses import dataclass
from typing import List, Optional

class Node:
    __slots__ = ("c", "p", "n")
    def __init__(self, ch: str):
        self.c = ch; self.p = None; self.n = None

@dataclass
class Action:
    typ: str
    nodes: List[Node]
    anchor: Optional[Node]
    ts: float

class Editor:
    def __init__(self, batch_timeout: float = 2.0):
        self.head = Node("")
        self.cursor_prev: Node = self.head
        self.undo_stack: List[Action] = []
        self.redo_stack: List[Action] = []
        self._batch: Optional[Action] = None
        self._last = 0.0
        self.timeout = batch_timeout

    def _ins_after(self, prev: Node, node: Node):
        nxt = prev.n
        node.p, node.n = prev, nxt
        prev.n = node
        if nxt: nxt.p = node

    def _unlink(self, node: Node):
        p, n = node.p, node.n
        if p: p.n = n
        if n: n.p = p
        node.p = node.n = None

    def _commit(self):
        if not self._batch: return
        if self._batch.typ == "del":
            self._batch.anchor = self.cursor_prev
        if self._batch.nodes:
            self.undo_stack.append(self._batch)
            self.redo_stack.clear()
        self._batch = None

    def _extend_ok(self, typ: str, ins_anchor: Optional[Node]) -> bool:
        return (self._batch is not None and
                self._batch.typ == typ and
                time.time() - self._last <= self.timeout and
                (typ != "ins" or self._batch.anchor is ins_anchor))

    def write(self, ch: str):
        if not ch: return
        prev = self.cursor_prev
        n = Node(ch)
        self._ins_after(prev, n)
        self.cursor_prev = n
        now = time.time()
        if self._extend_ok("ins", prev):
            self._batch.nodes.append(n)
        else:
            self._commit()
            self._batch = Action("ins", [n], prev, now)
        self._last = now

    def delete(self):
        if self.cursor_prev is self.head: return
        node = self.cursor_prev
        if self._batch and self._batch.typ == "del" and time.time() - self._last <= self.timeout:
            self._batch.nodes.insert(0, node)
        else:
            self._commit()
            self._batch = Action("del", [node], None, time.time())
        self._unlink(node)
        self.cursor_prev = node.p if node.p is not None else self.head
        self._last = time.time()

    def move_left(self):
        self._commit()
        if self.cursor_prev is not self.head:
            self.cursor_prev = self.cursor_prev.p if self.cursor_prev.p is not None else self.head

    def move_right(self):
        self._commit()
        nxt = self.cursor_prev.n
        if nxt: self.cursor_prev = nxt

    def undo(self):
        self._commit()
        if not self.undo_stack: return
        act = self.undo_stack.pop()
        if act.typ == "ins":
            for n in reversed(act.nodes):
                self._unlink(n)
            self.cursor_prev = act.anchor if act.anchor is not None else self.head
        else:
            cur = act.anchor if act.anchor is not None else self.head
            for n in act.nodes:
                self._ins_after(cur, n)
                cur = n
            self.cursor_prev = cur
        self.redo_stack.append(act)

    def redo(self):
        self._commit()
        if not self.redo_stack: return
        act = self.redo_stack.pop()
        if act.typ == "ins":
            cur = act.anchor if act.anchor is not None else self.head
            for n in act.nodes:
                self._ins_after(cur, n)
                cur = n
            self.cursor_prev = cur
        else:
            for n in act.nodes:
                self._unlink(n)
            self.cursor_prev = act.anchor if act.anchor is not None else self.head
        self.undo_stack.append(act)

    def display(self) -> str:
        out = []
        cur = self.head.n
        insert_at = self.cursor_prev.n if self.cursor_prev else None
        while cur:
            if cur is insert_at:
                out.append("|")
            out.append(cur.c)
            cur = cur.n
        if insert_at is None:
            out.append("|")
        return "".join(out)