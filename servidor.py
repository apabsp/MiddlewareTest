# servidor.py
import socket

HOST = '127.0.0.1'
PORT = 8080 # Servidor escuta em outra porta

def processar_operacao(operacao):
    try:
        op, x, y = operacao.split()
        x, y = int(x), int(y)
        if op == "soma":
            return str(x + y)
        elif op == "sub":
            return str(x - y)
        elif op == "mult":
            return str(x * y)
        elif op == "div":
            return str(x / y)
        else:
            return "Operação inválida"
    except Exception as e:
        return f"Erro: {e}"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"Servidor escutando em {HOST}:{PORT}...")
    while True:
        conn, addr = servidor.accept()
        with conn:
            print(f"Conectado a {addr}")
            dados = conn.recv(1024).decode()
            if not dados:
                break
            resposta = processar_operacao(dados)
            conn.sendall(resposta.encode())