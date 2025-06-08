import itertools

ALPHA_KEYS = [
    "YOV60VVMI76QYYRB",
    "BEF54TMCYM0VE7OJ",
    "PIDL50ESBX2YFSL7",
    "UWIPS8W3G6W2S90T"
]

_rotator = itertools.cycle(ALPHA_KEYS)

def get_alpha_key():
    return next(_rotator)
