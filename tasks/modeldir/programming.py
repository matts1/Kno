from string import punctuation, whitespace

CHARSET = [
    set([]),
    set(whitespace),
    set(punctuation)
]

def check_output(actual:bytes, expected:str, status) -> int:  # returns an index in the list scores
    if status != 0:
        return {-9: 5, 1: 6}.get(status, 7)

    out = actual.decode('UTF-8')
    for i, chars in enumerate(CHARSET):
        out = ''.join([char for char in out if char not in chars])
        expected = ''.join([char for char in expected if char not in chars])
        if out == expected:
            return i

    if out.lower() == expected.lower():
        return 3

    return 4
