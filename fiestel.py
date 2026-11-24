
def feistel(block, key, rounds, mode):
    half = len(block) // 2

    left = int(block[:half], 2)
    right = int(block[half:], 2)

    limit = (1 << half) - 1

    keys = []
    for i in range(rounds):
        keys.append((sum(key.encode()) + i) & limit)

    if mode == "D":
        keys.reverse()

    for k in keys:
        if mode == "E":
            left, right = right, left ^ (right ^ k)
        else:
            left, right = right ^ (left ^ k), left

    return format(left, f"0{half}b") + format(right, f"0{half}b")


def encrypt(message, key, block_size, rounds):
    bits = "".join(format(b, "08b") for b in message.encode())
    length = len(bits)

    while len(bits) % block_size != 0:
        bits += "0"

    result = ""

    for i in range(0, len(bits), block_size):
        block = bits[i:i+block_size]
        result += feistel(block, key, rounds, "E")

    return str(length) + ":" + result


def decrypt(ciphertext, key, block_size, rounds):
    length_text, bits = ciphertext.split(":")
    length = int(length_text)

    if len(bits) % block_size != 0:
        raise ValueError("Invalid block length")

    result = ""

    for i in range(0, len(bits), block_size):
        block = bits[i:i+block_size]
        result += feistel(block, key, rounds, "D")

    result = result[:length]

    data = bytes(int(result[i:i+8], 2)
                 for i in range(0, len(result), 8))

    return data.decode()


# Main program

choice = input("E for Encrypt, D for Decrypt: ").upper()
key = input("Enter secret key: ")
block_size = int(input("Enter block size (16, 32, 64): "))
rounds = int(input("Enter number of rounds: "))

if not key or block_size < 16 or block_size % 16 != 0 or rounds < 1:
    print("Invalid key, block size or rounds.")

elif choice == "E":
    message = input("Enter message: ")
    print("Ciphertext:", encrypt(message, key, block_size, rounds))

elif choice == "D":
    ciphertext = input("Enter ciphertext: ")
    try:
        print("Plaintext:", decrypt(ciphertext, key, block_size, rounds))
    except (ValueError, UnicodeDecodeError):
        print("Invalid ciphertext, key or settings.")

else:
    print("Invalid choice.")
