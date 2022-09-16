import socket
import threading
import time
import json

# def update_led(strand, status):
#     if strand == "windows":
#         if status == "complete": # 
            # Call function or put code to update the strand pattern/status
        # else:
            # Call function or put code to update strands progress bar



def handle(conn_addr, addr):
  with conn_addr as conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # conn.sendall(data)
            # print(json.loads(data))
            data_dict = json.loads(data) # returns data in the following format: {'id': 'Windows', 'data': 97}
            # update_led(data_dict.get('id'), data_dict.get('data'))





HOST = ''
PORT = 65432
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
  s.bind((HOST,PORT))
except socket.error as e:
  print(str(e))


s.listen(2)

while True:
  conn, addr = s.accept()
  threading.Thread(target=handle, args=(conn,addr)).start()


print("Should never be reached")

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print(f"Connected by {addr}")
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             conn.sendall(data)
