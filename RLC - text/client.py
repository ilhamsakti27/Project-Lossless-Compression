import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 4000))

while True:
    pilihan = input("Input pilihan menu (compression, decompression, end): ")
    s.send(bytes(pilihan, "utf-8"))

    if (pilihan == "compression"):
        message = input("Input pesan yang ingin dikompres: ")
        message_length = len(message) * 8
        s.send(bytes(message, "utf-8"))
        server_msg = s.recv(1024).decode("utf-8")
        server_msg_compression_length = s.recv(1024).decode("utf-8")
        server_msg_ratio = s.recv(1024).decode("utf-8")
        print(
            f"===> Pesan {message} dengan jumlah bit {message_length} berhasil dikompres menjadi: {server_msg} dengan jumlah bit {server_msg_compression_length} atau compression ratio sebesar {server_msg_ratio}")
    elif (pilihan == "decompression"):
        message = input("Input pesan yang ingin didekompres: ")
        s.send(bytes(message, "utf-8"))
        server_msg = s.recv(1024).decode("utf-8")
        print(
            f"===> Pesan {message} berhasil didekompres menjadi: {server_msg}")
    elif (pilihan == "end"):
        break
    else:
        server_msg = s.recv(1024)
        print("===> ", end="")
        print(server_msg.decode("utf-8"))
