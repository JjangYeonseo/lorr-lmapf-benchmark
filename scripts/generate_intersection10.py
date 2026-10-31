"""Generate a deterministic 10-agent cross-intersection LMAPF scenario for LoRR 2026.

This is a *new scenario*, not a change to the official LoRR planner.
The scenario generator is pure Python stdlib. Grid coordinates are (row, col).
Each task has two errands and tasks are progressively revealed by LoRR.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / "scenarios" / "intersection_10"
WIDTH = HEIGHT = 13
GRID = ["@@@@@...@@@@@"] * 5 + ["............."] * 3 + ["@@@@@...@@@@@"] * 5
STARTS = [
    (0, 5), (0, 7), (1, 6),  # north approach
    (12, 5), (12, 7), (11, 6),  # south approach
    (5, 0), (7, 0),  # west approach
    (5, 12), (7, 12),  # east approach
]
ARM = {
    "N": [(1, 5), (2, 6), (3, 7), (4, 5), (4, 7)],
    "S": [(11, 5), (10, 6), (9, 7), (8, 5), (8, 7)],
    "W": [(5, 1), (6, 2), (7, 3), (5, 4), (7, 4)],
    "E": [(5, 11), (6, 10), (7, 9), (5, 8), (7, 8)],
}
# Deterministic cross-traffic schedule; no seed varies the map/task order in v0.2 design.
ROUTES = [
    ("W", "E"), ("E", "W"), ("N", "S"), ("S", "N"),
    ("W", "N"), ("E", "S"), ("N", "E"), ("S", "W"),
    ("N", "W"), ("S", "E"), ("W", "S"), ("E", "N"),
]
ERRANDS = [
    (ARM[a][(i // len(ROUTES)) % len(ARM[a])], ARM[b][(i + i // len(ROUTES)) % len(ARM[b])])
    for i, (a, b) in ((j, ROUTES[j % len(ROUTES)]) for j in range(48))
]

def linearize(point: tuple[int, int]) -> int:
    r, c = point
    assert 0 <= r < HEIGHT and 0 <= c < WIDTH and GRID[r][c] == ".", point
    return r * WIDTH + c


def create() -> None:
    assert len(GRID) == HEIGHT and all(len(row) == WIDTH for row in GRID)
    assert len(STARTS) == 10 and len(set(STARTS)) == 10
    SCENE.joinpath("maps").mkdir(parents=True, exist_ok=True)
    SCENE.joinpath("agents").mkdir(parents=True, exist_ok=True)
    SCENE.joinpath("tasks").mkdir(parents=True, exist_ok=True)
    SCENE.joinpath("maps", "intersection_10.map").write_text(
        "type octile\nheight 13\nwidth 13\nmap\n" + "\n".join(GRID) + "\n", encoding="utf-8"
    )
    SCENE.joinpath("agents", "intersection_10.agents").write_text(
        "# version for LoRR 2026\n10\n" + "\n".join(map(str, map(linearize, STARTS))) + "\n", encoding="utf-8"
    )
    SCENE.joinpath("tasks", "intersection_10.tasks").write_text(
        f"# version for LoRR 2026\n{len(ERRANDS)}\n" +
        "\n".join(",".join(str(linearize(point)) for point in task) for task in ERRANDS) + "\n",
        encoding="utf-8",
    )
    problem = {
        "mapFile": "maps/intersection_10.map",
        "agentFile": "agents/intersection_10.agents",
        "taskFile": "tasks/intersection_10.tasks",
        "teamSize": 10,
        "numTasksReveal": 1.5,
        "version": "2026 LoRR",
        "agentCounter": 3,
        "agentSize": 1.0,
        "delayConfig": {
            "seed": 0,
            "minDelay": 1,
            "maxDelay": 3,
            "eventModel": "bernoulli",
            "pDelay": 0.0,
            "durationModel": "uniform",
            "gaussMeanRatio": 0.5,
            "gaussStdRatio": 0.22,
        },
    }
    SCENE.joinpath("problem.json").write_text(json.dumps(problem, indent=2) + "\n", encoding="utf-8")
    print(f"Generated 10-agent intersection map and 48 tasks at {SCENE}")


if __name__ == "__main__":
    create()
