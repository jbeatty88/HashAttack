import hashlib
import random
import secrets
import string
from statistics import mean


class HashAttackExperiment:
    """Class representing an experiment of Hash Attacks on SHA1 digests

    Attributes:
        original_string: the original input string from the user
        bit_count: the number of bits the sha1 digests should be truncated to
        bit_mask: the mask that will be used to truncate all sha1 digests
        original_string_truncated_hash: the truncated digest of the original input string

    """
    def __init__(self, user_string, bit_mask_size):
        self.original_string = user_string
        self.bit_count = bit_mask_size
        self.bit_mask = self.generate_bit_mask(bit_mask_size)
        self.original_string_truncated_hash = self.get_truncated_sha1_hash(self.original_string)
        self.run_experiment()

    def generate_bit_mask(self, b):
        """Generate a bit mask of b bits to truncate a digest.

        Args:
            b: number of bits to make the mask

        Returns: an integer that represents the bit mask.

        """

        return int('1' * b, 2)

    def run_experiment(self):
        """Execute all the steps in the experiment.

        The different trial counts we're to allow analysis
        of how the average changes with more trials. This
        will quickly become infeasible through if the bit_count
        is greater than 18-bits.

        Returns: None, just outputs to stdout

        """

        trial_counts = [50, 100, 500, 1000, 5000]
        print('-------------------------------------------')
        for trials in trial_counts:
            self.do_collision_attack_experiment(trials)
        self.do_collision_attack_experiment(10000)

        print('-------------------------------------------')
        for trials in trial_counts:
            self.do_pre_image_attack_experiment(trials)
        # self.do_pre_image_attack_experiment(10000)
        print('-------------------------------------------')

    def do_collision_attack_experiment(self, trial_count):
        """Execute the collision attack experiment.

        The collision attack experiment generates random strings,
        hashes them with sha1, and then check to see if that hash
        has been previously found. If it hasn't we add it to the list
        of hashes already found.

        Args:
            trial_count: integer representing how many time to run this experiment

        Returns: None, just prints to stdout

        """

        attempts_list = []
        trials = 0
        while trials < trial_count:
            # Keep track of how many attempts
            attempts = 0
            hash_list = [self.original_string_truncated_hash]
            r_hash = 0
            while r_hash not in hash_list:
                hash_list.append(r_hash)
                r = self.generate_random_string()
                r_hash = self.get_truncated_sha1_hash(r)
                attempts += 1
            attempts_list.append(attempts)
            trials += 1
            # print("TRIAL #{} TOOK {} ATTEMPTS".format(trials, attempts))

            trials += 1
        print(
            "The average attempts for {} trials of collision attack of a {}-bit hash was {}".format(trial_count,
                                                                                                    self.bit_count,
                                                                                                    mean(
                                                                                                        attempts_list)))

    def do_pre_image_attack_experiment(self, trial_count):
        """Execute the pre-image attack experiment.

        The pre-image attack experiment generates a random string, hashes it,
        truncates it, then compares it with the input string's hash. If it isn't
        a match, it tries again. We don not store any hashes that have been seen
        before. The preimage is either an exact match or not.

        Args:
            trial_count: integer representing how many times to run the experiment.

        Returns: None, just outputs to stdout

        """

        attempts_list = []
        trials = 0
        while trials < trial_count:
            # Keep track of how many attempts
            attempts = 0
            r_hash = 0
            while r_hash != self.original_string_truncated_hash:
                attempts += 1
                r = self.generate_random_string()
                r_hash = self.get_truncated_sha1_hash(r)
            attempts_list.append(attempts)
            trials += 1
            # print("TRIAL #{} TOOK {} ATTEMPTS".format(trials, attempts))

            # Compare to regular hash
            # Output to average and bit size
            trials += 1
        print(
            "The average attempts for {} trials of pre-image attack of a {}-bit hash was {}".format(trial_count,
                                                                                                    self.bit_count,
                                                                                                    mean(
                                                                                                        attempts_list)))

    def get_truncated_sha1_hash(self, s):
        """Generate a hash for a string and truncate it.

        Use the sha1 encryption algorithm to compute the hash

        Args:
            s: string to be hashed

        Returns: a truncated hash of the string

        """

        sha1 = hashlib.sha1(s)
        bin_hash = int.from_bytes(bytearray(sha1.digest()), 'big')
        # print(bin(bin_hash & self.bit_mask))
        return bin_hash & self.bit_mask

    def countTotalBits(self, num):
        """Count the total number of bits in a number.

        Count how many bits are in a number. This is just
        a utility function that assisted in verifying correct
        truncation of the hashes.

        Args:
            num: number to check bits

        Returns: integer representing how many bits are in this number.

        """

        # convert number into it's binary and
        # remove first two characters 0b.
        binary = bin(num)[2:]
        return len(binary)

    def generate_random_string(self):
        """Generate a random string.

        Generate a random 5-8 char alphanumeric string.

        Returns: a random string

        """
        l = random.randint(5, 8)
        rand = ''.join(
            secrets.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range(l))
        return rand.encode('utf-8')
