from py_ecc import bn128 as b
from curve import Scalar
import json

# Mimics the Poseidon hash for params:
#
# p                    = b.curve_order
# security level       = 128
# alpha                = 5
# input size           = 2
# t (inner state size) = 3
# full round count     = 8 (4 on each side)
# partial round count  = 56
#
# Tested compatible with the implementation at
# https://github.com/ingonyama-zk/poseidon-hash

rc = [
    [Scalar(a), Scalar(b), Scalar(c)]
    for (a,b,c) in json.load(open('test/poseidon_rc.json'))
]

mds = [Scalar(1) / i for i in range(3, 8)]

def poseidon_hash(in1, in2):
    L, M, R = Scalar(in1), Scalar(in2), Scalar(0)
    for i in range(64):
        L = (L + rc[i][0]) ** 5
        M += rc[i][1]
        R += rc[i][2]
        if i < 4 or i >= 60:
            M = M ** 5
            R = R ** 5

        (L, M, R) = (
            (L * mds[0] + M * mds[1] + R * mds[2]),
            (L * mds[1] + M * mds[2] + R * mds[3]),
            (L * mds[2] + M * mds[3] + R * mds[4]),
        )
    return M
