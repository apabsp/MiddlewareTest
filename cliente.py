# cliente.py
import socket

HOST = '127.0.0.1'
PORT = 5000  # Porta do middleware

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))
    print("Conectado ao middleware!")
    
    while True:
        msg = input("Digite operação (ex: soma 2 3) ou 'sair': ")
        if msg.lower() == "sair":
            break
        cliente.sendall(msg.encode())
        resposta = cliente.recv(1024).decode()
        print("Resposta:", resposta)
