"""Single-stroke glyph outlines in writing order.

Each glyph is defined in a unit cap-height frame: baseline y=0, cap line y=1.
Strokes are polylines ordered the way a person typically prints the character
(left-to-right, stroke by stroke). Curves are sampled densely so the later
interpolation step can space tags evenly along the ink.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

Point = tuple[float, float]
Stroke = list[Point]
Glyph = tuple[float, list[Stroke]]


def _arc(cx: float, cy: float, rx: float, ry: float, a0: float, a1: float, steps: int = 16) -> Stroke:
    """Elliptical arc. Angles in degrees, 0 = +X, 90 = +Y. Direction follows a0 -> a1."""
    a0_r = math.radians(a0)
    a1_r = math.radians(a1)
    return [
        (
            cx + rx * math.cos(a0_r + (a1_r - a0_r) * i / steps),
            cy + ry * math.sin(a0_r + (a1_r - a0_r) * i / steps),
        )
        for i in range(steps + 1)
    ]


def _line(*coords: float) -> Stroke:
    if len(coords) % 2:
        raise ValueError("line coordinates must be x,y pairs")
    return [(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]


def _glyph(strokes: Sequence[Stroke], advance: float | None = None, bearing: float = 0.12) -> Glyph:
    ink_right = max((x for stroke in strokes for x, _y in stroke), default=0.0)
    return (advance if advance is not None else ink_right + bearing, [list(s) for s in strokes])


# Capitals: print stroke order (stem first where that is the usual first stroke).
_A = _glyph(
    [
        _line(0.00, 0.00, 0.36, 1.00),
        _line(0.36, 1.00, 0.72, 0.00),
        _line(0.14, 0.38, 0.58, 0.38),
    ]
)
_B = _glyph(
    [
        _line(0.00, 0.00, 0.00, 1.00),
        _arc(0.22, 0.75, 0.32, 0.25, 90, -90, 12) + _arc(0.22, 0.28, 0.36, 0.28, 90, -90, 12),
    ]
)
_C = _glyph([_arc(0.40, 0.50, 0.40, 0.50, 50, 310, 18)])
_D = _glyph(
    [
        _line(0.00, 0.00, 0.00, 1.00),
        _arc(0.08, 0.50, 0.52, 0.50, 90, -90, 16),
    ]
)
_E = _glyph(
    [
        _line(0.00, 1.00, 0.00, 0.00),
        _line(0.00, 1.00, 0.58, 1.00),
        _line(0.00, 0.50, 0.48, 0.50),
        _line(0.00, 0.00, 0.58, 0.00),
    ]
)
_F = _glyph(
    [
        _line(0.00, 1.00, 0.00, 0.00),
        _line(0.00, 1.00, 0.56, 1.00),
        _line(0.00, 0.50, 0.46, 0.50),
    ]
)
_G = _glyph(
    [
        _arc(0.42, 0.50, 0.42, 0.50, 50, 320, 18),
        _line(0.62, 0.42, 0.42, 0.42),
    ]
)
_H = _glyph(
    [
        _line(0.00, 1.00, 0.00, 0.00),
        _line(0.62, 1.00, 0.62, 0.00),
        _line(0.00, 0.50, 0.62, 0.50),
    ]
)
_I = _glyph(
    [
        _line(0.00, 1.00, 0.36, 1.00),
        _line(0.18, 1.00, 0.18, 0.00),
        _line(0.00, 0.00, 0.36, 0.00),
    ]
)
_J = _glyph(
    [
        _line(0.10, 1.00, 0.52, 1.00),
        _line(0.42, 1.00, 0.42, 0.22) + _arc(0.22, 0.22, 0.20, 0.22, 0, -180, 10),
    ]
)
_K = _glyph(
    [
        _line(0.00, 1.00, 0.00, 0.00),
        _line(0.56, 1.00, 0.00, 0.48),
        _line(0.18, 0.62, 0.60, 0.00),
    ]
)
_L = _glyph([_line(0.00, 1.00, 0.00, 0.00, 0.54, 0.00)])
_M = _glyph(
    [
        _line(0.00, 0.00, 0.00, 1.00, 0.38, 0.28, 0.76, 1.00, 0.76, 0.00),
    ]
)
_N = _glyph(
    [
        _line(0.00, 0.00, 0.00, 1.00, 0.64, 0.00, 0.64, 1.00),
    ]
)
_O = _glyph([_arc(0.40, 0.50, 0.40, 0.50, 90, -270, 24)])
_P = _glyph(
    [
        _line(0.00, 0.00, 0.00, 1.00),
        _arc(0.18, 0.72, 0.36, 0.28, 90, -90, 14),
    ]
)
_Q = _glyph(
    [
        _arc(0.40, 0.50, 0.40, 0.50, 90, -270, 24),
        _line(0.46, 0.22, 0.72, -0.08),
    ]
)
_R = _glyph(
    [
        _line(0.00, 0.00, 0.00, 1.00),
        _arc(0.18, 0.72, 0.36, 0.28, 90, -90, 14),
        _line(0.28, 0.46, 0.62, 0.00),
    ]
)
_S = _glyph(
    [
        _arc(0.32, 0.74, 0.32, 0.26, 40, 220, 12)
        + _arc(0.32, 0.26, 0.32, 0.26, 140, -40, 12)
    ]
)
_T = _glyph(
    [
        _line(0.00, 1.00, 0.68, 1.00),
        _line(0.34, 1.00, 0.34, 0.00),
    ]
)
_U = _glyph(
    [
        _line(0.00, 1.00, 0.00, 0.28) + _arc(0.32, 0.28, 0.32, 0.28, 180, 360, 12) + _line(0.64, 0.28, 0.64, 1.00),
    ]
)
_V = _glyph([_line(0.00, 1.00, 0.36, 0.00, 0.72, 1.00)])
_W = _glyph([_line(0.00, 1.00, 0.22, 0.00, 0.44, 0.72, 0.66, 0.00, 0.88, 1.00)])
_X = _glyph(
    [
        _line(0.00, 1.00, 0.64, 0.00),
        _line(0.64, 1.00, 0.00, 0.00),
    ]
)
_Y = _glyph(
    [
        _line(0.00, 1.00, 0.34, 0.48),
        _line(0.68, 1.00, 0.34, 0.48, 0.34, 0.00),
    ]
)
_Z = _glyph([_line(0.00, 1.00, 0.64, 1.00, 0.00, 0.00, 0.64, 0.00)])

# Lowercase: x-height 0.64, descenders to -0.28. Stroke order follows print writing.
_a = _glyph(
    [
        _arc(0.28, 0.32, 0.28, 0.32, 40, 320, 16),
        _line(0.54, 0.58, 0.54, 0.00),
    ]
)
_b = _glyph(
    [
        _line(0.00, 1.00, 0.00, 0.00),
        _arc(0.28, 0.32, 0.28, 0.32, 150, -150, 16),
    ]
)
_c = _glyph([_arc(0.30, 0.32, 0.28, 0.32, 50, 310, 14)])
_d = _glyph(
    [
        _arc(0.28, 0.32, 0.28, 0.32, 30, 330, 16),
        _line(0.54, 1.00, 0.54, 0.00),
    ]
)
_e = _glyph(
    [
        _line(0.04, 0.32, 0.54, 0.32) + _arc(0.28, 0.32, 0.28, 0.32, 0, 310, 16),
    ]
)
_f = _glyph(
    [
        _arc(0.30, 0.86, 0.18, 0.14, 0, 180, 8) + _line(0.12, 0.86, 0.12, 0.00),
        _line(0.00, 0.64, 0.32, 0.64),
    ]
)
_g = _glyph(
    [
        _arc(0.28, 0.32, 0.28, 0.32, 30, 330, 16),
        _line(0.54, 0.58, 0.54, -0.04) + _arc(0.30, -0.04, 0.24, 0.24, 0, -160, 10),
    ]
)
_h = _glyph(
    [
        _line(0.00, 1.00, 0.00, 0.00),
        _arc(0.28, 0.36, 0.28, 0.28, 180, 0, 10) + _line(0.56, 0.36, 0.56, 0.00),
    ]
)
_i = _glyph(
    [
        _line(0.10, 0.64, 0.10, 0.00),
        _line(0.10, 0.82, 0.10, 0.82),
    ]
)
_j = _glyph(
    [
        _line(0.22, 0.64, 0.22, 0.00) + _arc(0.06, 0.00, 0.16, 0.22, 0, -160, 8),
        _line(0.22, 0.82, 0.22, 0.82),
    ]
)
_k = _glyph(
    [
        _line(0.00, 1.00, 0.00, 0.00),
        _line(0.44, 0.64, 0.00, 0.28),
        _line(0.16, 0.38, 0.48, 0.00),
    ]
)
_l = _glyph([_line(0.10, 1.00, 0.10, 0.00)])
_m = _glyph(
    [
        _line(0.00, 0.64, 0.00, 0.00),
        _arc(0.22, 0.40, 0.22, 0.24, 180, 0, 8) + _line(0.44, 0.40, 0.44, 0.00),
        _arc(0.66, 0.40, 0.22, 0.24, 180, 0, 8) + _line(0.88, 0.40, 0.88, 0.00),
    ]
)
_n = _glyph(
    [
        _line(0.00, 0.64, 0.00, 0.00),
        _arc(0.28, 0.36, 0.28, 0.28, 180, 0, 10) + _line(0.56, 0.36, 0.56, 0.00),
    ]
)
_o = _glyph([_arc(0.30, 0.32, 0.28, 0.32, 90, -270, 20)])
_p = _glyph(
    [
        _line(0.00, 0.64, 0.00, -0.28),
        _arc(0.28, 0.32, 0.28, 0.32, 150, -150, 16),
    ]
)
_q = _glyph(
    [
        _arc(0.28, 0.32, 0.28, 0.32, 30, 330, 16),
        _line(0.54, 0.64, 0.54, -0.28),
    ]
)
_r = _glyph(
    [
        _line(0.00, 0.64, 0.00, 0.00),
        _arc(0.22, 0.44, 0.22, 0.20, 180, 20, 8),
    ]
)
_s = _glyph(
    [
        _arc(0.24, 0.48, 0.24, 0.16, 40, 220, 10)
        + _arc(0.24, 0.16, 0.24, 0.16, 140, -40, 10)
    ]
)
_t = _glyph(
    [
        _line(0.16, 0.86, 0.16, 0.12) + _arc(0.28, 0.12, 0.12, 0.12, 180, 360, 6),
        _line(0.00, 0.64, 0.34, 0.64),
    ]
)
_u = _glyph(
    [
        _line(0.00, 0.64, 0.00, 0.22) + _arc(0.26, 0.22, 0.26, 0.22, 180, 360, 10) + _line(0.52, 0.22, 0.52, 0.64),
        _line(0.52, 0.64, 0.52, 0.00),
    ]
)
_v = _glyph([_line(0.00, 0.64, 0.28, 0.00, 0.56, 0.64)])
_w = _glyph([_line(0.00, 0.64, 0.18, 0.00, 0.36, 0.50, 0.54, 0.00, 0.72, 0.64)])
_x = _glyph(
    [
        _line(0.00, 0.64, 0.52, 0.00),
        _line(0.52, 0.64, 0.00, 0.00),
    ]
)
_y = _glyph(
    [
        _line(0.00, 0.64, 0.28, 0.00),
        _line(0.56, 0.64, 0.28, 0.00, 0.12, -0.28),
    ]
)
_z = _glyph([_line(0.00, 0.64, 0.52, 0.64, 0.00, 0.00, 0.52, 0.00)])

_0 = _glyph(
    [
        _arc(0.32, 0.50, 0.32, 0.50, 90, -270, 24),
        _line(0.12, 0.18, 0.52, 0.82),
    ]
)
_1 = _glyph([_line(0.08, 0.78, 0.28, 1.00, 0.28, 0.00), _line(0.06, 0.00, 0.50, 0.00)])
_2 = _glyph(
    [
        _arc(0.30, 0.72, 0.30, 0.28, 170, 10, 12) + _line(0.58, 0.72, 0.04, 0.00, 0.58, 0.00),
    ]
)
_3 = _glyph(
    [
        _arc(0.28, 0.74, 0.30, 0.26, 160, -20, 12),
        _arc(0.28, 0.26, 0.32, 0.26, 110, -70, 12),
    ]
)
_4 = _glyph(
    [
        _line(0.48, 0.00, 0.48, 1.00, 0.04, 0.38, 0.58, 0.38),
    ]
)
_5 = _glyph(
    [
        _line(0.52, 1.00, 0.08, 1.00, 0.06, 0.56, 0.30, 0.62)
        + _arc(0.28, 0.28, 0.30, 0.28, 110, -70, 14),
    ]
)
_6 = _glyph(
    [
        _arc(0.36, 0.50, 0.36, 0.50, 50, 270, 16) + _arc(0.30, 0.30, 0.28, 0.30, 180, 540, 16),
    ]
)
_7 = _glyph([_line(0.00, 1.00, 0.58, 1.00, 0.18, 0.00)])
_8 = _glyph(
    [
        _arc(0.30, 0.74, 0.28, 0.24, 90, -270, 16),
        _arc(0.32, 0.26, 0.32, 0.26, 90, -270, 16),
    ]
)
_9 = _glyph(
    [
        _arc(0.30, 0.70, 0.28, 0.28, 90, -270, 16),
        _line(0.58, 0.70, 0.58, 0.28) + _arc(0.30, 0.28, 0.28, 0.28, 0, -150, 10),
    ]
)

_space: Glyph = (0.42, [])
_period = _glyph([_line(0.10, 0.00, 0.10, 0.00)], advance=0.28)
_comma = _glyph([_line(0.12, 0.08, 0.04, -0.16)], advance=0.28)
_hyphen = _glyph([_line(0.04, 0.36, 0.40, 0.36)], advance=0.50)
_underscore = _glyph([_line(0.00, 0.00, 0.58, 0.00)], advance=0.66)
_apostrophe = _glyph([_line(0.10, 1.00, 0.10, 0.78)], advance=0.24)
_colon = _glyph(
    [_line(0.10, 0.18, 0.10, 0.18), _line(0.10, 0.52, 0.10, 0.52)],
    advance=0.28,
)
_semicolon = _glyph(
    [_line(0.10, 0.52, 0.10, 0.52), _line(0.12, 0.18, 0.04, -0.10)],
    advance=0.28,
)
_exclaim = _glyph(
    [_line(0.10, 1.00, 0.10, 0.28), _line(0.10, 0.08, 0.10, 0.00)],
    advance=0.28,
)
_question = _glyph(
    [
        _arc(0.28, 0.72, 0.28, 0.28, 180, -10, 12) + _line(0.28, 0.44, 0.28, 0.28),
        _line(0.28, 0.08, 0.28, 0.00),
    ]
)
_amp = _glyph(
    [
        _arc(0.28, 0.72, 0.22, 0.22, 30, 240, 12)
        + _arc(0.28, 0.28, 0.28, 0.28, 150, -30, 12)
        + _line(0.52, 0.14, 0.64, 0.00),
        _line(0.12, 0.22, 0.52, 0.72),
    ]
)
_slash = _glyph([_line(0.00, 0.00, 0.40, 1.00)], advance=0.48)
_backslash = _glyph([_line(0.00, 1.00, 0.40, 0.00)], advance=0.48)
_lparen = _glyph([_arc(0.28, 0.50, 0.22, 0.62, 70, 290, 12)], advance=0.36)
_rparen = _glyph([_arc(0.04, 0.50, 0.22, 0.62, 110, -110, 12)], advance=0.36)
_plus = _glyph(
    [_line(0.00, 0.40, 0.48, 0.40), _line(0.24, 0.64, 0.24, 0.16)],
    advance=0.56,
)
_equals = _glyph(
    [_line(0.00, 0.48, 0.52, 0.48), _line(0.00, 0.28, 0.52, 0.28)],
    advance=0.62,
)
_hash = _glyph(
    [
        _line(0.12, 0.00, 0.28, 1.00),
        _line(0.36, 0.00, 0.52, 1.00),
        _line(0.02, 0.64, 0.62, 0.64),
        _line(0.00, 0.36, 0.60, 0.36),
    ]
)
_star = _glyph(
    [
        _line(0.28, 0.70, 0.28, 0.10),
        _line(0.02, 0.56, 0.54, 0.24),
        _line(0.54, 0.56, 0.02, 0.24),
    ],
    advance=0.60,
)
_at = _glyph(
    [
        _arc(0.30, 0.32, 0.16, 0.20, 90, -270, 14) + _line(0.46, 0.32, 0.46, 0.18),
        _arc(0.36, 0.42, 0.36, 0.42, 40, 320, 16),
    ]
)

def _umlaut_dots(x0: float, y: float = 1.12) -> list[Stroke]:
    return [_line(x0, y, x0, y), _line(x0 + 0.22, y, x0 + 0.22, y)]


def _with_umlaut(base: Glyph, x0: float, y: float = 1.12) -> Glyph:
    advance, strokes = base
    return advance, list(strokes) + _umlaut_dots(x0, y)


_ss = _glyph(
    [
        _arc(0.22, 0.82, 0.18, 0.18, 0, 180, 8) + _line(0.04, 0.82, 0.04, 0.00),
        _arc(0.28, 0.36, 0.24, 0.20, 180, 20, 10),
    ]
)


GLYPHS: dict[str, Glyph] = {
    " ": _space,
    "A": _A,
    "B": _B,
    "C": _C,
    "D": _D,
    "E": _E,
    "F": _F,
    "G": _G,
    "H": _H,
    "I": _I,
    "J": _J,
    "K": _K,
    "L": _L,
    "M": _M,
    "N": _N,
    "O": _O,
    "P": _P,
    "Q": _Q,
    "R": _R,
    "S": _S,
    "T": _T,
    "U": _U,
    "V": _V,
    "W": _W,
    "X": _X,
    "Y": _Y,
    "Z": _Z,
    "a": _a,
    "b": _b,
    "c": _c,
    "d": _d,
    "e": _e,
    "f": _f,
    "g": _g,
    "h": _h,
    "i": _i,
    "j": _j,
    "k": _k,
    "l": _l,
    "m": _m,
    "n": _n,
    "o": _o,
    "p": _p,
    "q": _q,
    "r": _r,
    "s": _s,
    "t": _t,
    "u": _u,
    "v": _v,
    "w": _w,
    "x": _x,
    "y": _y,
    "z": _z,
    "0": _0,
    "1": _1,
    "2": _2,
    "3": _3,
    "4": _4,
    "5": _5,
    "6": _6,
    "7": _7,
    "8": _8,
    "9": _9,
    ".": _period,
    ",": _comma,
    "-": _hyphen,
    "_": _underscore,
    "'": _apostrophe,
    ":": _colon,
    ";": _semicolon,
    "!": _exclaim,
    "?": _question,
    "&": _amp,
    "/": _slash,
    "\\": _backslash,
    "(": _lparen,
    ")": _rparen,
    "+": _plus,
    "=": _equals,
    "#": _hash,
    "*": _star,
    "@": _at,
    "Ä": _with_umlaut(_A, 0.14),
    "Ö": _with_umlaut(_O, 0.18),
    "Ü": _with_umlaut(_U, 0.10),
    "ä": _with_umlaut(_a, 0.08, 0.86),
    "ö": _with_umlaut(_o, 0.10, 0.86),
    "ü": _with_umlaut(_u, 0.06, 0.86),
    "ß": _ss,
}


def fallback_glyph() -> Glyph:
    """A small open box used for characters that have no stroke definition."""
    return _glyph(
        [
            _line(0.04, 0.00, 0.04, 0.72, 0.48, 0.72, 0.48, 0.00, 0.04, 0.00),
        ]
    )


def get_glyph(char: str) -> tuple[Glyph, bool]:
    """Return (glyph, is_fallback)."""
    if char in GLYPHS:
        return GLYPHS[char], False
    return fallback_glyph(), True
