from multiprocessing import Process, Pipe
from time import sleep

def f(conn):
    conn.send([42, None, 'hello'])
    conn.send('hello')
    sleep(2)
    conn.send('test message')
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    print(parent_conn.recv())
    parent_conn.recv()
    p.join()