"""Generate Ronda launcher icons as PNGs with the standard library only."""
from __future__ import annotations

import math
import os
import struct
import zlib

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "icons")


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def mix(a, b, t):
    return a + (b - a) * t


def mark(u, v, maskable: bool):
    """Return a colour for the Ronda mark, or None for the background."""
    k = 0.72 if maskable else 0.9
    cx, cy = 0.5, 0.5
    x = cx + (u - cx) / k
    y = cy + (v - cy) / k
    dist = math.hypot(x - cx, y - cy)

    # three people orbiting the round table
    for angle, radius, colour in (
        (math.radians(-90), 0.255, (198, 255, 74)),
        (math.radians(30), 0.255, (67, 224, 208)),
        (math.radians(150), 0.255, (255, 194, 75)),
    ):
        px = cx + math.cos(angle) * radius
        py = cy + math.sin(angle) * radius
        if math.hypot(x - px, y - py) < 0.072:
            return colour
    # the ring
    if abs(dist - 0.255) < 0.031:
        return (255, 246, 234)
    # the centre
    if dist < 0.052:
        return (255, 246, 234)
    return None


def render(size: int, maskable: bool = False) -> bytes:
    ss = 3
    pixels = bytearray()
    for py in range(size):
        for px in range(size):
            r = g = b = 0.0
            for sy in range(ss):
                for sx in range(ss):
                    u = (px + (sx + 0.5) / ss) / size
                    v = (py + (sy + 0.5) / ss) / size
                    colour = mark(u, v, maskable)
                    if colour:
                        r += colour[0]
                        g += colour[1]
                        b += colour[2]
                    else:
                        t = clamp(0.5 * u + 0.5 * v)
                        # coral to violet, with a warm midpoint
                        if t < 0.5:
                            local = t / 0.5
                            br, bg, bb = mix(255, 255, local), mix(77, 138, local), mix(109, 69, local)
                        else:
                            local = (t - 0.5) / 0.5
                            br, bg, bb = mix(255, 124, local), mix(138, 58, local), mix(69, 246, local)
                        r += br
                        g += bg
                        b += bb
            count = ss * ss
            pixels += bytes((int(r / count), int(g / count), int(b / count), 255))
    return _png(size, size, bytes(pixels))


def _png(width: int, height: int, raw: bytes) -> bytes:
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    stride = width * 4
    compressed = zlib.compress(
        b"".join(b"\x00" + raw[y * stride:(y + 1) * stride] for y in range(height)), 9
    )
    header = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", compressed) + chunk(b"IEND", b"")


def _ico(png: bytes) -> bytes:
    """Wrap a 256x256 PNG in a single-entry ICO container."""
    header = struct.pack("<HHH", 0, 1, 1)
    offset = 6 + 16
    entry = struct.pack("<BBBBHHII", 0, 0, 0, 0, 1, 32, len(png), offset)
    return header + entry + png


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    jobs = [
        ("icon-192.png", 192, False),
        ("icon-512.png", 512, False),
        ("icon-maskable-512.png", 512, True),
        ("apple-touch-icon.png", 180, False),
    ]
    for name, size, maskable in jobs:
        path = os.path.join(OUT, name)
        with open(path, "wb") as fh:
            fh.write(render(size, maskable))
        print("wrote", path)
    png256 = render(256, False)
    with open(os.path.join(OUT, "icon-256.png"), "wb") as fh:
        fh.write(png256)
    with open(os.path.join(OUT, "ronda.ico"), "wb") as fh:
        fh.write(_ico(png256))
    print("wrote", os.path.join(OUT, "ronda.ico"))


if __name__ == "__main__":
    main()
