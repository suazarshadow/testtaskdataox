import random

USER_AGENT = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0",
    "Mozilla/5.0 (X11; Linux x86_64) Firefox/120.0",
    "Mozilla/5.0 (Linux; Android 13) Chrome/120.0",
]


def getUserAgent():
    return random.choice(USER_AGENT)
