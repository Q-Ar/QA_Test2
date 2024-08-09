import socket
from threading import Thread
import time

def tcp_emulator(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"TCP сервер запущен на {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключено устройство с адреса: {addr}")

        while True:
            client_socket.sendall("GET_A\n".encode())
            time.sleep(1)  # Пауза между отправкой сообщений
            client_socket.sendall("GET_B\n".encode())
            time.sleep(1)
            client_socket.sendall("GET_C\n".encode())
            time.sleep(1)
            client_socket.sendall("void\n".encode())
            time.sleep(1)

            # Чтение ответа от сервера
            response = client_socket.recv(1024).decode().strip()
            print(f"Ответ сервера: {response}")

        client_socket.close()


if __name__ == "__main__":
    emulator_thread = Thread(target=tcp_emulator, args=("localhost", 5000))
    emulator_thread.start()
