# from ast import Load
# from concurrent.futures import thread
import platform, os
import getpass

# from numpy import true_divide
from loader import Loader, progress
from time import sleep, time
import settings
# import functions
import multiprocessing
import menu
from colorama import Fore
# import queue
# import threading

if settings.USE_MPI:
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    cluster_size = comm.Get_size()
else:
    rank = 0
    cluster_size = 1
    start_number = rank

# class alphabet:
#     def __init__(self):
#         self.array = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
#     def update(self, password):
#         self.array = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
#         if any(map(str.isupper, password)) or settings.FORCE_CAPITALS:
#             self.array = self.array + ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
#         return self.array
#     def length(self):
#         return len(self.array)
#     def item(self, x):
#         return self.array[x]
#     def index(self, index):
#         return self.array.index(index)
#     def arrayitem(self):
#         return self.array
# alphabet = alphabet()

# def setup_alphabet(password):
#     global alphabet
#     alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
#     if any(map(str.isupper, password)) or settings.FORCE_CAPITALS:
#         alphabet = alphabet + ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]


# if settings.ALLOW_CAPITALS:
#     alphabet = alphabet + ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

# if settings.ALLOW_NUMBERS:
#     alphabet.append("0","1","2","3","4","5","6","7","8","9")

# if settings.ALLOW_SPECIAL:
#     alphabet.append(["!","?","@","#","$"])

# alphabet_length = len(alphabet)

def clear_console():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def print_worker(queues, event, progress):
    # i = 0
    while True:
        # i += 
        value = []
        if event.is_set():
            break
        # for q in queues:
            # print(q.get())
            # value.append(q.get())
        # print(value)
        progress.update(queues[0].get())

        sleep(0.20)

def _decompose2(number, alphabet):
    """Generate digits from `number` in base alphabet, most significants
    bits first.
    """
    # number -= 1  # Account for A in base alphabet being 1 in decimal rather than 0
    if number < len(alphabet):
        yield number
    else:
        number, remainder = divmod(number, len(alphabet))
        yield from _decompose2(number, alphabet)
        yield remainder

def base_10_to_alphabet2(number, alphabet):
    """Convert a decimal number to its base alphabet representation"""
    # print(alphabet.arrayitem())
    letter_combined = ''
    for part in _decompose2(number, alphabet):
        letter_combined = letter_combined + alphabet[(part-1)]
    return letter_combined
    # return ''.join(
    #         alphabet[part]
    #         for part in _decompose2(number)
    # )

def base_arr_to_10(letters, alphabet):
    """Convert an alphabet to its decimal representation based on a dictionary"""
    letters_num = 0
    for i, letter in enumerate(reversed(letters)):
        letters_num += (alphabet.index(letter) + 1) * len(alphabet)**i

    return letters_num

def password_crack(thread_number, q, f, encoded_password, alphabet):
    # print(current_process().pid)
    start = time()
    attempts = 0
        # for attempt in range(start_number, end_number, cluster_size * 2):
    threaded_start = (rank * settings.THREADS) + thread_number
    curr_attempt = threaded_start
    # f = open('E:/report.txt', 'w')
    while True:
        if (attempts % 100000) == 0:
            if q.is_set():
                break
            # pipe.put(curr_attempt)
            # p.put([thread_number, base_10_to_alphabet2(curr_attempt)])
            if thread_number == 0:
                print(Fore.WHITE, base_10_to_alphabet2(curr_attempt, alphabet), Fore.WHITE)
            elif thread_number == 1:
                print(Fore.RED, base_10_to_alphabet2(curr_attempt, alphabet), Fore.WHITE)
            elif thread_number == 2:
                print(Fore.GREEN, base_10_to_alphabet2(curr_attempt, alphabet), Fore.WHITE)
            elif thread_number == 3:
                print(Fore.BLUE, base_10_to_alphabet2(curr_attempt, alphabet), Fore.WHITE)
        if curr_attempt == encoded_password:
            print("Node ", rank+1, " Thread ", thread_number, " found the password")
            break
        # elif curr_attempt > encoded_password:
        #     print("node falied to find password")
        #     break
        else:
            # print("guess: ", curr_attempt)
            # f.write("Guess: " + base_10_to_alphabet2(curr_attempt) +'\n')
            curr_attempt += cluster_size * settings.THREADS
            attempts += 1
    # print(encoded_password, curr_attempt)
    if rank == 0:
        end = round(time() - start, 2)
        # print("Node ", thread_number, " made ", attempts, " attempts")
        # print("Nodes + Threads: ", str(cluster_size), " + ", str(args.threads))
        if thread_number == 0:
            print('Time elapsed: ' + str(end) + ' seconds')
        # q.put('Found')
        f.set()

def all_true(iterable):
    for item in iterable:
        if not item.is_alive():
            return False
    return True


if __name__ == '__main__':
    if rank == 0:
        clear_console()
        while True:
            try:
                print(menu.title_screen)
                print(menu.open_screen)
                password = input("Please enter a password to try and crack:")
                # print(alphabet.update(password))
                # print(alphabet)

                symbols = ["!","@","#","$","%","?"]
                alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
                if any(map(str.isupper, password)) or settings.FORCE_CAPITALS:
                    alphabet = alphabet + ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
                if any(map(str.isdigit,password)):
                    alphabet = alphabet + ["1","2","3","4","5","6","7","8","9","0"]
                if any([char in password for char in symbols]):
                    alphabet = alphabet + ["!","@","#","$","%","?"]
                # encoded_password = base_arr_to_10(password, alphabet)

                encoded_password = base_arr_to_10(password, alphabet)
                start = time()

                if settings.USE_MPI:
                    data = {"alphabet": alphabet, "password": encoded_password}
                    request = comm.bcast(data, root=0)
                    print(request)

                # with Loader("Checking password:" , "Password: ✔"):
                    # sleep(5)
                q = multiprocessing.Queue()
                quit = multiprocessing.Event()
                found = multiprocessing.Event()
                threads = []
                pipes = []
                for i in range(0, settings.THREADS):
                    # pipe = multiprocessing.Queue()
                    # child.close()
                    p = multiprocessing.Process(target=password_crack, args=(i,quit,found, encoded_password, alphabet))
                    threads.append(p)
                    # pipes.append(pipe)
                    p.start()
                    # p.join()
                # while not found.wait():
                #     print(pipes)
                #     for p in pipes:
                #         # if not p.empty():
                #         print(p.get())
                # while True:
                #     if found.is_set():
                #         print("found")
                #         break
                #     else:
                #         print("not found")

                prog = progress(encoded_password)
                # c = threading.Thread(target=print_worker,args=(pipes, found, prog), daemon=True)
                # c.start()
                # c.join()
                found.wait()

                # while found:
                #     for q in pipes:
                #         if not q.empty():
                #             print(q.get())

                quit.set()
                loader = Loader("Waiting for threads to clean up", "All threads closed").start()
                while all_true(threads):
                    #do nothing
                    sleep(0.5)
                    pass
                loader.stop()

                # for i in range (0,15):

                #     sleep(1)

                input("please press enter")
                clear_console()
            except KeyboardInterrupt:
                print('Interrupted')
                clear_console()
                break
    else:
        data = None
        request = comm.bcast(data,root=0)
        print("received request")