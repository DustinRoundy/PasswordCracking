import settings
import time

# alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
# alphabet_length = len(alphabet)

def _decompose2(number, alphabet):
    """Generate digits from `number` in base alphabet, most significants
    bits first.
    """
    alphabet_length = len(alphabet)
    # number -= 1  # Account for A in base alphabet being 1 in decimal rather than 0
    if number < alphabet_length:
        yield number
    else:
        number, remainder = divmod(number, alphabet_length)
        yield from _decompose2(number)
        yield remainder

def base_10_to_alphabet2(number, alphabet):
    """Convert a decimal number to its base alphabet representation"""
    letter_combined = ''
    for part in _decompose2(number):
        letter_combined = letter_combined + alphabet[(part-1)]
    return letter_combined
    # return ''.join(
    #         alphabet[part]
    #         for part in _decompose2(number)
    # )

def base_arr_to_10(letters, alphabet):
    """Convert an alphabet to its decimal representation based on a dictionary"""
    alphabet_length = len(alphabet)
    letters_num = 0
    for i, letter in enumerate(reversed(letters)):
        letters_num += (alphabet.index(letter) + 1) * alphabet_length**i

    return letters_num


# password = args.password
# # passmin = sys.argv.get(2)
# # passmax = sys.argv.get(3)
# # print(passmin)
# # print(passmax)
# encoded_password = base_arr_to_10(password)

# start = time.time()



# results = comm.gather(attempts, root=0)

# print(encoded_password, curr_attempt)
# if rank == 0:
#     end = round(time.time() - start, 2)
#     print("Found password in ", attempts, " attempts")
#     print("Nodes: ", str(cluster_size))
#     print('Time elapsed: ' + str(end) + ' seconds')

def password_crack(thread_number, q, f, rank, encoded_password, alphabet):
    # print(current_process().pid)
    attempts = 0
        # for attempt in range(start_number, end_number, cluster_size * 2):
    threaded_start = (rank * settings.THREADS) + thread_number
    curr_attempt = threaded_start
    # f = open('E:/report.txt', 'w')
    while True:
        if (attempts % 100000) == 0:
            if q.is_set():
                break
            if thread_number == 0:
                print(curr_attempt)
            #     print(Fore.WHITE, base_10_to_alphabet2(curr_attempt), Fore.WHITE)
            # elif thread_number == 1:
            #     print(Fore.RED, base_10_to_alphabet2(curr_attempt), Fore.WHITE)
            # elif thread_number == 2:
            #     print(Fore.GREEN, base_10_to_alphabet2(curr_attempt), Fore.WHITE)
            # elif thread_number == 3:
            #     print(Fore.BLUE, base_10_to_alphabet2(curr_attempt), Fore.WHITE)
        if curr_attempt == encoded_password:
            print("Node ", rank+1, " Thread ", thread_number, " found the password")
            break
        # elif curr_attempt > encoded_password:
        #     print("node falied to find password")
        #     break
        else:
            # print("guess: ", curr_attempt)
            # f.write("Guess: " + base_10_to_alphabet2(curr_attempt) +'\n')
            curr_attempt += settings.NODES * settings.THREADS
            attempts += 1
    print(encoded_password, curr_attempt)
    if rank == 0:
        # end = round(time.time() - start, 2)
        # # print("Node ", thread_number, " made ", attempts, " attempts")
        # # print("Nodes + Threads: ", str(cluster_size), " + ", str(args.threads))
        # print('Time elapsed: ' + str(end) + ' seconds')
        # q.put('Found')
        f.set()