import hashlib
import random
import secrets
import string
from statistics import mean


class HashAttackExperiment:

    def __init__(self, userString, bitMaskSize):
        self.original_string = userString
        self.bit_count = bitMaskSize
        self.bit_mask = self.generate_bit_mask(bitMaskSize)
        self.original_string_truncated_hash = self.get_truncated_sha1_hash(self.original_string)
        self.run_experiment()

    def generate_bit_mask(self, b):
        return int('1' * b, 2)

    def run_experiment(self):
        attempts_list = []
        trials = 0
        # We'll do 50 trials
        while trials < 50:
            # Keep track of how many attempts
            attempts = 0
            # Generate random string
            r = self.generate_random_string()
            r_hash = self.get_truncated_sha1_hash(r)
            while r_hash != self.original_string_truncated_hash:
                attempts += 1
                r = self.generate_random_string()
                r_hash = self.get_truncated_sha1_hash(r)
            attempts_list.append(attempts)
            trials += 1
            print("TRIAL #{} TOOK {} ATTEMPTS".format(trials, attempts))

            # Compare to regular hash
            # Output to average and bit size
            trials += 1
        print("The average attempts for a collision of a {}-bit hash was {}".format(self.bit_count, mean(attempts_list)))

    def get_truncated_sha1_hash(self, s):
        sha1 = hashlib.sha1(s)
        bin_hash = int.from_bytes(bytearray(sha1.digest()), 'big')
        return bin_hash & self.bit_mask

    def countTotalBits(self, num):
        # convert number into it's binary and
        # remove first two characters 0b.
        binary = bin(num)[2:]
        return len(binary)

    def generate_random_string(self):
        l = random.randint(5, 8)
        rand = ''.join(secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range(l))
        return rand.encode('utf-8')