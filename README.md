# Python-LWE
Latice based encryption using the LWE method, made in python

## Objective
Create a modulized example of the Learning With Errors encryption method. This method uses the idea of the complexity of the reversability of matricies with induced errors.

## Procedure
The first steps of this method is to identify the constants q, n, and m. For first attempts at this project, I tried to define them dynamically but this effected decryption in adverse ways. As a result, I statically defined them as follows: <br>
q=2<sup>16</sup> (modulus operator) <br>
n=2<sup>10</sup> (width of array A) <br>
m=n+2<sup>6</sup> (height of array A)<br>

### Key Generation
LWE is a asymmetric key encryption with public and private keys generated during encryption. To make these keys, 3 matrices are used: A, s, and e. <br>
-A is a matrix defined to have the dimensions n\*m with random values in the range [0, q). <br>
-s is a matrix defined to have the dimensions 1\*n with random values in the range [0, q). This is the private key (aka secret matrix).<br>
-e is a matrix defined to have the dimensions 1\*m with random values in the set {0, 1}. This is the error matrix, used to increase difficulty of reversing the primary key.<br>
These matrices are combined in a fashion to create a matrix b so that b=(A\*s+e)%q. The public key is (A,b)<br>
To store the keys I used a method to convert the keys to strings, compressed them, and then encoded them, which made it easier to store in a text file.

### Encryption
To encrypt a single bit (B) we create two matrices c<sub>1</sub> and c<sub>2</sub>. These matricies rely on a random matrix with dimensions 1\*m with values in the set {0, 1} <br>
C<sub>1</sub>=(A<sup>**T**</sup>r)%q  <br>
C<sub>2</sub>=(b<sup>**T**</sup>r+(q/2)*B)%q  <br>
The cipher text is the pair (C<sub>1</sub>, C<sub>2</sub>). To store this I converted it to string, compressed it, and encoded it.

### Decryption
Given the encoded ciphertext, I converted back into it's matrix version, and then had to run the following algorithms on it:
v=(C<sub>1</sub><sup>**T**</sup>s)%q<br>
d=(C<sub>2</sub>-v)%q<br>
The value d is the original bit, but is slightly off due to the errors introduced during encryption. To determine the value, we round the bit as follows:
```python
if abs(d-0) < abs(d-(q/2)):
     d=0
else: 
    d=1
```
## POINTS OF INTEREST
Right now due the algorithm can only encrypt 1 bit (0 or 1) at a time. While this can be looped, it is not practical given the size of the [ciphertext](./examples/ciphertext.txt) which was compressed before encoding.<br>
Private keys and Public keys have their own classes that allow them to be saved. Due to problems using `np.matrix` as a super for the private key class, I had to use `tuple` instead with the second value of the tuple being `None`. This seemed to resolve errors.<br>
I considered using `zlib` instead of `gzip`, but there was no visible increase in compression.

## SOURCE OF DESCRIPTION:
https://en.wikipedia.org/wiki/Lattice-based_cryptography<br>
https://en.wikipedia.org/wiki/Learning_with_errors<br>
https://chatgpt.com/share/80bde10d-bc5d-43cc-90cf-0d0443eb3b46