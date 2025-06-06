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

data = [0xa8, 0x9c]
checksum = crc8(data)
print(f"0x{checksum:02X}")

