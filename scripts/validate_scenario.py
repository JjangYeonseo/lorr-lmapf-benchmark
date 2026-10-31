"""Validate LoRR input artifacts without needing Docker or POGEMA."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "scenarios" / "basic_4"
conf = json.loads((D / "problem.json").read_text(encoding="utf-8"))
assert conf["teamSize"] == 4
assert conf["version"] == "2026 LoRR"
map_lines = (D / conf["mapFile"]).read_text(encoding="utf-8").splitlines()
assert map_lines[:4] == ["type octile", "height 9", "width 9", "map"]
rows = map_lines[4:]
assert len(rows) == 9 and all(len(x) == 9 for x in rows)
for k in ("agentFile", "taskFile"):
    lines = (D / conf[k]).read_text(encoding="utf-8").splitlines()
    assert lines[0] == "# version for LoRR 2026"
    assert int(lines[1]) == len(lines) - 2
    if k == "agentFile":
        assert int(lines[1]) == 4
    else:
        assert int(lines[1]) >= 4
    for value in lines[2:]:
        for piece in value.split(","):
            loc = int(piece)
            r, c = divmod(loc, 9)
            assert 0 <= r < 9 and 0 <= c < 9 and rows[r][c] == ".", (k, loc)
print("PASS: 4-agent input schema, map, starts and tasks (static check)")
