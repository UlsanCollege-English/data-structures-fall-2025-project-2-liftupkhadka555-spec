# src/app.py
import sys
from pathlib import Path
from trie import Trie

def main():
    trie = Trie()
    
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        if not parts:
            continue

        cmd = parts[0].lower()

        if cmd == "load" and len(parts) == 2:
            path = Path(parts[1])
            try:
                # Explicitly specify UTF-8 to avoid encoding errors
                with path.open(encoding="utf-8") as f:
                    for ln in f:
                        word, freq = ln.strip().split(',')
                        trie.insert(word, float(freq))
            except Exception as e:
                print(f"ERROR loading file: {e}")
        
        elif cmd == "contains" and len(parts) == 2:
            word = parts[1]
            print("YES" if trie.contains(word) else "NO")
        
        elif cmd == "complete" and len(parts) == 3:
            prefix = parts[1]
            try:
                k = int(parts[2])
            except ValueError:
                k = 0
            completions = trie.complete(prefix, k)
            print(','.join(completions))
        
        elif cmd == "remove" and len(parts) == 2:
            word = parts[1]
            print("OK" if trie.remove(word) else "MISS")
        
        elif cmd == "stats":
            words, height, nodes = trie.stats()
            print(f"words={words} height={height} nodes={nodes}")
        
        elif cmd == "quit":
            break

if __name__ == "__main__":
    main()
