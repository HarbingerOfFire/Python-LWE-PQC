from keygen import *

class encrypt:
    def __init__(self, buffer:bytes=None) -> None:
        self.buffer=self.bytes_to_binary_list(buffer)

    def gen_keys(self):
        self.pubkey, self.privkey=generate()
        return self.pubkey, self.privkey
    
    def bytes_to_binary_list(self, byte_string):
        binary_list = []
        for byte in byte_string:
            # Convert each byte to an 8-bit binary string, then convert to integers and add to the list
            binary_list.extend([int(bit) for bit in f'{byte:08b}'])
        return binary_list

    def binary_list_to_bytes(self, binary_list):
        byte_string = bytearray()
        for i in range(0, len(binary_list), 8):
            byte = ''.join(str(bit) for bit in binary_list[i:i+8])
            byte_string.append(int(byte, 2))
        return bytes(byte_string)

    def encode_cipher(self, ciphertext):
        c1, c2 = ciphertext
        data={
            "c1":c1,
            "c2":c2,
        }
        data=gzip.compress(json.dumps(data).encode())
        return base64.b64encode(data)

    def decode_cipher(self, ciphertext):
        data=base64.b64decode(ciphertext)
        data=json.loads(gzip.decompress(data))
        return (data["c1"],data["c2"])

    def encrypt(self, plaintext:str=None, pubkey:pubkey=None):
        if pubkey!=None:
            self.pubkey=pubkey
        r=gen_r()
        a,b=self.pubkey
        m=self.buffer
        c1 = [(R * A) % q for R, A in zip(r, a)]
        c2 = [((R * B) + (M * (q // 2))) % q for R, B, M in zip(r, b, m)]
        return self.encode_cipher((c1, c2))
    
    def decrypt(self, ciphertext:str=None, privkey:privkey=None):
        if ciphertext != None:
            self.buffer=ciphertext
        if privkey != None:
            self.privkey=privkey
        ciphertext=self.decode_cipher(self.buffer)
        s=self.privkey[0]
        c1, c2 = ciphertext
        m_1 = [(C1 * S) % q for C1, S in zip(c1, s)]
        d = [(C2 - M1) % q for C2, M1 in zip(c2, m_1)]
        for i in range(len(d)):
            if abs(d[i]-0) < abs(d[i]-(q//2)):
                d[i]=0
            else:
                d[i]=1
        return self.binary_list_to_bytes(d)