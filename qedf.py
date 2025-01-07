import socket
import random
import threading
from queue import Queue

ip_queue = Queue()

NUM_THREADS = 250

def generate_random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def check_port(ip):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((ip, 23))
            print(f"{ip}")
    except (socket.timeout, ConnectionRefusedError):
        pass
    except Exception as e:
        print(f"[Error] {ip}: {e}")

def worker():
    while not ip_queue.empty():
        ip = ip_queue.get()
        check_port(ip)
        ip_queue.task_done()

def main():
    while True:
        ip_queue.put(generate_random_ip())

    threads = []
    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
