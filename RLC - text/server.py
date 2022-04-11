import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 4000))
s.listen(1)
clientSocket, address = s.accept()
print(f"Connection from {address} has been established!")


def compression_msg(message):
    compression_str = ""
    i = 0
    while (i <= len(message)-1):
        count = 1
        ch = message[i]
        j = i
        while (j < len(message)-1):
            if (message[j] == message[j + 1]):
                count = count + 1
                j = j + 1
            else:
                break
        compression_str = compression_str + str(count) + ch
        i = j + 1
    return compression_str


def decompression_msg(our_message):
    decompression_str = ""
    i = 0
    j = 0
    while (i <= len(our_message) - 1):
        run_count = int(our_message[i])
        run_word = our_message[i + 1]
        for j in range(run_count):
            decompression_str = decompression_str + run_word
        i = i + 2
    return decompression_str


while True:
    pilihan_client = clientSocket.recv(1024)
    pilihan_client = pilihan_client.decode("utf-8")
    if (pilihan_client == "compression"):
        message = clientSocket.recv(1024).decode("utf-8")
        message_length = len(message) * 8
        compression_str = compression_msg(message)
        compression_str_length = (
            len(compression_str) * 3 / 2) + (len(compression_str) * 8 / 2)
        compression_ratio = str(message_length / compression_str_length)
        clientSocket.send(bytes(compression_str, "utf-8"))
        clientSocket.send(bytes(str(compression_str_length), "utf-8"))
        clientSocket.send(bytes(compression_ratio, "utf-8"))
    elif (pilihan_client == "decompression"):
        message = clientSocket.recv(1024).decode("utf-8")
        decompression_str = decompression_msg(message)
        clientSocket.send(bytes(decompression_str, "utf-8"))
    elif (pilihan_client == "end"):
        print(f"Connection from {address} has been removed!")
        clientSocket.close()
    else:
        clientSocket.send(bytes("Pilihan tidak ada!", "utf-8"))
