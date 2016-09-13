
import hexmap


def test_main():
    assert hexmap  # use your library here

def test_insert():
	hexMap = hexmap.HexMap()
	hexes = [hexmap.Hex(x,x+1,x-1) for x in range(50)]
	for h in hexes:
		hexMap.set(h, h.q)

def test_retrieval():
	hexMap = hexmap.HexMap()
	hexes = [hexmap.Hex(x,x+1,x-1) for x in range(50)]
	for h in hexes:
		hexMap.set(h, h.q)

	for h in hexes:
		result = hexMap.get(h)
		assert h.q == result
