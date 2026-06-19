import threading
from queue import Queue

total_palavras = 0
lock = threading.Lock()

def contar_palavras(nome_arquivo, fila):
    global total_palavras

    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            texto = arquivo.read()

        quantidade = len(texto.split())

        with lock:
            total_palavras += quantidade

        fila.put((nome_arquivo, quantidade))

    except Exception as erro:
        print(f"Erro ao processar {nome_arquivo}: {erro}")
        fila.put((nome_arquivo, 0))

arquivos = [
    "arquivo1.txt",
    "arquivo2.txt",
    "arquivo3.txt",
    "arquivo4.txt"
]

fila = Queue()
threads = []

for arquivo in arquivos:
    t = threading.Thread(
        target=contar_palavras,
        args=(arquivo, fila)
    )

    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\nResultado por arquivo:")

while not fila.empty():
    nome, qtd = fila.get()
    print(f"{nome}: {qtd} palavras")

print(f"\nTotal geral: {total_palavras} palavras")