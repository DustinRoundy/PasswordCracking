from mpi4py import MPI
import time
import sys
# from test import base_arr_to_10, base_10_to_alphabet2
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
cluster_size = comm.Get_size()
# rank = 0
# cluster_size = 1
# start_number = rank

alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
alphabet_length = len(alphabet)

def _decompose2(number):
    """Generate digits from `number` in base alphabet, most significants
    bits first.
    """

    # number -= 1  # Account for A in base alphabet being 1 in decimal rather than 0
    if number < alphabet_length:
        yield number
    else:
        number, remainder = divmod(number, alphabet_length)
        yield from _decompose2(number)
        yield remainder

def base_10_to_alphabet2(number):
    """Convert a decimal number to its base alphabet representation"""
    letter_combined = ''
    for part in _decompose2(number):
        letter_combined = letter_combined + alphabet[(part-1)]
    return letter_combined
    # return ''.join(
    #         alphabet[part]
    #         for part in _decompose2(number)
    # )

def base_arr_to_10(letters):
    """Convert an alphabet to its decimal representation based on a dictionary"""
    letters_num = 0
    for i, letter in enumerate(reversed(letters)):
        letters_num += (alphabet.index(letter) + 1) * alphabet_length**i

    return letters_num


password = sys.argv[1]
# passmin = sys.argv.get(2)
# passmax = sys.argv.get(3)
# print(passmin)
# print(passmax)
encoded_password = base_arr_to_10(password)

start = time.time()

attempts = 0


# for attempt in range(start_number, end_number, cluster_size * 2):
curr_attempt = start_number
# f = open('E:/report.txt', 'w')
while True:
    if curr_attempt == encoded_password:
        break
    elif curr_attempt > encoded_password:
        print("node falied to find password")
        break
    else:
        # print("guess: ", curr_attempt)
        # f.write("Guess: " + base_10_to_alphabet2(curr_attempt) +'\n')
        curr_attempt += cluster_size
        attempts += 1

# results = comm.gather(attempts, root=0)

# print(encoded_password, curr_attempt)
if rank == 0:
    end = round(time.time() - start, 2)
    print("Found password in ", attempts, " attempts")
    print("Nodes: ", str(cluster_size))
    print('Time elapsed: ' + str(end) + ' seconds')