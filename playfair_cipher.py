
def clean(text):
    text = text.upper().replace("J", "I")
    return "".join(ch for ch in text if "A" <= ch <= "Z")


def make_matrix(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    letters = ""

    for ch in clean(key) + alphabet:
        if ch not in letters:
            letters += ch

    matrix = []
    for i in range(0, 25, 5):
        matrix.append(list(letters[i:i+5]))

    return matrix


def prepare(text):
    text = clean(text)
    result = ""
    i = 0

    while i < len(text):
        a = text[i]
        filler = "Q" if a == "X" else "X"

        if i + 1 == len(text) or a == text[i+1]:
            b = filler
            i += 1
        else:
            b = text[i+1]
            i += 2

        result += a + b

    return result


def find(matrix, letter):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == letter:
                return row, col


def playfair(text, matrix, mode):
    result = ""
    shift = 1 if mode == "E" else -1

    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]

        r1, c1 = find(matrix, a)
        r2, c2 = find(matrix, b)

        if r1 == r2:
            a = matrix[r1][(c1 + shift) % 5]
            b = matrix[r2][(c2 + shift) % 5]

        elif c1 == c2:
            a = matrix[(r1 + shift) % 5][c1]
            b = matrix[(r2 + shift) % 5][c2]

        else:
            a = matrix[r1][c2]
            b = matrix[r2][c1]

        result += a + b

    return result


key = input("Enter key: ")
matrix = make_matrix(key)

print("\nPlayfair Matrix:")
for row in matrix:
    print(" ".join(row))

choice = input("\nE for Encrypt, D for Decrypt: ").upper()

if choice == "E":
    message = input("Enter message: ")
    message = prepare(message)
    print("Prepared Text:", message)
    print("Encrypted Text:", playfair(message, matrix, "E"))

elif choice == "D":
    message = clean(input("Enter encrypted text: "))
    if len(message) % 2 == 0:
        print("Decrypted Text:", playfair(message, matrix, "D"))
        print("Remove filler X/Q manually if needed.")
    else:
        print("Invalid ciphertext length.")

else:
    print("Invalid choice.")
