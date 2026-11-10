from pathlib import Path
from collections import deque
import json, random

N = 17
ROOT = Path('scenarios/topology_pilot_v1')

def grid():
    return [['@'] * N for _ in range(N)]

def free(g, r, c):
    g[r][c] = '.'

def maze(bays):
    g = grid()
    # Three one-cell-wide aisles connected into a snake
    for r in (3, 8, 13):
        for c in range(1, 16):
            free(g, r, c)
    for r in range(3, 9):
        free(g, r, 1)
    for r in range(8, 14):
        free(g, r, 15)

    if bays:
        # Side pockets where robots may yield
        for r, c in [
            (2, 5), (2, 10),
            (7, 6), (7, 11),
            (12, 5), (12, 10)
        ]:
            free(g, r, c)
    return g

def warehouse(cut):
    g = grid()
    # Five vertical aisles
    for r in range(2, 15):
        for c in (2, 5, 8, 11, 14):
            free(g, r, c)

    # Three horizontal cross-aisles
    for c in range(2, 15):
        for r in (2, 8, 14):
            free(g, r, c)

    if cut:
        # Remove some upper cross-aisle connections
        for c in (6, 7, 12, 13):
            g[2][c] = '@'
    return g

def tasks_from(left, right):
    rng = random.Random(20261110)
    return [
        (a, b) if i % 2 == 0 else (b, a)
        for i in range(48)
        for a, b in [(rng.choice(left), rng.choice(right))]
    ]

def validate(g, starts, tasks):
    assert len(starts) == 10
    assert len(set(starts)) == 10
    assert len(tasks) == 48

    cells = {
        (r, c) for r in range(N) for c in range(N)
        if g[r][c] == '.'
    }
    assert all(p in cells for p in starts)
    assert all(p in cells for task in tasks for p in task)

    seen = {starts[0]}
    q = deque(seen)

    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            v = (r + dr, c + dc)
            if v in cells and v not in seen:
                seen.add(v)
                q.append(v)

    assert seen == cells, "Map must be fully connected"
    return len(cells)

def save(name, g, starts, tasks):
    count = validate(g, starts, tasks)
    base = ROOT / name

    for folder in ('maps', 'agents', 'tasks'):
        (base / folder).mkdir(parents=True, exist_ok=True)

    idx = lambda p: p[0] * N + p[1]

    (base / 'maps/map.map').write_text(
        'type octile\nheight 17\nwidth 17\nmap\n'
        + '\n'.join(''.join(row) for row in g) + '\n',
        encoding='utf-8'
    )

    (base / 'agents/robots.agents').write_text(
        '# version for LoRR 2026\n10\n'
        + '\n'.join(map(str, map(idx, starts))) + '\n',
        encoding='utf-8'
    )

    (base / 'tasks/tasks.tasks').write_text(
        '# version for LoRR 2026\n48\n'
        + '\n'.join(f'{idx(a)},{idx(b)}' for a,b in tasks)
        + '\n',
        encoding='utf-8'
    )

    config = {
        'mapFile': 'maps/map.map',
        'agentFile': 'agents/robots.agents',
        'taskFile': 'tasks/tasks.tasks',
        'teamSize': 10,
        'numTasksReveal': 1.5,
        'version': '2026 LoRR',
        'agentCounter': 3,
        'agentSize': 1.0,
        'delayConfig': {
            'seed': 0,
            'minDelay': 1,
            'maxDelay': 3,
            'eventModel': 'bernoulli',
            'pDelay': 0.0,
            'durationModel': 'uniform',
            'gaussMeanRatio': 0.5,
            'gaussStdRatio': 0.22
        }
    }

    (base / 'problem.json').write_text(
        json.dumps(config, indent=2) + '\n',
        encoding='utf-8'
    )

    print(f'PASS {name}: free={count}, robots=10, tasks=48, connected')

# Maze: paired layouts
ms = [(3,c) for c in (2,4,6,8,10)] + \
     [(13,c) for c in (4,6,8,10,12)]

mt = tasks_from(
    [(3,c) for c in (3,5,7,9,11,13)],
    [(13,c) for c in (3,5,7,9,11,13)]
)

save('maze_plain', maze(False), ms, mt)
save('maze_bays', maze(True), ms, mt)

# Warehouse: paired layouts
ws = [
    (3,2), (4,5), (3,8), (4,11), (3,14),
    (12,2), (13,5), (12,8), (13,11), (12,14)
]

wt = tasks_from(
    [(2,c) for c in (2,5,8,11,14)],
    [(14,c) for c in (2,5,8,11,14)]
)

save('warehouse_open', warehouse(False), ws, wt)
save('warehouse_cut', warehouse(True), ws, wt)

# Confirm exact same starts and tasks within pairs
for a,b in [
    ('maze_plain','maze_bays'),
    ('warehouse_open','warehouse_cut')
]:
    for f in ['agents/robots.agents','tasks/tasks.tasks']:
        assert (ROOT/a/f).read_bytes() == (ROOT/b/f).read_bytes()

print('PASS: Identical starts and tasks within each pair.')
