charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}-!"
n = len(charset)

def encrypt(message):
    encrypted = []
    for char in message:
        if char in charset:
            x = charset.index(char)
            y = pow(2, x, n+1)
            encrypted.append(charset[y])
    return ''.join(encrypted)

def decrypt(encrypted_message):
    decrypted = []
    for char in encrypted_message:
        if char in charset:
            y = charset.index(char)
            # Nous devons trouver x tel que 2^x ≡ y mod (n+1)
            # Cela peut être fait en essayant toutes les valeurs possibles de x
            for x in range(n):
                if pow(2, x, n+1) == y:
                    decrypted.append(charset[x])
                    break
    return ''.join(decrypted)

print("DECRYPTED FLAG : ", decrypt("828x6Yvx2sOnzMM4nI2sQ"))
