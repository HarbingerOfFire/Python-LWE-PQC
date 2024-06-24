# Python-LWE
Latice based encryption using the LWE method, made in python

## Objective
Create a modulized example of the Learning With Errors encryption method. This method uses the idea of the complexity of polynomials with induced errors.

## Procedure
The first steps of this method is to identify the constants q and n. For first attempts at this project, I tried to define them dynamically but this effected decryption in adverse ways. As a result, I statically defined them as follows: <br>
q=2<sup>16</sup> (modulus operator) <br>
n=2<sup>10</sup> (width of array A) <br>

### Key Generation
LWE is a asymmetric key encryption with public and private keys generated during encryption. To make these keys, 3 polynomiasl are used: A, s, and e. <br>
-A is a polynomial defined to have coefficients in the range [0, q) and n terms
-s is a polynomial defined to have coefficients in the range [0, q) and n terms This is the private key (aka secret polynomial).<br>
-e is a polynomial defined to have coefficients in the set {0,1} and n terms. This is the error polynomial, used to increase difficulty of reversing the primary key.<br>
These polynomials are combined in a fashion to create a polynomial b so that b=(A\*s+e)%q. The public key is (A,b)<br>
To store the keys I used a method to convert the keys to strings, compressed them, and then encoded them, which made it easier to store in a text file.

### Encryption
To encrypt a buffer (B) we create two polynomials c<sub>1</sub> and c<sub>2</sub>. These polynomials rely on a polynomial, r, defined to have coefficients in the set {0,1} and n terms. Note that B must beconverted to a binary list before going through this cipher. <br>
C<sub>1</sub>=(A\*>r)%q  <br>
C<sub>2</sub>=(b\*r+(q//2)*B)%q  <br>
The cipher text is the pair (C<sub>1</sub>, C<sub>2</sub>). To store this, I converted it to string, compressed it, and encoded it.

### Decryption
Given the encoded ciphertext, I converted back into it's polynomial version, and then had to run the following algorithms on it:<br>
v=(C<sub>1</sub>\*s)%q<br>
d=(C<sub>2</sub>-v)%q<br>
The value d is the original list of bits, but is slightly off (by up to q) due to the errors introduced during encryption. To determine the value, we round the each bit as follows:
```python
if abs(d-0) < abs(d-(q/2)):
     d=0
else: 
    d=1
```
## POINTS OF INTEREST
Private keys and Public keys have their own classes that allow them to be saved. I used `tuple` as a superclass instead with the second value of the tuple being `None` for the private key bue to errors in an earlier version of this code.<br>
I considered using `zlib` instead of `gzip` to compress, but there was no visible increase in compression.

## SOURCE OF DESCRIPTION:
https://en.wikipedia.org/wiki/Lattice-based_cryptography<br>
https://en.wikipedia.org/wiki/Learning_with_errors<br>