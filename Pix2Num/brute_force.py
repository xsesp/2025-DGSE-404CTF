import sys
from PIL import Image

sys.set_int_max_str_digits(100000)

WIDTH = 400
HEIGHT = 200

def convert_image(image_path):
    image = Image.open(image_path).convert('L')
    pixels = list(image.getdata())
    binary_representation = ''.join(['1' if pixel == 255 else '0' for pixel in pixels])
    return int(binary_representation, 2)

def encrypt_number(number, key):
    new_number = 0
    shift = 0
    while number:
        bloc = (number & 0xFFFF_FFFF_FFFF_FFFF) ^ key
        new_number |= (bloc << shift)
        number >>= 64
        shift += 64
    return new_number

def decrypt_number(encrypted_number, key):
    new_number = 0
    shift = 0
    while encrypted_number:
        bloc = (encrypted_number & 0xFFFF_FFFF_FFFF_FFFF) ^ key
        new_number |= (bloc << shift)
        encrypted_number >>= 64
        shift += 64
    return new_number

def number_to_image(number, output_path):
    binary_representation = bin(number)[2:]
    binary_representation = binary_representation.zfill(WIDTH * HEIGHT)
    pixels = [255 if bit == '1' else 0 for bit in binary_representation]
    image = Image.new('L', (WIDTH, HEIGHT))
    image.putdata(pixels)
    image.save(output_path)

# Lire le nombre chiffré à partir du fichier number.txt
with open('number.txt', 'r') as file:
    encrypted_number = int(file.read())

# Supposer un bloc clair de 64 bits de pixels blancs
known_clear_block = int('1' * 64, 2)

# Calculer la clé
cipher_block = encrypted_number & 0xFFFF_FFFF_FFFF_FFFF
key = known_clear_block ^ cipher_block

# Déchiffrer le nombre
decrypted_number = decrypt_number(encrypted_number, key)

# Reconstruire l'image
number_to_image(decrypted_number, 'reconstructed_flag.png')

print(f"Clé trouvée : {key}")
print("Image reconstruite : reconstructed_flag.png")

