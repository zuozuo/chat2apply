import ipdb; ipdb.set_trace(context=5)

# content of test_sample.py
def inc(x):
    return x + 1


def test_answer():
    assert inc(4) == 5
