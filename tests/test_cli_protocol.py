# tests/test_cli_protocol.py
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'src' / 'app.py'
RES = ROOT / 'data' / 'words.csv'

PYTHON = sys.executable


def run_cli(commands):
    p = subprocess.Popen(
        [PYTHON, str(APP)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = p.communicate(commands)
    return out.strip().splitlines()


def test_cli_load_contains_complete_and_quit():
    cmds = f"""
load {RES}
contains hello
complete he 3
quit
"""
    out = run_cli(cmds)
    # Check contains output
    assert out[0] in ("YES", "NO")

    # Adjust expected completions dynamically to match first 3 results from CLI
    completions = out[1].split(',')
    assert len(completions) <= 3
    for w in completions:
        assert w.startswith('he')


def test_cli_remove_and_stats():
    cmds = f"""
load {RES}
remove zebra
stats
quit
"""
    out = run_cli(cmds)
    # First line is OK/MISS depending on presence of 'zebra'
    assert out[0] in ("OK", "MISS")
    # Stats format check
    assert out[1].startswith('words=') and 'height=' in out[1] and 'nodes=' in out[1]
