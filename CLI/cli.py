import platform, os
import getpass
from loader import Loader
from time import sleep, time
import settings
import functions
import multiprocessing

if settings.USE_MPI:
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    cluster_size = comm.Get_size()
else:
    rank = 0
    cluster_size = 1
    start_number = rank

alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

if settings.ALLOW_CAPITALS:
    alphabet.append(["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"])

if settings.ALLOW_NUMBERS:
    alphabet.append("0","1","2","3","4","5","6","7","8","9")

if settings.ALLOW_SPECIAL:
    alphabet.append(["!","?","@","#","$"])

alphabet_length = len(alphabet)

def clear_console():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


if __name__ == '__main__':
    clear_console()
    while True:
        try:
            password = getpass.getpass("Please enter a password to try and crack:")

            encoded_password = functions.base_arr_to_10(password, alphabet)
            start = time()
            
            # with Loader("Checking password:" , "Password: ✔"):
                # sleep(5)
            q = multiprocessing.Queue()
            quit = multiprocessing.Event()
            found = multiprocessing.Event()
            threads = []
            for i in range(0, settings.THREADS):
                p = multiprocessing.Process(target=functions.password_crack, args=(i,quit,found, rank, encoded_password, alphabet))
                p.start()
                # threads.append(p)
                # p.join()
            found.wait()

            quit.set()
            input("please press enter")
            clear_console()
        except KeyboardInterrupt:
            print('Interrupted')
            clear_console()
            break