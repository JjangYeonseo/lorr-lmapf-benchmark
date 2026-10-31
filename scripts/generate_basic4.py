"""Deterministic, tiny four-robot LoRR 2026 smoke-test dataset.

No external Python packages are needed. Coordinates are 0-indexed (row,col),
linearized as row * width + col. The official competition formats are used.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / "scenarios" / "basic_4"
WIDTH = 9
GRID = [
    ".........",
    ".@.....@.",
    ".........",
    "...@.@...",
    ".........",
    "...@.@...",
    ".........",
    ".@.....@.",
    ".........",
]
STARTS = [(0, 0), (0, 8), (8, 0), (8, 8)]
ERRANDS = [
    ((2, 2), (6, 6)), ((2, 6), (6, 2)),
    ((6, 2), (2, 6)), ((6, 6), (2, 2)),
    ((0, 4), (8, 4)), ((4, 0), (4, 8)),
    ((2, 4), (6, 4)), ((4, 2), (4, 6)),
    ((8, 4), (0, 4)), ((4, 8), (4, 0)),
    ((6, 4), (2, 4)), ((4, 6), (4, 2)),
    ((2, 2), (4, 8)), ((2, 6), (4, 0)),
    ((6, 2), (0, 4)), ((6, 6), (8, 4)),
]


def lin(p: tuple[int, int]) -> int:
    r, c = p
    assert 0 <= r < len(GRID) and 0 <= c < WIDTH and GRID[r][c] == ".", p
    return r * WIDTH + c


def create() -> None:
    assert all(len(r) == WIDTH for r in GRID)
    assert len(set(STARTS)) == 4
    (SCENE / "maps").mkdir(parents=True, exist_ok=True)
    (SCENE / "agents").mkdir(parents=True, exist_ok=True)
    (SCENE / "tasks").mkdir(parents=True, exist_ok=True)
    (SCENE / "maps" / "basic_4.map").write_text(
        f"type octile\nheight {len(GRID)}\nwidth {WIDTH}\nmap\n" + "\n".join(GRID) + "\n",
        encoding="utf-8",
    )
    (SCENE / "agents" / "basic_4.agents").write_text(
        "# version for LoRR 2026\n" + str(len(STARTS)) + "\n"
        + "\n".join(str(lin(s)) for s in STARTS) + "\n",
        encoding="utf-8",
    )
    (SCENE / "tasks" / "basic_4.tasks").write_text(
        "# version for LoRR 2026\n" + str(len(ERRANDS)) + "\n"
        + "\n".join(",".join(str(lin(p)) for p in task) for task in ERRANDS) + "\n",
        encoding="utf-8",
    )
    task = {
        "mapFile": "maps/basic_4.map",
        "agentFile": "agents/basic_4.agents",
        "taskFile": "tasks/basic_4.tasks",
        "teamSize": 4,
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
    (SCENE / "problem.json").write_text(json.dumps(task, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated 4-agent LoRR 2026 test: {SCENE}")


if __name__ == "__main__":
    create()
