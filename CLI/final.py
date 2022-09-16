import argparse
import multiprocessing
# from sre_constants import SRE_FLAG_VERBOSE
import time
import socket
import json
from colorama import Fore
# from loader import Loader

parser = argparse.ArgumentParser(description='Password testing software')
parser.add_argument('password', metavar='N', type=str, help='The password you want to try and crack')
# parser.add_argument('-m', '--min', default=1, type=int, help='The minimum amount of characters in the password')
parser.add_argument('-t', '--threads', type=int, choices=range(1,129), default=1 ,help='The maximum amount of threads you want to use')

args = parser.parse_args()

rank = 0

# def print_worker(queues, event, progress):
#     # i = 0
#     while True:
#         # i += 
#         value = []
#         if event.is_set():
#             break
#         # for q in queues:
#             # print(q.get())
#             # value.append(q.get())
#         # print(value)
#         progress.update(queues[0].get())

#         sleep(0.20)

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


password = args.password

symbols = ["!","@","#","$","%","?"]
alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
if any(map(str.isupper, password)):
    alphabet = alphabet + ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
if any(map(str.isdigit,password)):
    alphabet = alphabet + ["1","2","3","4","5","6","7","8","9","0"]
if any([char in password for char in symbols]):
    alphabet = alphabet + ["!","@","#","$","%","?"]

def password_crack(thread_number, q, f, encoded_password, alphabet, progress):
    # print(current_process().pid)
    attempts = 0
        # for attempt in range(start_number, end_number, cluster_size * 2):
    threaded_start = thread_number
    curr_attempt = threaded_start
    # f = open('E:/report.txt', 'w')
    while True:
        if (attempts % 100000) == 0:
            if q.is_set():
                break
            progress.update(curr_attempt)
            if thread_number == 0:
                print(Fore.WHITE, base_10_to_alphabet2(curr_attempt), Fore.WHITE)
            elif thread_number == 1:
                print(Fore.RED, base_10_to_alphabet2(curr_attempt), Fore.WHITE)
            elif thread_number == 2:
                print(Fore.GREEN, base_10_to_alphabet2(curr_attempt), Fore.WHITE)
            elif thread_number == 3:
                print(Fore.BLUE, base_10_to_alphabet2(curr_attempt), Fore.WHITE)
        if curr_attempt == encoded_password:
            print("Thread ", thread_number, " found the password")
            progress.complete()
            break
        # elif curr_attempt > encoded_password:
        #     print("node falied to find password")
        #     break
        else:
            # print("guess: ", curr_attempt)
            # f.write("Guess: " + base_10_to_alphabet2(curr_attempt) +'\n')
            curr_attempt += args.threads
            attempts += 1
    # print(encoded_password, curr_attempt)
    if rank == 0:
        if thread_number == 0:
            end = round(time.time() - start, 2)
            # print("Node ", thread_number, " made ", attempts, " attempts")
            # print("Nodes + Threads: ", str(cluster_size), " + ", str(args.threads))
            print('Time elapsed: ' + str(end) + ' seconds')
        # q.put('Found')
        f.set()

encoded_password = base_arr_to_10(password, alphabet)
start = time.time()

class Progress:
    def __init__(self, max, found, server="Windows"):
        self.HOST = ["192.168.1.242", "192.168.1.243"]
        self.PORT = 65432
        self.FOUND = found
        self.CONNECTED = False
        self.MAX = max
        self.id = server
        self.percent = 0
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        self.connect()

    def connect(self):
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOCKET1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # loader = Loader("Attempting to connect to server", "Connected!").start()
        try:
            print("attempting to connect to server") #connect to 1.242 and 1.243
            self.SOCKET.settimeout(5)
            self.SOCKET1.settimeout(5)
            self.SOCKET.connect((self.HOST[0], self.PORT))
            self.SOCKET1.connect((self.HOST[0], self.PORT))
            self.CONNECTED = True
            print("connected")
            # loader.stop()
            # self.SOCKET.sendall(str.encode(json.dumps({"data":"1234"})))
            # self.SOCKET = s
        except:
            print("failed to connect")
            # loader.update("Failed to Connect")
            # loader.stop()

    def update(self, status):
        if self.CONNECTED:
            percentage = int(round((status / self.MAX) * 100, 0))
            if percentage <= 99:
                if percentage > self.percent:
                    if percentage != self.percent:
                        self.SOCKET.sendall(str.encode(json.dumps({"id":self.id,"data": percentage})))
                        self.SOCKET1.sendall(str.encode(json.dumps({"id":self.id,"data": percentage})))
                        self.percent = percentage
            # if percentage == 100:
            #     if self.FOUND.is_set():
            #         self.SOCKET.sendall(str.encode(json.dumps({"data": "complete"})))
    
    def close(self):
        if self.CONNECTED:
            self.SOCKET.close()
            self.SOCKET1.close()
            self.CONNECTED = False

    def complete(self):
        if self.CONNECTED:
            self.SOCKET.sendall(str.encode(json.dumps({"id":self.id,"data": "complete"})))
            self.SOCKET1.sendall(str.encode(json.dumps({"id":self.id,"data": "complete"})))



if __name__ == '__main__':
    # HOST = "127.0.0.1"  # The server's hostname or IP address
    # PORT = 65432  # The port used by the server

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.connect((HOST, PORT))
    #     s.sendall(str.encode(json.dumps({"data":"1234"})))
    #     # data = s.recv(1024)
   

    q = multiprocessing.Queue()
    quit = multiprocessing.Event()
    found = multiprocessing.Event()
    progress = Progress(encoded_password, found)
    progress.update(0)
    threads = []
    for i in range(0, args.threads):
        p = multiprocessing.Process(target=password_crack, args=(i,quit,found, encoded_password, alphabet, progress))
        p.start()

    found.wait()

    quit.set()

