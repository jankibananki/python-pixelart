
from PIL import Image, ImageDraw

SIZE = 64

C = {
    "ink": "#2a102b",
    "border": "#751a48",
    "shadow": "#b52c77",
    "pink": "#f46aa3",
    "rose": "#ff96b9",
    "pale": "#ffc9d3",
    "cream": "#ffe2a5",
    "light": "#fff4cb",
    "purple": "#b65bb6",
    "body": "#241027",
}

# pozicije krila
KEY_POSES = [
    (1.00, 0.0, 1.00),
    (0.79, -3.0, 0.82),
    (0.43, -7.0, 0.56),
    (0.75, -2.0, 0.79),
]


def blend(a, b, t):
    return a + (b - a) * t


def pose_at(phase):
    phase = (phase % 1.0) * 4

    i = int(phase)
    t = phase - i

    # Smooth interpolation
    t = t * t * (3 - 2 * t)

    return tuple(
        blend(a, b, t)
        for a, b in zip(
            KEY_POSES[i],
            KEY_POSES[(i + 1) % 4]
        )
    )


def create_butterfly(phase=0.0):
    upper_width, upper_rise, lower_width = pose_at(phase)

    im = Image.new(
        "RGBA",
        (SIZE, SIZE),
        (0, 0, 0, 0)
    )

    d = ImageDraw.Draw(im)

    #okretanje krila
    def wing(
        points,
        color,
        pivot=(26, 36),
        width=1.0,
        rise=0.0
    ):
        px, py = pivot
        transformed = []

        for x, y in points:
            distance = max(0, (x - px) / 34)

            transformed.append((
                round(px + (x - px) * width),
                round(py + (y - py) + rise * distance)
            ))

        d.polygon(
            transformed,
            fill=C.get(color, color)
        )

    #sporedno krilo

    rear = (24, 36)

    rear_w = 0.88 + 0.10 * upper_width
    rear_rise = upper_rise * 0.4

    def rear_poly(points, color):
        px, py = rear
        transformed = []

        for x, y in points:
            nx = px + (x - px) * rear_w

            ny = py + (y - py) + rear_rise * max(
                0, (py - y) / 29
            )

            transformed.append((
                round(nx),
                round(ny)
            ))

        d.polygon(
            transformed,
            fill=C[color]
        )

    #spolja
    rear_poly([
        (24, 35), (20, 30), (16, 24),
        (14, 17), (16, 9), (21, 7),
        (26, 11), (29, 20), (28, 31)
    ], "border")

    #base color
    rear_poly([
        (23, 31), (19, 25), (17, 17),
        (19, 11), (22, 11), (26, 17),
        (26, 29)
    ], "pale")

    #unutrasnjost
    rear_poly([
        (22, 29), (20, 23), (20, 16),
        (23, 14), (25, 19), (25, 28)
    ], "cream")

    rear_poly([
        (20, 20), (20, 16),
        (21, 15), (22, 17)
    ], "shadow")

    #gornje krilo

    pivot = (26, 37)

    def up(points, color):
        wing(
            points,
            color,
            pivot,
            upper_width,
            upper_rise
        )

    #spoljasnji oblik
    up([
        (25, 37), (26, 29), (29, 23),
        (33, 17), (39, 11), (45, 6),
        (50, 4), (56, 5), (60, 10),
        (61, 16), (58, 21), (55, 23),
        (59, 27), (59, 33), (55, 38),
        (49, 41), (39, 43), (30, 41)
    ], "ink")

    #tamni okvir
    up([
        (28, 35), (29, 28), (34, 20),
        (40, 13), (47, 8), (51, 7),
        (56, 9), (58, 14), (56, 19),
        (52, 23), (56, 27), (56, 33),
        (52, 36), (46, 39), (37, 40)
    ], "border")

    #ping deo
    up([
        (29, 34), (31, 27), (36, 20),
        (43, 13), (48, 10), (54, 10),
        (56, 14), (53, 20), (50, 23),
        (54, 27), (54, 33), (48, 37),
        (38, 38)
    ], "pink")

    #patern
    up([
        (31, 33), (36, 25), (41, 20),
        (46, 20), (49, 24), (46, 30),
        (40, 35), (34, 37)
    ], "cream")

    #glavni highlight
    up([
        (36, 32), (40, 25), (44, 23),
        (45, 26), (40, 32)
    ], "light")

    #tacke na gornjem krilu
    up([
        (45, 12), (49, 9), (53, 11),
        (54, 15), (51, 19), (47, 17)
    ], "pale")

    up([
        (49, 12), (52, 12),
        (52, 15), (49, 16)
    ], "light")

    up([
        (49, 28), (52, 26),
        (54, 29), (52, 33),
        (48, 33)
    ], "rose")

    up([
        (45, 35), (47, 34),
        (49, 35), (48, 37)
    ], "cream")

    # sara
    up([
        (30, 37), (32, 32),
        (37, 25), (41, 22),
        (38, 27), (34, 35)
    ], "shadow")

    # donje krilo

    def low(points, color):
        wing(
            points,
            color,
            (26, 39),
            lower_width,
            0
        )

    #outline
    low([
        (26, 39), (35, 40), (44, 43),
        (51, 47), (56, 52), (57, 56),
        (53, 59), (46, 60), (39, 56),
        (33, 52), (28, 47)
    ], "ink")

    #border
    low([
        (29, 41), (36, 42), (44, 45),
        (51, 49), (54, 54), (52, 57),
        (46, 57), (39, 53), (32, 47)
    ], "border")

    #pink deo
    low([
        (30, 42), (38, 44), (45, 47),
        (51, 51), (52, 55), (47, 55),
        (40, 51), (33, 46)
    ], "pink")

    #cream patern
    low([
        (33, 44), (39, 46), (45, 49),
        (48, 52), (45, 53), (39, 50),
        (35, 47)
    ], "cream")

    #donji highlight
    low([
        (45, 55), (50, 56),
        (52, 55), (49, 57),
        (46, 57)
    ], "pale")

    #telo

    #telo - osnova
    d.polygon([
        (22, 34), (26, 33),
        (29, 37), (29, 43),
        (27, 48), (25, 53),
        (23, 55), (22, 52),
        (24, 45), (23, 40)
    ], fill=C["body"])

    #glava
    d.ellipse(
        (20, 32, 28, 39),
        fill=C["body"]
    )

    #highlight na telo
    d.line([
        (24, 39), (25, 45),
        (24, 51)
    ], fill=C["border"], width=1)

    #antenice
    d.line([
        (22, 34), (17, 29),
        (13, 23), (12, 19)
    ], fill=C["border"], width=1)

    d.line([
        (24, 33), (20, 25),
        (20, 18)
    ], fill=C["border"], width=1)

    #antenice-vrhovi
    d.rectangle(
        (11, 17, 13, 19),
        fill=C["shadow"]
    )

    d.rectangle(
        (19, 16, 21, 18),
        fill=C["shadow"]
    )

    return im
