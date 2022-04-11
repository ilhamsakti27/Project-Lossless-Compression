import socket
import sys
import cv2
import numpy as np
from time import sleep

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1088))

full_msg = ''
msg = s.recv(1024).decode()
print(msg)

while True:
    nama_foto = input("Masukkan nama foto:")
    s.send(bytes(str(nama_foto), "utf-8"))

    average_lenght =s.recv(1024).decode()
    print("\nAverage length of code is ", average_lenght, "bits")

    original_size = s.recv(1024).decode()
    print("Size of the image is ", original_size, "Kb")

    comp_size = s.recv(1024).decode()
    print("Size after compression is ", comp_size, "Kb")

    print("compression Ratio is ", average_lenght)