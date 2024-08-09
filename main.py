import serial
import socket
import time

class SerialTCPParser:
    def __init__(self, mode='serial', serial_port=None, baudrate=9600, tcp_host=None, tcp_port=None):
        self.mode = mode
        self.serial_port = serial_port
        self.baudrate = baudrate
        self.tcp_host = tcp_host
        self.tcp_port = tcp_port
        self.connection = None

        if self.mode == 'serial':
            self.connection = serial.Serial(self.serial_port, self.baudrate, timeout=1)
        elif self.mode == 'tcp':
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.tcp_host, self.tcp_port))

    def read_data(self):
        if self.mode == 'serial':
            data = self.connection.readline().decode().strip()
        elif self.mode == 'tcp':
            data = self.connection.recv(1024).decode().strip()
        return data

    def send_data(self, data):
        if self.mode == 'serial':
            self.connection.write(data.encode())
        elif self.mode == 'tcp':
            self.connection.send(data.encode())

    def parse_data(self, data):
        if data == "GET_A":
            return "A_10V"
        elif data == "GET_B":
            return "B_5V"
        elif data == "GET_C":
            return "C_15A"
        else:
            return "UNKNOWN_COMMAND"

    def close(self):
        if self.connection:
            self.connection.close()

def main():
    mode = input("Введите режим работы (serial/tcp): ").strip().lower()

    if mode == "serial":
        port = input("Введите порт: ")
        parser = SerialTCPParser(mode='serial', serial_port=port, baudrate=9600)
    elif mode == "tcp":
        host = input("Введите IP адрес: ")
        port = int(input("Введите порт: "))
        parser = SerialTCPParser(mode='tcp', tcp_host=host, tcp_port=port)
    else:
        print("Неподдерживаемый режим. Используйте «serial» или «tcp».")
        exit()

    try:
        while True:
            data = parser.read_data()
            if data:
                print(f"Received: {data}")
                response = parser.parse_data(data)
                parser.send_data(response)
                print(f"Sent: {response}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        parser.close()

if __name__ == "__main__":
    main()
