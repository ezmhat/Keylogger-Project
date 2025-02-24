class Encryptor:
    def __init__(self, key: str):
        self.key = key

    def xor_encrypt(self, data: str) -> str:
        encrypted_chars = [chr(ord(c) ^ ord(self.key[i % len(self.key)])) for i, c in enumerate(data)]
        return "".join(encrypted_chars)

    def encrypt(self, data: str) -> str:
        encrypted_data = self.xor_encrypt(data)
        return encrypted_data.encode('utf-8').hex()

    def decrypt(self, encrypted_hex: str) -> str:
        encrypted_data = bytes.fromhex(encrypted_hex).decode('utf-8')
        return self.xor_encrypt(encrypted_data)

