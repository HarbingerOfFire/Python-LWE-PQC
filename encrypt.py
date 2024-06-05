from keygen import *

class encrypt:
    def __init__(self, buffer:int=None) -> None:
        self.buffer=buffer

    def gen_keys(self):
        self.pubkey, self.privkey=generate()
        return self.pubkey, self.privkey
    
    def encrypt_bit(self, pubkey=None):
        if pubkey!=None:
            self.pubkey=pubkey
        r=gen_r()
        c1=(self.pubkey[0].transpose() * r) % q
        c2=(self.pubkey[1].transpose() * r + (q//2)*self.buffer)%q
        return self.encode_cipher((c1, c2))
    
    def encode_cipher(self, ciphertext):
        c1, c2 = ciphertext
        data={
            "c1":c1.tolist(),
            "c2":c2.tolist(),
        }
        data=gzip.compress(json.dumps(data).encode())
        return base64.b64encode(data)
    
    def decrypt_bit(self, ciphertext, privkey=None):
        if type(privkey)!=type(None):
            self.privkey=privkey
        ciphertext=self.decode_cipher(ciphertext)
        v=(ciphertext[0].transpose()*self.privkey[0])%q
        d=((ciphertext[1]-v)%q)[0][0]
        if abs(d-0) < abs(d-(q//2)):
            d=0
        else:
            d=1
        return d
    
    def decode_cipher(self, ciphertext):
        data=base64.b64decode(ciphertext)
        data=json.loads(gzip.decompress(data))
        return (np.matrix(data["c1"]), np.matrix(data["c2"]))