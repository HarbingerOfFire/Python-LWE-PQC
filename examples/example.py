#WARNING: Do not attempt to run here. Move to same directory as encrypt.py
import encrypt

bit=1

#can only support bits of 0 or 1 right now
e=encrypt.encrypt(bit)
pub, priv = e.gen_keys()

pub.save()
priv.save()

ciphertext=e.encrypt_bit()
print(ciphertext)
d=e.decrypt_bit(ciphertext)
assert d==bit