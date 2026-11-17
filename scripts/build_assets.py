#!/usr/bin/env python3
"""Generates every SVG in assets/ (header, stack, project cards, site plaque).

Pure stdlib:  python3 scripts/build_assets.py
Each asset is self-contained (no JS, no external fonts) because GitHub renders
README images through <img>. Motion is CSS-only and switched off under
prefers-reduced-motion; the static frame is complete on its own.
"""
from __future__ import annotations

import json
import math
import pathlib
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

# --- tokens (mirror of the hexarch.me design system) -------------------------
THEMES = {
    "dark": dict(
        bg="#121311", surface="#1a1b19", surface2="#232422", border="#30322e",
        strong="#74776f", text="#ecebe6", text2="#b9b8b0", text3="#99988f",
        accent="#5cc8c0", ok="#8ccf6a", shade="#000000", shade_k=0.55,
        clay=("#93d2aa", "#66a985", "#467b5f"), gold=("#f0c35a", "#d9a53a", "#a87a1f"),
        ink=("#3a3d42", "#2b2e33", "#1e2024"), base=("#20211f", "#191a18", "#151614"),
        screen="#14201f",
    ),
    "light": dict(
        bg="#f6f5f1", surface="#ffffff", surface2="#ecebe6", border="#d6d4cc",
        strong="#85837a", text="#1b1b19", text2="#45443f", text3="#63615a",
        accent="#0a6a66", ok="#2f6f14", shade="#000000", shade_k=0.17,
        clay=("#8ccca4", "#61a480", "#43775b"), gold=("#eebf52", "#d39f33", "#a3761c"),
        ink=("#4a4d52", "#33363b", "#232529"), base=("#ffffff", "#e3e1d9", "#d2d0c7"),
        screen="#1d2b2a",
    ),
}
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
K = math.sin(math.radians(36))  # ground-plane squash of the site's overview camera

# Martian Mono (OFL), wght 700, outlines of the glyphs used in titles. 1000 upm, y down.
GLYPHS = json.loads((pathlib.Path(__file__).with_name("glyphs.json")).read_text())["glyphs"]


def mix(a: str, b: str, t: float) -> str:
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(pa, pb))


def n(v: float) -> str:
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def title(text: str, x: float, base: float, size: float, fill: str, rise: bool = True) -> str:
    """Display title set in outlines; letters rise from under the line mask once."""
    k = size / 1000
    adv = 700 * k * 0.98
    cid = "m" + "".join(c for c in text if c.isalnum())
    w = adv * len(text)
    out = [f'<clipPath id="{cid}"><rect x="{n(x - 4)}" y="{n(base - size * 0.86)}" width="{n(w + 8)}" height="{n(size * 1.1)}"/></clipPath>',
           f'<g clip-path="url(#{cid})" fill="{fill}">']
    for i, ch in enumerate(text):
        cls = f' class="rise" style="animation-delay:{i * 45}ms"' if rise else ""
        out.append(f'<g transform="translate({n(x + i * adv)} {n(base)}) scale({k:.4f})"><path{cls} d="{GLYPHS[ch]["d"]}"/></g>')
    out.append("</g>")
    return "".join(out)


BASE_CSS = """
.rise{animation:rise .8s cubic-bezier(.2,.9,.3,1) backwards}
@keyframes rise{from{transform:translateY(1150px)}}
.bob{animation:bob 5.6s ease-in-out infinite}
@keyframes bob{50%{transform:translateY(-4px)}}
.sh{transform-box:fill-box;transform-origin:center;animation:sh 5.6s ease-in-out infinite}
@keyframes sh{50%{transform:scale(.9)}}
.pulse{opacity:0;animation:pulse 9.6s linear infinite}
@keyframes pulse{0%{stroke-dashoffset:0;opacity:0}2%{opacity:1}17%{opacity:1}20%{stroke-dashoffset:-92;opacity:0}100%{stroke-dashoffset:-92;opacity:0}}
.flash{opacity:0;transform-box:fill-box;transform-origin:center;animation:flash 9.6s ease-out infinite}
@keyframes flash{0%,18%{opacity:0;transform:scale(.8)}21%{opacity:.9}34%{opacity:0;transform:scale(1.5)}100%{opacity:0}}
.timer{animation:timer 9.6s linear infinite}
@keyframes timer{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}
.nudge{animation:nudge 2.4s cubic-bezier(.2,0,.38,.9) infinite}
@keyframes nudge{0%,60%,100%{transform:none}30%{transform:translateY(4px)}}
.nudgex{animation:nudgex 2.4s cubic-bezier(.2,0,.38,.9) infinite}
@keyframes nudgex{0%,60%,100%{transform:none}30%{transform:translateX(4px)}}
.halo{transform-box:fill-box;transform-origin:center;animation:halo 2.8s ease-out infinite}
@keyframes halo{0%{opacity:.5;transform:scale(1)}70%,100%{opacity:0;transform:scale(2.6)}}
.flow{animation:flow 2.4s linear infinite}
@keyframes flow{to{stroke-dashoffset:-100}}
.restart{animation:restart 9.6s cubic-bezier(.3,1.3,.5,1) infinite}
@keyframes restart{0%,58%{transform:none;opacity:1}63%{transform:translateY(5px);opacity:0}64%{transform:translateY(-46px);opacity:0}76%,100%{transform:none;opacity:1}}
.warn{opacity:0;animation:warn 9.6s linear infinite}
@keyframes warn{0%,50%{opacity:0}52%,74%{opacity:1}78%,100%{opacity:0}}
.lift{animation:lift 4.8s ease-in-out infinite}
@keyframes lift{0%,55%,100%{transform:none}25%{transform:translateY(-9px)}}
.blink{animation:blink 1.2s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""


def svg(w: int, h: int, label: str, body: str, defs: str = "", fixed: bool = False) -> str:
    size = f' width="{w}" height="{h}"' if fixed else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"{size} role="img" aria-label="{escape(label)}">'
            f"<title>{escape(label)}</title><style>{BASE_CSS.strip()}</style><defs>{defs}</defs>{body}</svg>\n")


def panel(t: dict, w: int, h: int, fill: str | None = None) -> str:
    return f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="6" fill="{fill or t["bg"]}" stroke="{t["border"]}"/>'


def text(x, y, s, size, fill, font=SANS, weight=400, anchor="start", extra="") -> str:
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    wt = f' font-weight="{weight}"' if weight != 400 else ""
    return f'<text x="{n(x)}" y="{n(y)}" font-family="{font}" font-size="{n(size)}"{wt}{a} fill="{fill}"{extra}>{escape(s)}</text>'


def status_dot(t: dict, x: float, y: float, r: float = 5) -> str:
    return (f'<circle class="halo" cx="{n(x)}" cy="{n(y)}" r="{n(r)}" fill="{t["ok"]}" opacity="0"/>'
            f'<circle cx="{n(x)}" cy="{n(y)}" r="{n(r)}" fill="{t["ok"]}"/>')


# --- scene: hub + ring of nodes ---------------------------------------------
def scene_defs(t: dict) -> str:
    c = t["clay"]
    return (f'<radialGradient id="ball" cx=".36" cy=".3" r=".78"><stop offset="0" stop-color="{mix(c[0], "#ffffff", .25)}"/>'
            f'<stop offset=".5" stop-color="{c[0]}"/><stop offset=".74" stop-color="{c[1]}"/><stop offset=".76" stop-color="{c[2]}"/></radialGradient>'
            f'<radialGradient id="shade"><stop offset=".3" stop-color="{t["shade"]}" stop-opacity="{t["shade_k"]}"/>'
            f'<stop offset=".7" stop-color="{t["shade"]}" stop-opacity="{t["shade_k"] * .3:.2f}"/><stop offset="1" stop-color="{t["shade"]}" stop-opacity="0"/></radialGradient>')


def ellipse_path(cx, cy, rx, ry, a0=0.0, a1=math.tau, steps=48) -> str:
    """Arc on the ground plane, angle 0 = nearest point, clockwise seen from above."""
    pts = []
    m = max(2, int(steps * abs(a1 - a0) / math.tau))
    for i in range(m + 1):
        a = a0 + (a1 - a0) * i / m
        pts.append(f"{n(cx + rx * math.sin(a))} {n(cy + ry * math.cos(a))}")
    return "M" + "L".join(pts)


def scene(t: dict, cx: float, cy: float, R: float, labels: list[str] | None, count: int = 8,
          label_size: float = 15, ball: float = 17) -> str:
    u = R / 225  # scale unit
    core_r, core_h, top_y = 50 * u, 22 * u, cy - 26 * u
    timer_r = core_r * 1.46
    o = []
    # ground: orbit, group arcs, core shadow
    o.append(f'<ellipse cx="{n(cx)}" cy="{n(cy)}" rx="{n(R)}" ry="{n(R * K)}" fill="none" stroke="{t["border"]}" stroke-opacity=".8"/>')
    g = 4
    for i in range(g):
        a0 = math.tau * i / g + 0.12
        a1 = math.tau * (i + 1) / g - 0.12
        o.append(f'<path d="{ellipse_path(cx, cy, R * 1.3, R * 1.3 * K, a0, a1)}" fill="none" stroke="{t["strong"]}" stroke-opacity=".55" stroke-linecap="round"/>')
    o.append(f'<ellipse cx="{n(cx + 8 * u)}" cy="{n(cy + 6 * u)}" rx="{n(core_r * 1.9)}" ry="{n(core_r * 1.9 * K)}" fill="url(#shade)"/>')

    nodes = []
    for i in range(count):
        a = math.tau * (i + 0.5) / count
        s = 1 + 0.13 * math.cos(a)
        gx, gy = cx + R * math.sin(a), cy + R * K * math.cos(a)
        r = ball * u * s
        nodes.append(dict(i=i, a=a, s=s, gx=gx, gy=gy, r=r, bx=gx, by=gy - 30 * u * s))
    for nd in nodes:  # contact shadows
        o.append(f'<ellipse class="sh" style="animation-delay:-{nd["i"] * .7:.1f}s" cx="{n(nd["gx"] + 7 * u)}" cy="{n(nd["gy"] + 2 * u)}" rx="{n(nd["r"] * 1.5)}" ry="{n(nd["r"] * 1.5 * K)}" fill="url(#shade)"/>')

    def edge(nd) -> str:
        sx, sy = cx + timer_r * math.sin(nd["a"]), top_y + timer_r * K * math.cos(nd["a"])
        ex, ey = nd["bx"], nd["by"]
        qx, qy = (sx + ex) / 2, (sy + ey) / 2 - 26 * u
        d = f'M{n(sx)} {n(sy)}Q{n(qx)} {n(qy)} {n(ex)} {n(ey)}'
        delay = nd["i"] * 0.16
        return (f'<path d="{d}" fill="none" stroke="{t["strong"]}" stroke-width="1.5" stroke-linecap="round"/>'
                f'<path class="pulse" style="animation-delay:{delay:.2f}s" d="{d}" pathLength="100" fill="none" stroke="{t["accent"]}" '
                f'stroke-width="{n(3 * max(u, .7))}" stroke-linecap="round" stroke-dasharray="8 92"/>')

    def node(nd) -> str:
        r, bx, by = nd["r"], nd["bx"], nd["by"]
        fade = 1 - 0.28 * (1 - math.cos(nd["a"])) / 2
        delay = nd["i"] * 0.16
        body = (f'<g class="bob" style="animation-delay:-{nd["i"] * .7:.1f}s">'
                f'<circle cx="{n(bx)}" cy="{n(by)}" r="{n(r + 8 * u)}" fill="none" stroke="{t["text3"]}" stroke-opacity=".55" stroke-width="{n(4.5 * u)}" stroke-dasharray="1.4 3.4"/>'
                f'<circle class="flash" style="animation-delay:{delay:.2f}s" cx="{n(bx)}" cy="{n(by)}" r="{n(r + 3 * u)}" fill="none" stroke="{t["accent"]}" stroke-width="2"/>'
                f'<circle cx="{n(bx)}" cy="{n(by)}" r="{n(r)}" fill="{t["bg"]}"/>'
                f'<circle cx="{n(bx)}" cy="{n(by)}" r="{n(r)}" fill="url(#ball)" opacity="{fade:.2f}"/></g>')
        if labels:
            halo = f' stroke="{t["bg"]}" stroke-width="5" stroke-linejoin="round" paint-order="stroke"'
            side, off = math.sin(nd["a"]), r + 14 * u
            if abs(side) > 0.7:  # side nodes: label outwards, level with the ball
                body += text(bx + math.copysign(off, side), by + label_size * .34, labels[nd["i"]], label_size, t["text2"], MONO,
                             anchor="start" if side > 0 else "end", extra=halo)
            elif math.cos(nd["a"]) < 0:  # far nodes: label above
                body += text(bx, by - off - label_size * .2, labels[nd["i"]], label_size, t["text2"], MONO, anchor="middle", extra=halo)
            else:
                body += text(nd["gx"], nd["gy"] + r * K + label_size * 1.45, labels[nd["i"]], label_size, t["text2"], MONO, anchor="middle", extra=halo)
        return body

    back = [nd for nd in nodes if math.cos(nd["a"]) < 0]
    front = sorted((nd for nd in nodes if math.cos(nd["a"]) >= 0), key=lambda d: math.cos(d["a"]))
    for nd in sorted(back, key=lambda d: math.cos(d["a"])):
        o.append(edge(nd) + node(nd))

    # hub: hexagonal prism, lit from the upper left like the site's shader
    def hexpts(y):
        return [(cx + core_r * math.sin(k * math.pi / 3), y + core_r * K * math.cos(k * math.pi / 3)) for k in range(6)]
    top, bot = hexpts(top_y), hexpts(top_y + core_h)
    poly = lambda pts, fill: f'<polygon points="{" ".join(f"{n(x)},{n(y)}" for x, y in pts)}" fill="{fill}"/>'
    core = t["text"]
    o.append(poly([top[5], top[0], bot[0], bot[5]], mix(core, t["bg"], .18)))
    o.append(poly([top[0], top[1], bot[1], bot[0]], mix(core, t["bg"], .45)))
    o.append(poly(top, core))
    tp = ellipse_path(cx, top_y, timer_r, timer_r * K, math.pi, math.pi + math.tau)
    o.append(f'<path d="{tp}Z" fill="none" stroke="{t["border"]}" stroke-width="1.5"/>')
    o.append(f'<path class="timer" d="{tp}" pathLength="100" fill="none" stroke="{t["accent"]}" stroke-width="2" stroke-linecap="round" stroke-dasharray="100" stroke-dashoffset="68"/>')
    for nd in front:
        o.append(edge(nd) + node(nd))
    return "".join(o)


def workshop(t: dict, ox: float, oy: float, u: float, fs: float) -> str:
    """Platform workshop: meshed pods with sidecars, a database stack, an MCP gateway, a terminal."""
    c = Clay(t, ox, oy, u)
    W, D = 16, 12
    c.box(0, 0, -.45, W, D, .45, "base")
    edge = [(0, 0), (W, 0), (W, D), (0, D)]
    c.raw(f'<path d="{c.ground(edge)}Z" fill="none" stroke="{t["border"]}"/>')
    for k in range(2, W, 2):
        c.raw(f'<path d="{c.ground([(k, 0), (k, D)])}" stroke="{t["border"]}" stroke-opacity=".45"/>')
    for k in range(2, D, 2):
        c.raw(f'<path d="{c.ground([(0, k), (W, k)])}" stroke="{t["border"]}" stroke-opacity=".45"/>')

    wires = [
        [(4.4, 2.6), (6.5, 2.6)], [(4.4, 7.6), (6.5, 7.6)], [(2.6, 3.7), (2.6, 6.5)], [(7.6, 3.7), (7.6, 6.5)],
        [(9.4, 2.6), (11.4, 2.6)], [(9.4, 7.6), (11.2, 7.6)], [(12.9, 7.0), (12.9, 4.3)],
        [(2.6, 10.3), (2.6, 8.7)], [(4.4, 10.7), (12.9, 10.7), (12.9, 9.2)],
    ]
    for k, w in enumerate(wires):
        d = c.ground(w)
        c.raw(f'<path d="{d}" fill="none" stroke="{t["strong"]}" stroke-width="{n(u * .12)}" stroke-linecap="round" stroke-linejoin="round"/>'
              f'<path class="flow" style="animation-delay:-{k * .53:.2f}s;animation-duration:{2.2 + (k % 3) * .5:.1f}s" d="{d}" pathLength="100" fill="none" '
              f'stroke="{t["accent"]}" stroke-width="{n(u * .22)}" stroke-linecap="round" stroke-dasharray="7 43" stroke-dashoffset="-12"/>')

    halo = f' stroke="{t["bg"]}" stroke-width="{n(fs * .32)}" stroke-linejoin="round" paint-order="stroke"'

    def dot(x, y, z, k, warn=False):
        cx, cy = c.p(x, y, z)
        r = u * .2
        o = f'<circle class="bob" style="animation-delay:-{k * .7:.1f}s" cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="{t["ok"]}"/>'
        if warn:
            o += f'<circle class="warn" cx="{n(cx)}" cy="{n(cy)}" r="{n(r * 1.25)}" fill="{t["gold"][0]}"/>'
        c.raw(o)

    def pod(x, y, k, restart=False):
        if restart:
            c.raw('<g class="restart">')
        c.box(x, y, 0, 2.2, 2.2, 1.7)
        c.quad([(x + .35, y + 2.2, 1.05), (x + 1.85, y + 2.2, 1.05), (x + 1.85, y + 2.2, 1.3), (x + .35, y + 2.2, 1.3)], t["clay"][2])
        if restart:
            c.raw('</g>')
        c.box(x + 2.2, y + .75, 0, .7, .7, .95, "gold")
        dot(x + 1.1, y + 1.1, 2.55, k, restart)

    pod(1.5, 1.5, 0)
    pod(6.5, 1.5, 1)
    pod(1.5, 6.5, 2)
    # database stack: three clay discs, the top one lifts out
    c.cyl(12.9, 2.9, 0, 1.35, .7, "clay")
    c.cyl(12.9, 2.9, .95, 1.35, .7, "clay")
    c.raw('<g class="lift">')
    c.cyl(12.9, 2.9, 1.9, 1.35, .7, "gold")
    c.raw('</g>')
    # terminal
    tx, ty = 1.4, 10.3
    c.box(tx, ty, 0, 3.0, .4, 2.1, "ink")
    c.quad([(tx + .2, ty + .4, .25), (tx + 2.8, ty + .4, .25), (tx + 2.8, ty + .4, 1.9), (tx + .2, ty + .4, 1.9)], t["screen"])
    for r_, (ln, col) in enumerate([(1.5, t["accent"]), (2.0, t["clay"][0]), (1.1, t["clay"][0])]):
        z = 1.55 - r_ * .42
        c.quad([(tx + .4, ty + .4, z), (tx + .4 + ln, ty + .4, z), (tx + .4 + ln, ty + .4, z + .16), (tx + .4, ty + .4, z + .16)], col)
    c.raw('<g class="blink">')
    c.quad([(tx + 1.7, ty + .4, .71), (tx + 1.95, ty + .4, .71), (tx + 1.95, ty + .4, .93), (tx + 1.7, ty + .4, .93)], t["gold"][0])
    c.raw('</g>')
    pod(6.5, 6.5, 3, restart=True)
    # MCP gateway: one dark block, three gold ports
    gx, gy = 11.2, 7.0
    c.box(gx, gy, 0, 3.4, 2.2, 1.3, "ink")
    for k in range(3):
        px = gx + .45 + k * .95
        c.quad([(px, gy + 2.2, .45), (px + .55, gy + 2.2, .45), (px + .55, gy + 2.2, .85), (px, gy + 2.2, .85)], t["gold"][0])
    c.box(gx + 1.2, gy + .6, 1.3, 1.0, 1.0, .35, "clay")
    dot(gx + 1.7, gy + 1.1, 2.3, 4)

    def label(x, y, s, anchor="middle", z=0.0):
        lx, ly = c.p(x, y, z)
        c.raw(text(lx, ly, s, fs, t["text2"], MONO, anchor=anchor, extra=halo))

    label(5.2, 5.3, "mesh")
    label(15.1, 1.2, "dbaas", z=2.2)
    label(15.4, 9.9, "mcp", z=-.9)
    label(1.2, 13.1, "tooling", z=.2)
    return c.svg()


def header(t: dict, compact: bool) -> str:
    label = "hexarch — Nikita Belyakov, Go platform engineer: service mesh, DBaaS, developer tooling, MCP infrastructure"
    if not compact:
        w, h = 1200, 440
        body = panel(t, w, h) + workshop(t, 872, 74, 22, 16)
        x = 64
        body += status_dot(t, x + 6, 82) + text(x + 22, 88, "Nikita Belyakov · platform engineering in Go", 17, t["text3"], MONO)
        body += title("hexarch", x - 4, 198, 92, t["text"])
        body += text(x, 256, "Go platform engineer. Service mesh, DBaaS,", 25, t["text2"])
        body += text(x, 290, "developer tooling and MCP infrastructure.", 25, t["text2"])
        body += text(x, 368, "Scroll — a tour of what I build", 17, t["text3"], MONO)
        body += f'<g class="nudge">{text(x + 31.6 * 17 * .602, 368, "↓", 17, t["text3"], MONO)}</g>'
    else:
        w, h = 720, 760
        body = panel(t, w, h) + workshop(t, 322, 66, 25, 22)
        x = 44
        body += status_dot(t, x + 8, 446, 7) + text(x + 30, 455, "Nikita Belyakov · Go platform engineer", 25, t["text3"], MONO)
        body += title("hexarch", x - 4, 604, 116, t["text"])
        body += text(x, 664, "Service mesh, DBaaS, developer tooling", 33, t["text2"])
        body += text(x, 706, "and MCP infrastructure.", 33, t["text2"])
        body += f'<g class="nudge">{text(w - x, 706, "↓", 33, t["text3"], MONO, anchor="end")}</g>'
    return svg(w, h, label, body, scene_defs(t))


# --- stack -------------------------------------------------------------------
STACK = [
    ("languages", ["Go", "Swift", "TypeScript", "C#", "Python"]),
    ("platform", ["Kubernetes", "k3s", "Flux GitOps", "Consul", "Docker"]),
    ("data", ["PostgreSQL", "ClickHouse", "Redis", "Kafka"]),
    ("services", ["gRPC", "MCP", "Temporal", "OAuth 2"]),
    ("ui & 3D", ["React", "three.js", "Vite", "SwiftUI"]),
]


def stack(t: dict, compact: bool) -> str:
    w = 720 if compact else 1200
    fs = 27 if compact else 21
    ch, gap, padx = fs * 1.9, fs * 0.5, fs * 0.75
    x0 = 40 if compact else 250
    maxw = w - 40
    o, y = [], (34 if compact else 30)
    for ri, (name, items) in enumerate(STACK):
        if ri:
            o.append(f'<line x1="1" x2="{w - 1}" y1="{n(y - (18 if compact else 14))}" y2="{n(y - (18 if compact else 14))}" stroke="{t["border"]}"/>')
        ly = y + ch / 2
        if compact:
            o.append(status_dot(t, 48, y + fs * .42, 6).replace('class="halo"', f'class="halo" style="animation-delay:{ri * .4:.1f}s"'))
            o.append(text(68, y + fs * .78, name, fs, t["text3"], MONO))
            y += fs * 1.55
            ly = y + ch / 2
        else:
            o.append(status_dot(t, 46, ly, 5).replace('class="halo"', f'class="halo" style="animation-delay:{ri * .4:.1f}s"'))
            o.append(text(66, ly + fs * .34, name, fs, t["text3"], MONO))
        x = x0
        for it in items:
            cw = len(it) * fs * 0.602 + padx * 2
            if x + cw > maxw:
                x, y = x0, y + ch + gap
                ly = y + ch / 2
            o.append(f'<rect x="{n(x)}" y="{n(y)}" width="{n(cw)}" height="{n(ch)}" rx="4" fill="{t["surface2"]}"/>')
            o.append(text(x + cw / 2, ly + fs * .34, it, fs, t["text"], MONO, anchor="middle"))
            x += cw + gap
        y += ch + (36 if compact else 28)
    h = round(y - (36 if compact else 28) + (34 if compact else 30))
    return svg(w, h, "Stack: " + "; ".join(f"{k}: {', '.join(v)}" for k, v in STACK), panel(t, w, h, t["surface"]) + "".join(o))


# --- clay figurines (flat-shaded isometric solids) ----------------------------
class Clay:
    def __init__(self, t: dict, ox: float, oy: float, u: float):
        self.t, self.ox, self.oy, self.u, self.o = t, ox, oy, u, []

    def p(self, x, y, z):
        return (self.ox + (x - y) * 0.866 * self.u, self.oy + (x + y) * 0.5 * self.u - z * self.u)

    def quad(self, pts, fill):
        self.o.append(f'<polygon points="{" ".join(f"{n(a)},{n(b)}" for a, b in (self.p(*q) for q in pts))}" fill="{fill}" stroke="{fill}" stroke-width=".6" stroke-linejoin="round"/>')

    def box(self, x, y, z, dx, dy, dz, mat="clay"):
        top, left, right = self.t[mat]
        self.quad([(x, y + dy, z), (x + dx, y + dy, z), (x + dx, y + dy, z + dz), (x, y + dy, z + dz)], left)
        self.quad([(x + dx, y, z), (x + dx, y + dy, z), (x + dx, y + dy, z + dz), (x + dx, y, z + dz)], right)
        self.quad([(x, y, z + dz), (x + dx, y, z + dz), (x + dx, y + dy, z + dz), (x, y + dy, z + dz)], top)

    def cyl(self, x, y, z, r, h, mat="gold"):
        top, left, right = self.t[mat]
        cx, cy = self.p(x, y, z)
        rx, ry, hh = r * 1.2247 * self.u, r * 0.7071 * self.u, h * self.u
        self.o.append(f'<path d="M{n(cx - rx)} {n(cy - hh)}V{n(cy)}A{n(rx)} {n(ry)} 0 0 0 {n(cx + rx)} {n(cy)}V{n(cy - hh)}Z" fill="{left}"/>')
        self.o.append(f'<path d="M{n(cx)} {n(cy + ry)}A{n(rx)} {n(ry)} 0 0 0 {n(cx + rx)} {n(cy)}V{n(cy - hh)}H{n(cx)}Z" fill="{right}"/>')
        self.o.append(f'<ellipse cx="{n(cx)}" cy="{n(cy - hh)}" rx="{n(rx)}" ry="{n(ry)}" fill="{top}"/>')

    def disc_left(self, x, y, z, r, fill):
        """Disc lying on a left-facing wall (plane y = const), centre (x, y, z)."""
        pts = [self.p(x + r * math.cos(a), y, z + r * math.sin(a)) for a in (math.tau * i / 28 for i in range(28))]
        self.o.append(f'<polygon points="{" ".join(f"{n(a)},{n(b)}" for a, b in pts)}" fill="{fill}"/>')

    def raw(self, s: str):
        self.o.append(s)

    def ground(self, pts, z=0.0) -> str:
        return "M" + "L".join(f"{n(a)} {n(b)}" for a, b in (self.p(x, y, z) for x, y in pts))

    def svg(self) -> str:
        return "".join(self.o)


def fig_porovnu(c: Clay):
    c.box(0, 0, 0, 2.1, 3.2, .55)
    c.box(2.9, 0, 0, 2.1, 3.2, .55)
    c.cyl(1.05, 1.6, .55, .62, .3)
    c.cyl(3.95, 1.6, .55, .62, .3)
    c.cyl(3.95, 1.6, .85, .62, .3)


def fig_hexbridge(c: Clay):
    c.box(-.4, 0, 0, 1.1, 1.5, 2.3)
    c.box(3.9, 0, 0, 1.1, 1.5, 2.3)
    c.box(-.9, -.1, 2.3, 6.4, 1.7, .5)
    c.box(1.7, .25, 2.8, 1.2, 1, .5, "gold")


def fig_memecam(c: Clay):
    c.box(0, 0, 0, 3.6, 2.2, 2.4)
    c.box(.5, .5, 2.4, 1.2, 1.1, .5, "ink")
    c.cyl(2.75, 1.1, 2.4, .32, .22)
    c.disc_left(1.8, 2.2, 1.2, .92, c.t["ink"][1])
    c.disc_left(1.8, 2.2, 1.2, .62, c.t["gold"][0])
    c.disc_left(1.8, 2.2, 1.2, .3, c.t["ink"][2])


def fig_calendar(c: Clay):
    c.box(0, 0, 0, 4.2, 3.6, .5)
    c.box(0, 0, .5, 4.2, .9, .3, "gold")
    for i in range(3):
        for j in range(2):
            x, y = .5 + i * 1.2, 1.3 + j * 1.1
            c.quad([(x, y, .5), (x + .8, y, .5), (x + .8, y + .7, .5), (x, y + .7, .5)],
                   c.t["gold"][0] if (i, j) == (1, 1) else c.t["clay"][2])
    c.box(.9, .3, .8, .3, .3, .5, "ink")
    c.box(3.0, .3, .8, .3, .3, .5, "ink")


def fig_goimporter(c: Clay):
    c.box(0, 0, 0, 4.6, 2.2, .6)
    c.box(0, 0, .85, 3.4, 2.2, .6)
    c.box(0, 0, 1.7, 2.2, 2.2, .6)
    c.box(0, 0, 2.55, 1.1, 2.2, .6, "gold")


def fig_onec(c: Clay):
    c.box(0, 0, 0, 2.8, 2.4, 3.3)
    for k in range(3):
        z = .35 + k * 1.0
        c.quad([(.3, 2.4, z), (2.5, 2.4, z), (2.5, 2.4, z + .7), (.3, 2.4, z + .7)], c.t["clay"][2])
        c.quad([(1.05, 2.4, z + .26), (1.75, 2.4, z + .26), (1.75, 2.4, z + .46), (1.05, 2.4, z + .46)],
               c.t["gold"][0] if k == 1 else c.t["clay"][0])
    c.box(3.5, .9, 0, .9, .9, .9, "gold")


CARDS = [
    ("porovnu", fig_porovnu, "Go", "#00add8",
     "Bill splitter in production: receipt scan, per-item split, one-transfer settlement.",
     "Go microservices · SwiftUI"),
    ("hexbridge", fig_hexbridge, "C#", "#178600",
     "A Mac's microphone and DualSense on a Windows gaming PC, beside the game stream.",
     "C# · Swift · Kotlin · Go"),
    ("memecam", fig_memecam, "Swift", "#f05138",
     "Face and hand gestures become cat memes, live in any call via a virtual camera.",
     "Swift 6 · Apple Vision"),
    ("itmo-calendar", fig_calendar, "Go", "#00add8",
     "University schedule as a subscribable calendar feed for Apple and Google Calendar.",
     "Go · iCal / CalDAV"),
    ("goimporter", fig_goimporter, "Go", "#00add8",
     "Deterministic grouping and ordering of Go imports across a whole codebase.",
     "Go · CLI"),
    ("onec-conf-fetcher", fig_onec, "Python", "#3572a5",
     "NetExec module that collects and parses 1C Enterprise configuration files over SMB.",
     "Python · NetExec"),
]


def wrap(s: str, width: int) -> list[str]:
    lines, cur = [], ""
    for word in s.split():
        if cur and len(cur) + 1 + len(word) > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur]


def figure(t: dict, fig, cx: float, cy: float, u: float, delay: float = 0) -> str:
    c = Clay(t, 0, 0, u)
    fig(c)
    # centre the figurine on (cx, cy) using the bounds of what was drawn
    xs, ys = [], []
    import re
    for m in re.finditer(r'points="([^"]+)"', c.svg()):
        for pair in m.group(1).split():
            a, b = pair.split(",")
            xs.append(float(a)); ys.append(float(b))
    dx, dy = cx - (min(xs) + max(xs)) / 2, cy - (min(ys) + max(ys)) / 2
    bw = max(xs) - min(xs)
    shadow = f'<ellipse class="sh" style="animation-delay:-{delay}s" cx="{n(cx + 3)}" cy="{n(max(ys) + dy + 1)}" rx="{n(bw * .56)}" ry="{n(bw * .2)}" fill="url(#shade)"/>'
    return shadow + f'<g class="bob" style="animation-delay:-{delay}s"><g transform="translate({n(dx)} {n(dy)})">{c.svg()}</g></g>'


def card(t: dict, idx: int) -> str:
    name, fig, lang, lang_color, desc, meta = CARDS[idx]
    w, h = 418, 172
    o = [panel(t, w, h, t["surface"])]
    o.append(f'<rect x="1" y="1" width="112" height="{h - 2}" rx="5" fill="{t["bg"]}"/><line x1="113" x2="113" y1="1" y2="{h - 1}" stroke="{t["border"]}"/>')
    o.append(figure(t, fig, 57, 84, 12.5, idx * 0.9))
    x = 132
    o.append(text(x, 39, name, 19, t["text"], MONO, 700))
    for i, line in enumerate(wrap(desc, 38)):
        o.append(text(x, 66 + i * 21, line, 14.5, t["text2"]))
    o.append(f'<circle cx="{x + 5}" cy="{h - 27}" r="4.5" fill="{lang_color}"/>')
    o.append(text(x + 17, h - 22.5, meta, 12.5, t["text3"], MONO))
    o.append(f'<g class="nudgex" style="animation-delay:{idx * .3:.1f}s">{text(w - 20, h - 21, "→", 16, t["accent"], MONO, anchor="end")}</g>')
    return svg(w, h, f"{name} — {desc}", "".join(o), scene_defs(t), fixed=True)


# --- site plaque -----------------------------------------------------------------
def site(t: dict, compact: bool) -> str:
    label = "hexarch.me — a personal server run as code, with a live 3D service map"
    if not compact:
        w, h = 1200, 250
        body = panel(t, w, h) + scene(t, 190, 142, 112, None, count=6, ball=19)
        x = 390
        body += title("hexarch.me", x - 3, 104, 50, t["text"], rise=False)
        body += text(x, 150, "A personal server run as code: k3s and Flux GitOps,", 23, t["text2"])
        body += text(x, 182, "with a live 3D map of every service on the front page.", 23, t["text2"])
        bx, by, bw, bh = 940, 176, 212, 46
        body += f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="5" fill="{t["accent"]}"/>'
        on = "#0c1413" if t is THEMES["dark"] else "#ffffff"
        body += text(bx + 22, by + 30, "Take the tour", 19, on, MONO, 600)
        body += f'<g class="nudgex">{text(bx + bw - 22, by + 30, "→", 19, on, MONO, 600, anchor="end")}</g>'
    else:
        w, h = 720, 480
        body = panel(t, w, h) + scene(t, 150, 150, 92, None, count=6, ball=20)
        x = 44
        body += title("hexarch.me", 300, 132, 56, t["text"], rise=False)
        body += text(300, 178, "the server as code", 27, t["text3"], MONO)
        body += text(x, 300, "A personal server on k3s and Flux GitOps,", 31, t["text2"])
        body += text(x, 340, "with a live 3D map of every service.", 31, t["text2"])
        bx, by, bw, bh = x, 384, w - 2 * x, 62
        body += f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="6" fill="{t["accent"]}"/>'
        on = "#0c1413" if t is THEMES["dark"] else "#ffffff"
        body += text(bx + 28, by + 41, "Take the tour", 28, on, MONO, 600)
        body += f'<g class="nudgex">{text(bx + bw - 28, by + 41, "→", 28, on, MONO, 600, anchor="end")}</g>'
    return svg(w, h, label, body, scene_defs(t))


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    files = {}
    for name, t in THEMES.items():
        for compact in (False, True):
            sfx = f"{'-compact' if compact else ''}-{name}.svg"
            files["header" + sfx] = header(t, compact)
            files["stack" + sfx] = stack(t, compact)
            files["site" + sfx] = site(t, compact)
        for i, c in enumerate(CARDS):
            files[f"card-{c[0]}-{name}.svg"] = card(t, i)
    for fn, data in sorted(files.items()):
        (OUT / fn).write_text(data, encoding="utf-8")
        print(f"{len(data.encode()):6d}  assets/{fn}")


if __name__ == "__main__":
    main()
