
import hashlib
import math

# Step 1: Choose prime numbers
p = 61
q = 53

# Step 2: Calculate n and phi
n = p * q
phi = (p - 1) * (q - 1)

# Step 3: Choose public exponent
e = 17

if math.gcd(e, phi) != 1:
    print("Invalid value of e")
    exit()

# Step 4: Calculate private exponent
d = pow(e, -1, phi)

print("Public Key:", (e, n))
print("Private Key:", (d, n))

# Step 5: Take message from user
message = input("\nEnter message: ")

# Step 6: Generate message hash
hash_value = hashlib.sha256(message.encode()).hexdigest()
hash_num = int(hash_value, 16) % n

print("Message Hash:", hash_value)

# Step 7: Generate digital signature
signature = pow(hash_num, d, n)

print("Digital Signature:", signature)

# Step 8: Verify signature
verified_hash = pow(signature, e, n)

if verified_hash == hash_num:
    print("Signature Verified Successfully!")
else:
    print("Signature Verification Failed!")
