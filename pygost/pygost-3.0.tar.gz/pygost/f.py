from pygost.gost3410 import CURVE_PARAMS
from pygost.gost3410 import GOST3410Curve
curve = GOST3410Curve(*CURVE_PARAMS["GostR3410_2012_TC26_ParamSetA"])
from os import urandom
prv_raw = urandom(32)
from pygost.gost3410 import prv_unmarshal
prv = prv_unmarshal(prv_raw)
from pygost.gost3410 import public_key
pub = public_key(curve, prv)
from pygost.gost3410 import pub_marshal
from pygost.utils import hexenc
print("Public key is:", hexenc(pub_marshal(pub)))
from pygost import gost34112012256
data_for_signing = b"some data"
dgst = gost34112012256.new(data_for_signing).digest()
from pygost.gost3410 import sign
signature = sign(curve, prv, dgst, mode=2012)
from pygost.gost3410 import verify
print(verify(curve, pub, dgst, signature, mode=2012))
