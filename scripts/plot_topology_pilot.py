from pathlib import Path
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
import json, re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures" / "topology_pilot_v1"
OUT.mkdir(parents=True, exist_ok=True)

BLUE = "#1683C5"
ORANGE = "#E99738"
INK = "#1E293B"
MUTED = "#64748B"
DARK = "#475569"

def font(size, bold=False):
    names = (
        ["C:/Windows/Fonts/arialbd.ttf"] if bold
        else ["C:/Windows/Fonts/arial.ttf"]
    )
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()

def read_map(rel):
    base = ROOT / rel
    rows = (
        (base / "maps/map.map")
        .read_text(encoding="utf-8")
        .splitlines()[4:]
    )
    assert len(rows) == 17
    assert all(len(row) == 17 for row in rows)

    starts = [
        int(x) for x in
        (base / "agents/robots.agents")
        .read_text(encoding="utf-8")
        .splitlines()[2:]
    ]
    assert len(starts) == 10

    targets = set()
    task_lines = (
        (base / "tasks/tasks.tasks")
        .read_text(encoding="utf-8")
        .splitlines()[2:]
    )
    for line in task_lines:
        for value in line.split(","):
            targets.add(int(value))

    return rows, starts, targets

cases = [
    ("Room / 3-cell door", "scenarios/room_quick/door3"),
    ("Warehouse / Open", "scenarios/topology_pilot_v1/warehouse_open"),
    ("Maze / Plain", "scenarios/topology_pilot_v1/maze_plain"),
    ("Room / 1-cell door", "scenarios/room_quick/door1"),
    ("Warehouse / Cut", "scenarios/topology_pilot_v1/warehouse_cut"),
    ("Maze / Passing bays", "scenarios/topology_pilot_v1/maze_bays")
]

# Figure 1: Six topology maps
cell = 23
cw, ch = 452, 478
im = Image.new("RGB", (3*cw+40, 2*ch+135), "#EDF2F7")
d = ImageDraw.Draw(im)

d.text((32,17), "TOPOLOGY PILOT | 10 ROBOTS",
       font=font(30,True), fill=INK)
d.text((32,61),
       "Blue = robot starts | Orange = task waypoints | Dark = obstacles",
       font=font(17), fill=MUTED)

for k,(label,rel) in enumerate(cases):
    ri,ci = divmod(k,3)
    x,y = 20+ci*cw, 93+ri*ch
    d.rounded_rectangle(
        (x,y,x+cw-12,y+ch-11),
        radius=15, fill="white"
    )
    d.text((x+19,y+12),label,font=font(22,True),fill=INK)

    rows,starts,targets = read_map(rel)
    x0,y0 = x+24,y+54

    for r,line in enumerate(rows):
        for c,value in enumerate(line):
            color = "white" if value == "." else DARK
            d.rectangle(
                (x0+c*cell,y0+r*cell,
                 x0+(c+1)*cell-2,y0+(r+1)*cell-2),
                fill=color
            )

    for p in targets:
        r,c = divmod(p,17)
        px,py = x0+c*cell+cell//2,y0+r*cell+cell//2
        d.rectangle((px-4,py-4,px+4,py+4),fill=ORANGE)

    for agent,p in enumerate(starts):
        r,c = divmod(p,17)
        px,py = x0+c*cell+cell//2,y0+r*cell+cell//2
        d.ellipse(
            (px-9,py-9,px+9,py+9),
            fill=BLUE,outline="white"
        )
        d.text((px,py),str(agent),
               anchor="mm",font=font(11,True),fill="white")

    free = sum(v == "." for row in rows for v in row)
    d.text((x+22,y+451),
           f"Free cells: {free} | Agents: 10",
           font=font(15),fill=MUTED)

im.save(OUT/"topology_maps.png",optimize=True)

# Figure 2: Completed tasks from real JSON data
pairs = [
    ("ROOM", [
        ("3-cell doorway","results/room_quick/door3.json"),
        ("1-cell doorway","results/room_quick/door1.json")
    ]),
    ("WAREHOUSE", [
        ("Open lanes","results/topology_pilot_v1/warehouse_open.json"),
        ("Blocked lanes","results/topology_pilot_v1/warehouse_cut.json")
    ]),
    ("MAZE", [
        ("Plain","results/topology_pilot_v1/maze_plain.json"),
        ("Passing bays","results/topology_pilot_v1/maze_bays.json")
    ])
]

im = Image.new("RGB",(1280,710),"white")
d = ImageDraw.Draw(im)
d.text((45,30),"COMPLETED TASKS BY TOPOLOGY",
       font=font(32,True),fill=INK)
d.text((45,79),
       "LoRR 2026 | 10 robots | 360 ticks | 1 run per map",
       font=font(19),fill=MUTED)

for group,(family,entries) in enumerate(pairs):
    y0 = 145+group*178
    d.text((45,y0),family,font=font(22,True),fill=INK)

    for j,(label,rel) in enumerate(entries):
        data = json.loads((ROOT/rel).read_text(encoding="utf-8"))
        n = data["numTaskFinished"]
        y = y0+40+j*52
        d.text((60,y+6),label,font=font(18),fill=INK)

        bx = 305
        d.rectangle((bx,y,bx+800,y+36),fill="#EDF2F7")
        if n:
            d.rectangle(
                (bx,y,bx+n*25,y+36),
                fill=BLUE if j==0 else ORANGE
            )
        d.text((bx+n*25+12,y+2),
               str(n),font=font(24,True),fill=INK)

    if group < 2:
        d.line((45,y0+156,1220,y0+156),
               fill="#CBD5E1",width=2)

d.text((45,668),
       "Compare within map pairs; workloads differ across map families.",
       font=font(18),fill=MUTED)
im.save(OUT/"completed_tasks.png",optimize=True)

# Figure 3: Maze actual action distribution
im = Image.new("RGB",(1280,515),"white")
d = ImageDraw.Draw(im)
d.text((45,27),"MAZE EXECUTED ACTION DISTRIBUTION",
       font=font(29,True),fill=INK)
d.text((45,74),
       "From actualPaths | 10 robots x 360 ticks = 3,600 robot-ticks",
       font=font(18),fill=MUTED)

for i,(label,rel) in enumerate([
    ("Plain","results/topology_pilot_v1/maze_plain.json"),
    ("Passing bays","results/topology_pilot_v1/maze_bays.json")
]):
    data = json.loads((ROOT/rel).read_text(encoding="utf-8"))
    totals = Counter()

    for path in data["actualPaths"]:
        chunks = re.findall(
            r"\[\(([^)]*)\):\(([^)]*)\)\]",path
        )
        assert chunks, "Cannot decode actualPaths"

        for _,actions in chunks:
            for token in actions.split(","):
                action,count = token.strip().split()
                totals[action] += int(count)

    counts = [
        totals["W"],
        totals["F"],
        totals["R"]+totals["C"]
    ]
    assert sum(counts) == 3600

    y = 153+i*151
    d.text((45,y),label,font=font(23,True),fill=INK)
    d.text((45,y+41),
           f"Tasks finished: {data['numTaskFinished']}",
           font=font(17),fill=MUTED)

    x = 295
    for count,color in zip(
        counts,["#64748B",BLUE,ORANGE]
    ):
        width = round(860*count/3600)
        d.rectangle((x,y,x+width,y+53),fill=color)
        if width > 80:
            d.text(
                (x+width/2,y+27),
                f"{100*count/3600:.1f}%",
                anchor="mm",
                font=font(18,True),
                fill="white"
            )
        x += width

    d.text((1175,y+15),"3,600",font=font(18),fill=INK)

for j,(label,color) in enumerate([
    ("Wait (W)","#64748B"),
    ("Forward (F)",BLUE),
    ("Rotate (R+C)",ORANGE)
]):
    x = 310+j*220
    d.rectangle((x,462,x+23,485),fill=color)
    d.text((x+32,460),label,font=font(18),fill=INK)

im.save(OUT/"maze_actions.png",optimize=True)

for p in sorted(OUT.glob("*.png")):
    print(f"OK: {p.name} ({p.stat().st_size/1024:.1f} KB)")
