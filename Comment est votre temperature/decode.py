def crc8(data):
    crc = 0xFF
    polynomial = 0x31
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
            crc &= 0xFF
    return crc

def decode_i2c_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    transitions = []
    for line in lines:
        line = line.strip()
        if not line or ',' not in line:
            continue
        try:
            scl_str, sda_str = line.split(',')
            transitions.append((int(scl_str), int(sda_str)))
        except ValueError:
            continue  # ignore lignes incorrectes

    prev_scl, prev_sda = 1, 1
    bits = []
    in_transaction = False
    decoded = []

    for i in range(1, len(transitions)):
        scl, sda = transitions[i]

        # START
        if prev_sda == 1 and sda == 0 and scl == 1:
            in_transaction = True
            bits = []
            decoded.append(f"{i}: START")
        
        # STOP
        elif prev_sda == 0 and sda == 1 and scl == 1 and in_transaction:
            in_transaction = False
            decoded.append(f"{i}: STOP")
            process_i2c_bits(bits, decoded)
            bits = []

        # SCL rising edge = clock data bit
        if in_transaction and prev_scl == 0 and scl == 1:
            bits.append(sda)

        prev_scl, prev_sda = scl, sda

    return decoded

def process_i2c_bits(bits, decoded):
    if len(bits) < 9:
        decoded.append("  Incomplet (moins de 9 bits)")
        return

    i = 0
    frame = []

    def next_byte():
        nonlocal i
        if i + 8 > len(bits):
            return None
        val = 0
        for _ in range(8):
            val = (val << 1) | bits[i]
            i += 1
        return val

    def next_bit():
        nonlocal i
        if i >= len(bits):
            return None
        b = bits[i]
        i += 1
        return b

    # Première trame : maître écrit commande
    addr = next_byte()
    rw = addr & 0x01
    address = (addr >> 1) & 0x7F
    ack1 = next_bit()

    decoded.append(f"  Addr: 0x{address:02X}, {'Read' if rw else 'Write'}, ACK={ack1 == 0}")

    if rw == 0:  # Write (maître -> esclave)
        cmd = next_byte()
        ack2 = next_bit()
        decoded.append(f"  CMD: 0x{cmd:02X}, ACK={ack2 == 0}")

    else:  # Read (esclave -> maître)
        data1 = next_byte()
        ack1 = next_bit()
        data2 = next_byte()
        ack2 = next_bit()
        crc = next_byte()
        nack = next_bit()

        decoded.append(f"  DATA1: 0x{data1:02X}, ACK={ack1 == 0}")
        decoded.append(f"  DATA2: 0x{data2:02X}, ACK={ack2 == 0}")
        decoded.append(f"  CRC: 0x{crc:02X}, NACK={nack == 1}")

        # Vérification CRC
        crc_calc = crc8([data1, data2])
        if crc == crc_calc:
            decoded.append(f"  ✓ CRC OK")
        else:
            decoded.append(f"  ✗ CRC MISMATCH (attendu 0x{crc_calc:02X})")

# Exemple d'utilisation
if __name__ == "__main__":
    output = decode_i2c_from_file("sample.txt")
    for line in output:
        print(line)
