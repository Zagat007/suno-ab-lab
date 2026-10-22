"""Deterministic Elo ranking for blind listening comparisons."""

def elo_update(a, b, winner, k=24):
    if winner not in ('a', 'b', 'tie'):
        raise ValueError('winner must be a, b, or tie')
    expected_a = 1 / (1 + 10 ** ((b - a) / 400))
    score_a = {'a': 1.0, 'b': 0.0, 'tie': 0.5}[winner]
    change = k * (score_a - expected_a)
    return a + change, b - change
