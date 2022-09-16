from mpi4py import MPI
import time
import sys
import json
import socket
# from test import base_arr_to_10, base_10_to_alphabet2
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
cluster_size = comm.Get_size()
# rank = 0
# cluster_size = 1
start_number = rank

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


class Progress:
    def __init__(self, max, found, server="Cluster"):
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


password = sys.argv[1]
# passmin = sys.argv.get(2)
# passmax = sys.argv.get(3)
# print(passmin)
# print(passmax)
encoded_password = base_arr_to_10(password)

start = time.time()

attempts = 0
progress = Progress(encoded_password, None)
progress.update(0)


# for attempt in range(start_number, end_number, cluster_size * 2):
curr_attempt = start_number
# f = open('E:/report.txt', 'w')
while True:
    if curr_attempt == encoded_password:
        progress.complete()
        break
    elif curr_attempt > encoded_password:
        print("node falied to find password")
        break
    else:
        if rank == 0:
            progress.update(curr_attempt)
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