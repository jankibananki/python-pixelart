
from butterfly import create_butterfly


def generate_frames(count=12):
    return [
        create_butterfly(i / count)
        for i in range(count)
    ]
