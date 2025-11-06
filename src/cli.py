from src.trie import Trie

def run_cli(commands: str):
    t = Trie()
    out = []
    for line in commands.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        cmd = parts[0].lower()
        if cmd == "load":
            path = parts[1]
            with open(path) as f:
                for l in f:
                    word, freq = l.strip().split(",")
                    t.insert(word, float(freq))
        elif cmd == "contains":
            word = parts[1]
            out.append("YES" if t.contains(word) else "NO")
        elif cmd == "complete":
            prefix = parts[1]
            k = int(parts[2])
            out.append(" ".join(t.complete(prefix, k)))
        elif cmd == "remove":
            word = parts[1]
            out.append("OK" if t.remove(word) else "MISS")
        elif cmd == "stats":
            words, height, nodes = t.stats()
            out.append(f"{words} {height} {nodes}")
        elif cmd == "quit":
            break
    return out
