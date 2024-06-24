#one file version, just change m to the desired plaintext
from secrets import randbelow, choice

n = 2**10
q = 2**16
err = [0, 1]
# Generate random vectors
a = [randbelow(q) for _ in range(n)]
s = [randbelow(q) for _ in range(n)]
e = [choice(err) for _ in range(n)]
r = [choice(err) for _ in range(n)]

# Generate public key b
b = [((A * S) + E) % q for A, S, E in zip(a, s, e)]

def string_to_binary_list(input_string):
    binary_list = []
    for char in input_string:
        # Convert each character to its ASCII value
        ascii_value = ord(char)
        # Convert the ASCII value to an 8-bit binary number
        binary_string = format(ascii_value, '08b')
        # Extend the binary_list with the binary digits (as integers)
        binary_list.extend([int(bit) for bit in binary_string])
    return binary_list

def binary_list_to_string(binary_list):
    # Check if the binary list length is a multiple of 8
    if len(binary_list) % 8 != 0:
        raise ValueError("The binary list length must be a multiple of 8.")
    
    string_output = ""
    for i in range(0, len(binary_list), 8):
        # Get the next 8 bits
        byte = binary_list[i:i+8]
        # Convert the 8 bits to a string and then to an integer (base 2)
        ascii_value = int(''.join(map(str, byte)), 2)
        # Convert the ASCII value to a character and append to the result string
        string_output += chr(ascii_value)
    return string_output


# Example usage:
input_string = "Hello"*7
m = string_to_binary_list(input_string)
print(m)

print(len(m))

# Encrypt the message
c1 = [(R * A) % q for R, A in zip(r, a)]
c2 = [((R * B) + (M * (q // 2))) % q for R, B, M in zip(r, b, m)]

print(c2)
# Decrypt the message
m_1 = [(C1 * S) % q for C1, S in zip(c1, s)]
m_e = [(C2 - M1) % q for C2, M1 in zip(c2, m_1)]

# Decode the message
decoded_message = []
for d in m_e:
    if abs(d-0) < abs(d-(q/2)):
        decoded_message.append(0)
    else: 
        decoded_message.append(1)

print(binary_list_to_string(decoded_message))

assert m==decoded_message