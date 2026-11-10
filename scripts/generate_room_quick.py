from pathlib import Path
import json
import random

root = Path.cwd() / "scenarios" / "room_quick"
W = 17

starts = [
    (2,2), (4,3), (8,2), (12,3), (14,2),
    (2,14), (4,13), (8,14), (12,13), (14,14)
]

left = [
    (3,6), (5,5), (7,6),
    (9,5), (11,6), (13,5)
]

right = [
    (3,10), (5,11), (7,10),
    (9,11), (11,10), (13,11)
]

tasks = []

for i in range(48):
    a = left[(i // 2) % 6]
    b = right[((i // 2) * 5 + 1) % 6]
    tasks.append((a,b) if i % 2 == 0 else (b,a))

random.Random(20261110).shuffle(tasks)

def pos(p):
    return p[0] * W + p[1]

for width in (1,3):
    dest = root / f"door{width}"

    for sub in ("maps", "agents", "tasks"):
        (dest / sub).mkdir(parents=True, exist_ok=True)

    rows = []

    for r in range(W):
        if r in (0,16):
            rows.append("@" * W)
        else:
            door = "." if abs(r - 8) <= width // 2 else "@"
            rows.append("@" + "." * 7 + door + "." * 7 + "@")

    (dest / "maps" / "map.map").write_text(
        "type octile\nheight 17\nwidth 17\nmap\n"
        + "\n".join(rows) + "\n"
    )

    (dest / "agents" / "robots.agents").write_text(
        "# version for LoRR 2026\n10\n"
        + "\n".join(str(pos(p)) for p in starts) + "\n"
    )

    (dest / "tasks" / "tasks.tasks").write_text(
        "# version for LoRR 2026\n48\n"
        + "\n".join(
            f"{pos(a)},{pos(b)}" for a,b in tasks
        ) + "\n"
    )

    config = {
        "mapFile": "maps/map.map",
        "agentFile": "agents/robots.agents",
        "taskFile": "tasks/tasks.tasks",
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
            "gaussStdRatio": 0.22
        }
    }

    (dest / "problem.json").write_text(
        json.dumps(config, indent=2) + "\n"
    )

    print("Generated:", dest / "problem.json")

assert (
    (root / "door1" / "tasks" / "tasks.tasks").read_bytes()
    ==
    (root / "door3" / "tasks" / "tasks.tasks").read_bytes()
)

print("PASS: Identical tasks for both room layouts")
