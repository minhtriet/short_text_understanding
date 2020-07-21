from nerd import NERD
import json

def test_apple(loop):
    n = NERD('apple')
    assert n.status == 200
    assert json.loads(n.json)

