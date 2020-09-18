import sys

from hash_attack_experiment import HashAttackExperiment


def main(argv):
    global string_to_hash, num_bits
    if len(argv) != 2:
        string_to_hash, num_bits = prompt()
    else:
        string_to_hash = argv[0].encode('utf-8')
        num_bits = int(argv[1])

    hashAttackExperiment = HashAttackExperiment(string_to_hash, num_bits)

def prompt():
    print("############################################################################")
    print("Command Line Usage: >> python main.py <stringToHash> <#ofBitsHashShouldBe>")
    print("If you prefer to pass in arguments via the terminal, press CTR+C and start over.")
    print("############################################################################", end='\n\n')
    s = input("Please give the string that you want to hash ---> ").encode('utf-8')
    n = int(input("Please give the number of bits the hash should be ---> "))
    return s, n

if __name__ == '__main__':
    main(sys.argv[1:])

