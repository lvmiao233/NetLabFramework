import threading
import queue
from socket_util import socket_client

def client_emulation(host, port, result_queue):
    try:
        client = socket_client.SocketClient(host, port)
        client.connect()
        response = client.receive_messages()
        result_queue.put(response)
    except Exception as e:
        result_queue.put(e)

def server_threading_test(host, port, num_threads):
    results_queue = queue.Queue()
    threads = []
    for _ in range(int(num_threads)):
        thread = threading.Thread(target=client_emulation, args=(host, int(port), results_queue))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    # 收集所有线程的结果
    results = [results_queue.get() for _ in range(num_threads)]
    return results