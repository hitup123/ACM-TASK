import hashlib
import random
from primePy import primes


class SchnorrZKProof:
    def __init__(self, p, q, g):
        self.p = p# any large prime number
        self.q = q# prime divisor of p-1
        self.g = g#generator

    def generate_hash(self, *args):
        hash_input = ''.join(map(str, args))
        hash_input_bytes = hash_input.encode('utf-8')
        sha256_hash = hashlib.sha256(hash_input_bytes)
        hex_digest = sha256_hash.hexdigest()
        return int(hex_digest, 16)

    def verify(self, public_key, commitment, response, challenge):
        lhs = pow(self.g, response, self.p)
        rhs = (commitment * pow(public_key, challenge, self.p)) % self.p
        return lhs == rhs
    
    def commitment(self):
        self.random_value = random.randint(0, self.q - 1)
        self.commitment = pow(self.g, self.random_value, self.p)
        return self.commitment  
     
    def response(self, challenge):
        self.response = (self.random_value + self.private_key * challenge) % self.q
        return self.response
    
    def keys(self):
        self.private_key = random.randint(0, self.q - 1)
        self.public_key = pow(self.g, self.private_key, self.p)
        return self.public_key

   

    
length=15 
def nextPrime(i):
    if(i%2==0):
        i=i+1
    while(1):
        if( primes.check(i)):
                break
        i+=2
    return i
def prime():
    q = nextPrime(random.randint(int("9"*(length-1))+1,int("9"*length)))  # Generate a 15-bit prime for q

    k = 2
    p = k * q + 1
    while not primes.check(p):
        k += 1
        p = k * q + 1
    return p, q

def generator(p, q):
    g = 2
    while g < p - 1:
        if pow(g, (p-1)//q, p) != 1:
            return g
        g += 1
p, q = prime()
g = generator(p, q)




zkp = SchnorrZKProof(p, q, g)
public_key = zkp.keys()
commitment = zkp.commitment()


challenge_input = str(commitment) + str(public_key) + str(g)
challenge = zkp.generate_hash(challenge_input)


response = zkp.response(challenge)


verified = zkp.verify(public_key, commitment, response, challenge)


print('Public Key:', public_key)
print('Commitment:', commitment)
print('Challenge:', challenge)
print('Response:', response)
print('Verified:', verified)
    

