import random

# Example free proxy list (for demo/testing only)
# For production, use a paid proxy provider for reliability.
PROXIES = [
    'http://51.158.68.68:8811',
    'http://138.201.5.11:3128',
    'http://134.209.29.120:3128',
    'http://159.89.49.217:3128',
    'http://165.22.81.30:3128',
    'http://178.62.193.19:3128',
    # Add more proxies or load from a file/service
]

def get_random_proxy():
    """Return a random proxy from the list."""
    return random.choice(PROXIES)
