import argparse
from audioop import mul
from multiprocessing.dummy import current_process
import threading
import multiprocessing
import time
# password = ''
# minimum = 0
# threads = 0
parser = argparse.ArgumentParser(description='Password testing software')
parser.add_argument('password', metavar='N', type=str, help='The password you want to try and crack')
parser.add_argument('-m', '--min', default=1, type=int, help='The minimum amount of characters in the password')
parser.add_argument('-t', '--threads', type=int, choices=range(1,9), default=1 ,help='The maximum amount of threads you want to use')

args = parser.parse_args()

# print(args.password)
# print(args.min)
# print(args.threads)

rank = 0
cluster_size = 1
start_number = rank

alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","d","E","F","G","H","I","J","K","L","M","N","O","P","q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"]
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


password = args.password
# passmin = sys.argv.get(2)
# passmax = sys.argv.get(3)
# print(passmin)
# print(passmax)
encoded_password = base_arr_to_10(password)

start = time.time()



# results = comm.gather(attempts, root=0)

# print(encoded_password, curr_attempt)
# if rank == 0:
#     end = round(time.time() - start, 2)
#     print("Found password in ", attempts, " attempts")
#     print("Nodes: ", str(cluster_size))
#     print('Time elapsed: ' + str(end) + ' seconds')

def password_crack(thread_number, q):
    # print(current_process().pid)
    attempts = 0
        # for attempt in range(start_number, end_number, cluster_size * 2):
    threaded_start = (rank * args.threads) + thread_number
    curr_attempt = threaded_start
    # f = open('E:/report.txt', 'w')
    while True:
        if (attempts % 1000000) == 0:
            if thread_number == 0:
                print(base_10_to_alphabet2(curr_attempt))
            elif thread_number == 1:
                print("\t" + base_10_to_alphabet2(curr_attempt))
            elif thread_number == 2:
                print("\t\t" + base_10_to_alphabet2(curr_attempt))
            elif thread_number == 3:
                print("\t\t\t" + base_10_to_alphabet2(curr_attempt))
        if curr_attempt == encoded_password:
            print("Node ", rank+1, " Thread ", thread_number, " found the password")
            break
        # elif curr_attempt > encoded_password:
        #     print("node falied to find password")
        #     break
        else:
            # print("guess: ", curr_attempt)
            # f.write("Guess: " + base_10_to_alphabet2(curr_attempt) +'\n')
            curr_attempt += cluster_size * args.threads
            attempts += 1
    print(encoded_password, curr_attempt)
    if rank == 0:
        end = round(time.time() - start, 2)
        print("Node made ", attempts, " attempts")
        print("Nodes + Threads: ", str(cluster_size), " + ", str(args.threads))
        print('Time elapsed: ' + str(end) + ' seconds')
        q.put('Found')

# password_crack()
# for i in range(0, args.threads):
#     # print(i)
#     # password_crack(i)
#     t = threading.Thread(target=password_crack, args=(i,))
#     t.start()
#     t.join()

# threads = []

# for i in range(0, args.threads):
#     thread = multiprocessing.Process(target=password_crack, args=(i,))
#     threads.append(thread)
#     thread.start()

# # you need to wait for the threads to finish
# for thread in threads:
#     thread.join()

if __name__ == '__main__':
    q = multiprocessing.Queue()
    threads = []
    for i in range(0, args.threads):
        p = multiprocessing.Process(target=password_crack, args=(i,q,))
        p.start()
        threads.append(p)
        # p.join()

    while True:
        if q.get() == "Found":
            print('Tread found password. Terminating other threads.')
            for i in threads:
                if i.is_alive():
                    i.terminate()
                    i.join()
        break