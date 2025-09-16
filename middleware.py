# middleware.py
import socket
from cryptography.fernet import Fernet 

CLIENTE_PORT = 5000  # Recebe req5sições do cliente
SERVIDOR_PORT = 8080  # Repassa para o servidor
HOST = '127.0.0.1'

def log(mensagem):
    with open("middleware.log", "a") as f:
        f.write(mensagem + "\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mw:
    mw.bind((HOST, CLIENTE_PORT))
    mw.listen()
    print(f"Middleware escutando em {HOST}:{CLIENTE_PORT}...")

    chave = Fernet.generate_key()
    fernet = Fernet(chave)

    while True:
        conn_cliente, addr = mw.accept()
        with conn_cliente:
            print(f"Cliente conectado: {addr}")
            dados = conn_cliente.recv(1024).decode()
            if not dados:
                break
            
            # Aqui o middleware pode modificar, autenticar, logar...
            log(f"Recebido do cliente: {dados}")
            encryption = fernet.encrypt(str(dados).encode("utf-8"))
            print(f'fernet: {encryption}')
            
            if "div" in dados and dados[2] == 0:
                print("Divisão por 0 não deve ser possível") 
            # Repassa ao servidor
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, SERVIDOR_PORT))
                s.sendall(dados.encode())
                resposta = s.recv(1024).decode()
            
            # Aqui o middleware pode alterar a resposta antes de devolver
            log(f"Resposta do servidor: {resposta}")
            conn_cliente.sendall(resposta.encode())
