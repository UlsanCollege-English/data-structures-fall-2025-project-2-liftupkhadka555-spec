# src/trie.py

class TrieNode:
    __slots__ = ("children", "is_word", "freq")

    def __init__(self):
        self.children = {}
        self.is_word = False
        self.freq = 0.0

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self._words = 0
        self._nodes = 1

    def insert(self, word, freq):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
                self._nodes += 1
            node = node.children[ch]
        if not node.is_word:
            self._words += 1
        node.is_word = True
        node.freq = freq

    def remove(self, word):
        path = []
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            path.append((node, ch))
            node = node.children[ch]
        if not node.is_word:
            return False
        node.is_word = False
        node.freq = 0
        self._words -= 1
        # Optional: prune nodes with no children
        for parent, ch in reversed(path):
            child = parent.children[ch]
            if not child.children and not child.is_word:
                del parent.children[ch]
                self._nodes -= 1
            else:
                break
        return True

    def contains(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_word

    def complete(self, prefix, k):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]
        results = []

        def dfs(n, path):
            if n.is_word:
                results.append((path, n.freq))
            for c in n.children:
                dfs(n.children[c], path + c)

        dfs(node, prefix)
        results.sort(key=lambda x: (-x[1], x[0]))
        return [w for w, f in results[:k]]

    def stats(self):
        def height(node):
            if not node.children:
                return 1
            return 1 + max(height(child) for child in node.children.values())
        return self._words, height(self.root), self._nodes

    def items(self):
        results = []
        def dfs(n, path):
            if n.is_word:
                results.append((path, n.freq))
            for c in n.children:
                dfs(n.children[c], path + c)
        dfs(self.root, "")
        return results
