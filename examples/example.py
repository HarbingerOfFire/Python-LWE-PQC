#WARNING: Do not attempt to run here. Move to same directory as encrypt.py
import encrypt

plaintext=b"Hello World"

#can only support bits of 0 or 1 right now
e=encrypt.encrypt(plaintext)
pub, priv = e.gen_keys()

pub.save()
priv.save()

ciphertext=e.encrypt()
d=e.decrypt(ciphertext)
print(ciphertext)
print(d)

assert d==plaintext