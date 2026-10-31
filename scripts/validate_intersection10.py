"""Static validation for 10-agent LoRR cross-intersection input."""
from __future__ import annotations
from collections import deque
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / "scenarios" / "intersection_10"
problem = json.loads((SCENE / "problem.json").read_text(encoding="utf-8"))
assert problem["version"] == "2026 LoRR"
assert problem["teamSize"] == 10
assert problem["agentCounter"] == 3
assert problem["delayConfig"]["pDelay"] == 0
raw_map = (SCENE / problem["mapFile"]).read_text(encoding="utf-8").splitlines()
assert raw_map[:4] == ["type octile", "height 13", "width 13", "map"]
grid = raw_map[4:]
assert len(grid) == 13 and all(len(line) == 13 for line in grid)
assert all(set(line) <= {".", "@"} for line in grid)
assert sum(row.count(".") for row in grid) == 69  # three-cell-wide cross with center counted once

def read_positions(field):
    lines = (SCENE / problem[field]).read_text(encoding="utf-8").splitlines()
    assert lines[0] == "# version for LoRR 2026"
    count = int(lines[1]); assert len(lines[2:]) == count
    return [list(map(int, line.split(","))) for line in lines[2:]]

starts = read_positions("agentFile")
tasks = read_positions("taskFile")
assert len(starts) == 10 and all(len(s) == 1 for s in starts)
assert len({s[0] for s in starts}) == 10
assert len(tasks) == 48 and all(len(task) == 2 for task in tasks)
spots = [pos for row in starts + tasks for pos in row]
for idx in spots:
    r, c = divmod(idx, 13)
    assert 0 <= idx < 169 and grid[r][c] == ".", idx
# Check all starting points and destinations are mutually reachable in open floorplan.
start = (0, 5)
seen = {start}; queue = deque([start])
while queue:
    r,c = queue.popleft()
    for nr,nc in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)):
        if 0 <= nr < 13 and 0 <= nc < 13 and grid[nr][nc] == "." and (nr,nc) not in seen:
            seen.add((nr,nc)); queue.append((nr,nc))
assert len(seen) == 69, f"Disconnected floorplan: {len(seen)} / 69 reachable"
print("PASS: 13x13 cross intersection, 10 starts, 48 two-errand tasks, all reachable; pDelay=0")
