import time
import copy

class Tab:
    def __init__(self, tab_id, url, group=None):
        self.tab_id = tab_id
        self.url = url
        self.group = group
        self.last_active = time.time()
        self.prev = None
        self.next = None

class BrowserManager:
    def __init__(self, max_tabs=10):
        self.head = None
        self.current = None
        self.tabs = {}           
        self.groups = {}         
        self.snapshots = []      
        self.max_tabs = max_tabs
        self.counter = 1

    def _add_tab(self, tab):
        if not self.head:
            self.head = tab
            tab.next = tab.prev = tab
            self.current = tab
        else:
            tail = self.head.prev
            tail.next = tab
            tab.prev = tail
            tab.next = self.head
            self.head.prev = tab
            self.current = tab

        self.tabs[tab.tab_id] = tab
        if tab.group:
            self.groups.setdefault(tab.group, []).append(tab.tab_id)

    def _remove_tab(self, tab):
        if tab.next == tab:
            self.head = self.current = None
        else:
            tab.prev.next = tab.next
            tab.next.prev = tab.prev
            if tab == self.head:
                self.head = tab.next
            if tab == self.current:
                self.current = tab.next

        self.tabs.pop(tab.tab_id, None)
        if tab.group and tab.tab_id in self.groups.get(tab.group, []):
            self.groups[tab.group].remove(tab.tab_id)

    def _enforce_lru(self):
        if len(self.tabs) <= self.max_tabs:
            return

        lru = min(self.tabs.values(), key=lambda t: t.last_active)
        print(f"LRU limit exceeded. Closing {lru.tab_id}")
        self._remove_tab(lru)

    def open(self, url, group=None):
        tab_id = f"T{self.counter}"
        self.counter += 1
        tab = Tab(tab_id, url, group)
        self._add_tab(tab)
        self._enforce_lru()
        print(f"Tab {tab_id} opened: {url}" + (f" (Group: {group})" if group else ""))

    def close(self):
        if not self.current:
            print("No tabs open.")
            return
        closed = self.current.tab_id
        self._remove_tab(self.current)
        print(f"{closed} closed.")

    def next(self):
        if self.current:
            self.current = self.current.next
            self.current.last_active = time.time()
            print(f"Active: {self.current.tab_id}")

    def prev(self):
        if self.current:
            self.current = self.current.prev
            self.current.last_active = time.time()
            print(f"Active: {self.current.tab_id}")

    def switch_tab(self, tab_id):
        tab = self.tabs.get(tab_id)
        if not tab:
            print("Tab not found.")
            return
        self.current = tab
        tab.last_active = time.time()
        print(f"Switched to {tab_id}")

    def snapshot(self):
        self.snapshots.append(copy.deepcopy(self))
        print(f"Session saved ({len(self.tabs)} tabs).")

    def restore(self):
        if not self.snapshots:
            print("No snapshot to restore.")
            return
        restored = self.snapshots.pop()
        self.__dict__ = restored.__dict__
        print(f"Session restored ({len(self.tabs)} tabs).")

    def prune(self):
        seen = {}
        removed = []

        for tab in list(self.tabs.values()):
            if tab.url in seen:
                older = seen[tab.url]
                newer = max(tab, older, key=lambda t: t.last_active)
                removed_tab = older if newer == tab else tab
                removed.append(removed_tab.tab_id)
                self._remove_tab(removed_tab)
                seen[tab.url] = newer
            else:
                seen[tab.url] = tab

        for t in removed:
            print(f"Removed duplicate tab {t}")
        print(f"Remaining: {len(self.tabs)} tabs.")

    def status(self):
        if not self.tabs:
            print("No open tabs.")
            return

        print("Tabs:")
        t = self.head
        while True:
            marker = "*" if t == self.current else " "
            print(f"{marker} {t.tab_id} | {t.url} | Group: {t.group}")
            t = t.next
            if t == self.head:
                break

        print("Groups:", self.groups)


def main():
    manager = BrowserManager(max_tabs=5)
    print("Browser Tab Manager started.")

    while True:
        cmd = input("> ").strip().split()
        if not cmd:
            continue

        c = cmd[0]

        if c == "OPEN":
            manager.open(cmd[1], cmd[2] if len(cmd) > 2 else None)
        elif c == "CLOSE":
            manager.close()
        elif c == "NEXT":
            manager.next()
        elif c == "PREV":
            manager.prev()
        elif c == "SWITCH":
            manager.switch_tab(cmd[1])
        elif c == "SNAPSHOT":
            manager.snapshot()
        elif c == "RESTORE":
            manager.restore()
        elif c == "PRUNE":
            manager.prune()
        elif c == "STATUS":
            manager.status()
        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
