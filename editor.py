import time
from dataclasses import dataclass
from typing import List, Optional


class Node:
    __slots__ = ("c", "p", "n")

    def __init__(self, ch: str):
        self.c = ch
        self.p = None
        self.n = None


@dataclass
class Action:
    typ: str
    nodes: List[Node]
    anchor: Optional[Node]
    ts: float


class Editor:
    def __init__(self, batch_timeout: float = 2.0):
        self.head = Node("")
        self.cursor_prev = self.head
        self.undo_stack: List[Action] = []
        self.redo_stack: List[Action] = []
        self._batch: Optional[Action] = None
        self._last = 0.0
        self.timeout = batch_timeout

    def _ins_after(self, prev: Node, node: Node):
        nxt = prev.n
        node.p, node.n = prev, nxt
        prev.n = node
        if nxt:
            nxt.p = node

    def _unlink(self, node: Node):
        p, n = node.p, node.n
        if p:
            p.n = n
        if n:
            n.p = p
        node.p = node.n = None

    def _extend_ok(self, typ: str) -> bool:
        return (
            self._batch is not None
            and self._batch.typ == typ
            and time.time() - self._last <= self.timeout
        )

    def _commit(self):
        if not self._batch:
            return

        if self._batch.typ == "del":
            self._batch.anchor = self.cursor_prev

        if self._batch.nodes:
            self.undo_stack.append(self._batch)
            self.redo_stack.clear()

        self._batch = None

    def write(self, ch: str):
        if not ch:
            return

        prev = self.cursor_prev
        node = Node(ch)
        self._ins_after(prev, node)
        self.cursor_prev = node

        now = time.time()
        if self._extend_ok("ins"):
            self._batch.nodes.append(node)
        else:
            self._commit()
            self._batch = Action("ins", [node], prev, now)

        self._last = now

    def delete(self):
        if self.cursor_prev is self.head:
            return

        node = self.cursor_prev
        now = time.time()

        if self._extend_ok("del"):
            self._batch.nodes.insert(0, node)
        else:
            self._commit()
            self._batch = Action("del", [node], None, now)

        self._unlink(node)
        self.cursor_prev = node.p if node.p else self.head
        self._last = now

    def move_left(self):
        self._commit()
        if self.cursor_prev is not self.head:
            self.cursor_prev = self.cursor_prev.p or self.head

    def move_right(self):
        self._commit()
        if self.cursor_prev.n:
            self.cursor_prev = self.cursor_prev.n

    def undo(self):
        self._commit()
        if not self.undo_stack:
            return

        act = self.undo_stack.pop()
        if act.typ == "ins":
            for n in reversed(act.nodes):
                self._unlink(n)
            self.cursor_prev = act.anchor or self.head
        else:
            cur = act.anchor or self.head
            for n in act.nodes:
                self._ins_after(cur, n)
                cur = n
            self.cursor_prev = cur

        self.redo_stack.append(act)

    def redo(self):
        self._commit()
        if not self.redo_stack:
            return

        act = self.redo_stack.pop()
        if act.typ == "ins":
            cur = act.anchor or self.head
            for n in act.nodes:
                self._ins_after(cur, n)
                cur = n
            self.cursor_prev = cur
        else:
            for n in act.nodes:
                self._unlink(n)
            self.cursor_prev = act.anchor or self.head

        self.undo_stack.append(act)

    def display(self) -> str:
        out = []
        cur = self.head.n
        insert_at = self.cursor_prev.n

        while cur:
            if cur is insert_at:
                out.append("|")
            out.append(cur.c)
            cur = cur.n

        if insert_at is None:
            out.append("|")

        return "".join(out)
