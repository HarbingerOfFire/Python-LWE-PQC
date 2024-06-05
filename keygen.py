import secrets
import numpy as np
import json, base64, gzip

q = 2**16
n = 2**10
m = n + 64

class pubkey(tuple):
    def __init__(self, publickey) -> None:
        self.key=publickey
        super().__init__()
    
    def __repr__(self):
        return self.key
    
    def save(self, filename="key.public"):
        A,b = self.key
        data={
            "A":A.tolist(),
            "b":b.tolist(),
        }
        data=gzip.compress(json.dumps(data).encode())
        data=base64.b64encode(data)
        open(filename, "wb").write(data)
    
    def load(self, filename="key.public"):
        data=open(filename, "rb").read()
        data=json.loads(gzip.decompress(base64.b64decode(data)))
        A=np.matrix(data["A"])
        b=np.matrix(data["b"])
        return pubkey((A,b))

class privkey(tuple):
    def __init__(self, privatekey) -> None:
        super().__init__()
        self.key=privatekey
    
    def __repr__(self):
        return self.key
    
    def save(self, filename="key.private"):
        s, none=self.key
        data={
            "s":s.tolist(),
        }
        data=gzip.compress(json.dumps(data).encode())
        data=base64.b64encode(data)
        open(filename, "wb").write(data)
    
    def load(self, filename="key.private"):
        data=open(filename, "rb").read()
        data=json.loads(gzip.decompress(base64.b64decode(data)))
        s=np.matrix(data["s"])
        return privkey((s, None))

def generate():
    A = np.matrix([[secrets.randbelow(q) for _ in range(n)] for _ in range(m)])
    s = np.matrix([secrets.randbelow(q) for _ in range(n)]).transpose()
    e = np.matrix([secrets.choice([0, 1]) for _ in range(m)]).transpose()
    b = (A * s + e) % q
    return pubkey((A, b)), privkey((s, None))

def gen_r():
    return np.matrix([secrets.choice([0, 1]) for _ in range(m)]).transpose()