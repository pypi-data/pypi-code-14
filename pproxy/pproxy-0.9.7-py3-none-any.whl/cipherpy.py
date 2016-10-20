import hashlib, struct, base64

from pproxy.cipher import BaseCipher

# Pure Python Ciphers
ROL = lambda a, b: ((a&((1<<(32-b))-1))<<b)|((a>>(32-b))&((1<<b)-1))

class Table_Cipher(BaseCipher):
    LIBRARY = False
    KEY_LENGTH = 0
    IV_LENGTH = 0
    def setup(self):
        if self.key in self.CACHE:
            self.encrypt_table, self.decrypt_table = self.CACHE[self.key]
        else:
            a, _ = struct.unpack('<QQ', hashlib.md5(self.key).digest())
            table = list(range(256))
            for i in range(1, 1024):
                table.sort(key = lambda x: a % (x + i))
            self.encrypt_table = bytes(table)
            self.decrypt_table = bytes.maketrans(self.encrypt_table, bytes(range(256)))
            self.CACHE[self.key] = self.encrypt_table, self.decrypt_table
    def decrypt(self, s):
        return bytes.translate(s, self.decrypt_table)
    def encrypt(self, s):
        return bytes.translate(s, self.encrypt_table)

class StreamCipher(BaseCipher):
    LIBRARY = False
    def setup(self):
        self.stream = self.core()
    def encrypt(self, s):
        return bytes(i^next(self.stream) for i in s)
    decrypt = encrypt

class RC4_Cipher(StreamCipher):
    KEY_LENGTH = 16
    IV_LENGTH = 0
    def core(self):
        data = list(range(256))
        y = 0
        for x in range(256):
            y = (self.key[x % self.KEY_LENGTH] + data[x] + y) & 0xff
            data[x], data[y] = data[y], data[x]
        x = y = 0
        while 1:
            x = (x+1) & 0xff
            y = (y+data[x]) & 0xff
            data[x], data[y] = data[y], data[x]
            yield data[(data[x]+data[y]) & 0xff]

class RC4_MD5_Cipher(RC4_Cipher):
    IV_LENGTH = 16
    def setup(self):
        self.key = hashlib.md5(self.key + self.iv).digest()
        RC4_Cipher.setup(self)

class ChaCha20_Cipher(StreamCipher):
    KEY_LENGTH = 32
    IV_LENGTH = 8
    def core(self):
        ORDERS = ((0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
                  (0, 5, 10, 15), (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14)) * 10
        data = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574] + \
                    list(struct.unpack('<IIIIIIII', self.key)) + [0]
        if self.IV_LENGTH == 8:
            data += [0] + list(struct.unpack('<II', self.iv))
        else:
            data += list(struct.unpack('<III', self.iv))
        while 1:
            H = data[:]
            for a, b, c, d in ORDERS:
                H[a] = (H[a]+H[b]) & 0xffffffff
                H[d] = ROL(H[d]^H[a], 16)
                H[c] = (H[c]+H[d]) & 0xffffffff
                H[b] = ROL(H[b]^H[c], 12)
                H[a] = (H[a]+H[b]) & 0xffffffff
                H[d] = ROL(H[d]^H[a], 8)
                H[c] = (H[c]+H[d]) & 0xffffffff
                H[b] = ROL(H[b]^H[c], 7)
            H = [(H[i]+data[i])&0xffffffff for i in range(16)]
            data[12] = (data[12]+1) & 0xffffffff
            if not data[12]:
                data[13] = (data[13]+1) & 0xffffffff
            for i in struct.pack('<IIIIIIIIIIIIIIII', *H):
                yield i

class ChaCha20_IETF_Cipher(ChaCha20_Cipher):
    IV_LENGTH = 12

class Salsa20_Cipher(StreamCipher):
    KEY_LENGTH = 32
    IV_LENGTH = 8
    def core(self):
        data = [0x61707865] + list(struct.unpack('<IIII', self.key[:16])) + \
               [0x3320646e] + list(struct.unpack('<II', self.iv)) + \
               [0, 0] + [0x79622d32] + list(struct.unpack('<IIII', self.key[16:])) + \
               [0x6b206574]
        ORDERS = ((4, 0, 12, 8), (9, 5, 1, 13), (14, 10, 6, 2), (3, 15, 11, 7),
                  (1, 0, 3, 2), (6, 5, 4, 7), (11, 10, 9, 8), (12, 15, 14, 13)) * 10
        while 1:
            H = data[:]
            for a, b, c, d in ORDERS:
                H[a] ^= ROL(H[b]+H[c], 7)
                H[d] ^= ROL(H[a]+H[b], 9)
                H[c] ^= ROL(H[d]+H[a], 13)
                H[b] ^= ROL(H[c]+H[d], 18)
            H = [(H[i]+data[i])&0xffffffff for i in range(16)]
            data[8] = (data[8]+1) & 0xffffffff
            if not data[8]:
                data[9] = (data[9]+1) & 0xffffffff
            for i in struct.pack('<IIIIIIIIIIIIIIII', *H):
                yield i

class CFBCipher(StreamCipher):
    def setup(self):
        self.bitmode = self.SEGMENT_SIZE % 8 != 0
        self.stream = self.core()
        self.last = None
        self.cipher = self.CIPHER(self.key)
    def process(self, s, inv=False):
        r = bytearray()
        for i in s:
            if self.bitmode:
                j = 0
                for k in range(7,-1,-1):
                    ibit = (i>>k)&1
                    jbit = ibit^self.stream.send(self.last)
                    j |= jbit<<k
                    self.last = ibit if inv else jbit
            else:
                j = i^self.stream.send(self.last)
                self.last = i if inv else j
            r.append(j)
        return bytes(r)
    def encrypt(self, s):
        return self.process(s, False)
    def decrypt(self, s):
        return self.process(s, True)
    def core(self):
        if self.bitmode:
            next_iv = int.from_bytes(self.iv, 'big')
            mask = (1 << (self.IV_LENGTH*8)) - 1
            while 1:
                data = self.cipher.encrypt(next_iv.to_bytes(self.IV_LENGTH, 'big'))
                next_iv = (next_iv << self.SEGMENT_SIZE) & mask
                for i in range(self.SEGMENT_SIZE):
                    next_iv |= (yield (data[i//8]>>(7-i%8))&1)<<(self.SEGMENT_SIZE-1-i)
        else:
            next_iv = bytearray(self.iv)
            segment_byte = self.SEGMENT_SIZE // 8
            while 1:
                data = self.cipher.encrypt(next_iv)
                del next_iv[:segment_byte]
                for i in range(segment_byte):
                    next_iv.append((yield data[i]))

class CTRCipher(StreamCipher):
    def setup(self):
        self.stream = self.core()
        self.cipher = self.CIPHER(self.key)
    def encrypt(self, s):
        return bytes(i^next(self.stream) for i in s)
    decrypt = encrypt
    def core(self):
        next_iv = bytearray(self.iv)
        while 1:
            data = self.cipher.encrypt(next_iv)
            yield from data
            for i in range(len(next_iv)-1,-1,-1):
                if next_iv[i] != 255:
                    next_iv[i] += 1
                    break
                else:
                    next_iv[i] = 0

class OFBCipher(StreamCipher):
    def core(self):
        data = self.iv
        while 1:
            data = self.cipher.encrypt(data)
            yield from data

class AES:
    g1 = base64.b64decode(b'Y3x3e/Jrb8UwAWcr/terdsqCyX36WUfwrdSir5ykcsC3/ZMmNj/3zDSl5fFx2DEVBMcjwxiWBZoHEoDi6yeydQmDLBobblqgUjvWsynjL4RT0QDtIPyxW2rLvjlKTFjP0O+q+0NNM4VF+QJ/UDyfqFGjQI+SnTj1vLbaIRD/89LNDBPsX5dEF8Snfj1kXRlzYIFP3CIqkIhG7rgU3l4L2+AyOgpJBiRcwtOsYpGV5HnnyDdtjdVOqWxW9Opleq4IunglLhymtMbo3XQfS72LinA+tWZIA/YOYTVXuYbBHZ7h+JgRadmOlJseh+nOVSjfjKGJDb/mQmhBmS0PsFS7Fg==')
    g2 = [((a<<1)&0xff)^0x1b if a&0x80 else a<<1 for a in g1]
    g3 = [a^(((a<<1)&0xff)^0x1b if a&0x80 else a<<1) for a in g1]
    Rcon = base64.b64decode(b'jQECBAgQIECAGzZs2KtNmi9evGPGlzVq1LN9+u/FkTly5NO9YcKfJUqUM2bMgx06dOjL')
    shifts = tuple((j,j&3|((j>>2)+(j&3))*4&12,(j+3)&3|((j>>2)+((j+3)&3))*4&12,(j+2)&3|((j>>2)+((j+2)&3))*4&12,(j+1)&3|((j>>2)+((j+1)&3))*4&12) for j in range(16))
    def __init__(self, key):
        size = len(key)
        if size == 16: nbr = 10
        elif size == 24: nbr = 12
        elif size == 32: nbr = 14
        else: raise Exception('Unknown key length')
        ekey = bytearray(key)
        while len(ekey) < 16*(nbr+1):
            t = ekey[-4:]
            if len(ekey) % size == 0:
                t = [self.g1[i] for i in t[1:]+t[:1]]
                t[0] ^= self.Rcon[len(ekey)//size%51]
            if size == 32 and len(ekey) % size == 16:
                t = [self.g1[i] for i in t]
            for m in t:
                ekey.append(ekey[-size] ^ m)
        self.ekey = tuple(ekey[i*16:i*16+16] for i in range(nbr+1))
    def encrypt(self, data):
        s = [data[j]^self.ekey[0][j] for j in range(16)]
        for key in self.ekey[1:-1]:
            s = [self.g2[s[a]]^self.g1[s[b]]^self.g1[s[c]]^self.g3[s[d]]^key[j] for j,a,b,c,d in self.shifts]
        return bytes(self.g1[s[self.shifts[j][1]]]^self.ekey[-1][j] for j in range(16))

class AES_256_CFB_Cipher(CFBCipher):
    KEY_LENGTH = 32
    IV_LENGTH = 16
    SEGMENT_SIZE = IV_LENGTH*8
    CIPHER = AES

class AES_192_CFB_Cipher(AES_256_CFB_Cipher):
    KEY_LENGTH = 24

class AES_128_CFB_Cipher(AES_256_CFB_Cipher):
    KEY_LENGTH = 16

class AES_256_CFB8_Cipher(AES_256_CFB_Cipher):
    SEGMENT_SIZE = 8

class AES_192_CFB8_Cipher(AES_256_CFB8_Cipher):
    KEY_LENGTH = 24

class AES_128_CFB8_Cipher(AES_256_CFB8_Cipher):
    KEY_LENGTH = 16

class AES_256_CFB1_Cipher(AES_256_CFB_Cipher):
    SEGMENT_SIZE = 1

class AES_192_CFB1_Cipher(AES_256_CFB1_Cipher):
    KEY_LENGTH = 24

class AES_128_CFB1_Cipher(AES_256_CFB1_Cipher):
    KEY_LENGTH = 16

class AES_256_CTR_Cipher(CTRCipher):
    KEY_LENGTH = 32
    IV_LENGTH = 16
    CIPHER = AES

class AES_192_CTR_Cipher(AES_256_CTR_Cipher):
    KEY_LENGTH = 24

class AES_128_CTR_Cipher(AES_256_CTR_Cipher):
    KEY_LENGTH = 16

class AES_256_OFB_Cipher(OFBCipher):
    KEY_LENGTH = 32
    IV_LENGTH = 16
    CIPHER = AES

class AES_192_OFB_Cipher(AES_256_OFB_Cipher):
    KEY_LENGTH = 24

class AES_128_OFB_Cipher(AES_256_OFB_Cipher):
    KEY_LENGTH = 16

MAP = {name[:-7].replace('_', '-').lower()+'-py': cls for name, cls in globals().items() if name.endswith('_Cipher')}

