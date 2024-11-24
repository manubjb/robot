import socket

# Set up the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 2025))
endereco_servidor = ("127.0.0.1", 2024)

def options():
    print(f"{'Comandos':-^20}")
    print(f"{'up':<10}\n{'down':<10}\n{'right':<10}\n{'left':<10}\n{'jump':<10}\n{'q(sair)':<10}\n")
    return input("Movimente ela: ").strip().lower()

# Send commands
try:
    while True:
        acao = options()
        if acao == 'q':
            break
        elif acao in ['up', 'down', 'left', 'right']:
            mensagem = f"controle;{acao}"
            sent = sock.sendto(mensagem.encode(), endereco_servidor)
            print(f"Comando enviado: {mensagem}")
        else:
            print("Comando inválido. Tente novamente")

finally:
    print("Fechando socket")
    sock.close()

