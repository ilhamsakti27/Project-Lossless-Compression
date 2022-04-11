import socket       # menggunakan library cv2 dan numpy untuk mengambil data-data pada gambar
import sys          # library socket digunakan untuk menghubungkan antara server dan client
import cv2
import numpy as np
from time import sleep
# from Huffman import Huff

# hubungkan antara server dan client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1088))
s.listen(5)     # makes a socket ready for accepting connections.

# class Node dibuat untuk membuat pohon huffman
class Node:
    # __init__, sebagai constructor atau fungsi yg pertama kali dipanggil ketika kelas dipanggil
    # parameter fungsi ini adalah data (untuk menyimpan data), freq (berapa kali data tersebut muncul), left, dan right untuk membuat phon huffman
    def __init__(self, data, freq, left=None, right=None):
        self.data = data
        self.freq = freq
        self.left = left
        self.right = right


class Huff:
    # fungsi ini berfungsi untuk mengambil data-data pada gambar
    def __init__(self, img):
        self.dict = {}          # deklarasi dictionary
        self.code = []          # deklarasi list
        self.hist_dic = {}      # deklarasi dictionary
        self.img =img
        hist, bins = np.histogram(self.img.ravel(), 256, [0, 256])      # ambil data dan frekuensi dari gambar dgn pendistribusian pixel pada gambar menggunakn histogram dan ravel
        bins = bins.tolist()        # untuk menyimpan data gambar
        hist = hist.tolist()        # untuk menyimpan frekuensi
        # Remove zeros
        for hist, bin in zip(hist, bins):
            self.hist_dic[bin] = hist
        dic = self.hist_dic.copy()
        for key in dic.keys():
            if self.hist_dic[key] == 0:
                del(self.hist_dic[key])

        self.bins = self.hist_dic.keys()
        self.hist = [self.hist_dic[x] for x in self.bins]

    # untuk membuat pohon havmand
    def CreateTree(self):
        charList = self.bins # ambil data pada gambar
        freqList = self.hist # ambil frekuensi pada gambar
        minHeap = [Node(c, f) for c, f in zip(charList, freqList)] # ambil dasar dari dua variabel sebelumnya

        # pembuatan pohon huffman 
        # urutkan dengan bandingkan data dan frekuensi pada gambar
        while(len(minHeap) != 1):
            minHeap = sorted(minHeap, key=lambda x: x.freq, reverse=True)
            # print([x.freq for x in minHeap])
            # print([x.data for x in minHeap])
            intNode = Node(None, minHeap[-1].freq+minHeap[-2].freq) # masukkan data ke node. -1 untuk sebelah kanan. -2 untuk sebelah kanan
            intNode.left = minHeap[-2]      # node sebelah kiri datanya dikurangi dua
            intNode.right = minHeap[-1]     # node sebelah kiri datanya dikurangi satu
            minHeap.pop()                   # hapus node terakhir
            minHeap.pop()                   # hapus node terakhir
            minHeap.append(intNode)         # menambahkan value intNode ke min heap

        return minHeap[0] # return nilai min heap

    # untuk memberikan bilangan boolean pada data yg sudah dibuat oleh pohon huffman
    def Code(self, tree, s=""):
        if tree.data is not None:
            print(tree.data, end=" ")
            print(s)
            self.dict[tree.data] = s
            return
        self.Code(tree.left, s+'0')     # sebelah kiri diberi nilai 0
        self.Code(tree.right, s+'1')    # sebelah kiri diberi nilai ``

    # melakukan encode pada data yg sudah dibuat pada pohon huffman
    # me-replace karakter pada string dengan kode Huffman yang berkaitan, maka akan didapatkan string dengan kode Huffman
    def encode(self):
        flat = self.img.flatten().tolist()
        for pix in flat:
            self.code.append(self.dict[pix])
        return self.code

    # untuk decode data pohon huffman
    def decode(self, tree):
        current = tree
        self.string = []
        for code in self.code:
            for bit in code:
                if bit == "0":
                    current = current.left
                else:
                    current = current.right

            if current.left == None and current.right == None:
                self.string.append(current.data)
                current = tree
        return self.string


while True:
    # sambungkan client dgn server
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")   # jika connected
    clientsocket.send(bytes("Server connected", "utf-8"))

    #  inti program huffman
    while True:
        nama_foto = ''                                      # input file foto
        nama_foto = clientsocket.recv(1024).decode()
        print(nama_foto)
        image = cv2.imread(nama_foto, 0)                    # baca foto sesai nama filenya
        cv2.imshow("OriginalImage", image)                  # tampilkan foto yg diinputkan

        obj = Huff(image)                                   # buat variabel obj untuk memanggil fungsi huff. ubah data image ke dalam bentuk objek
        root = obj.CreateTree()                             # variabel root untuk memanggil fungsi CreateTree
        obj.Code(root)                                      # berikan nilai boolean pada pohon huffman sesuai data pada image yg diinputkan
        coded_image = obj.encode()                          # encode data pohon huffman
        temp = 0    
        for code in coded_image:                            # hitung panjang data darin encode yg telah dilakukan 
            temp += len(code)

        average_length = temp/len(coded_image)              # hitung rata2 dimensi foto
        clientsocket.send(str(average_length).encode())     # kirim hasil ke client
        sleep(1)

        shape = image.shape
        original_size = (shape[0]*shape[1])/1024 # in Kb    # hitung ukuran asli foto
        clientsocket.send(str(original_size).encode())      # kirim hasil ke client
        sleep(1)

        comp_size = (temp/8)/1024 # for Kb                  # hitung size file foto setelah di compress
        clientsocket.send(str(comp_size).encode())          # kirim ke client
        sleep(1)

        ret = obj.decode(root)                              # decode pohon huffman
        ret = np.array(ret, np.uint8)                       # hasil decode jadikan dlm bentuk array
        ret_image = np.reshape(ret, shape)                  # reshape untuk foto yg telah di compress
        cv2.imshow("RetrivedFromCompression", ret_image)    # tampilkan foto ke screen
        cv2.waitKey()                                       #  using the wait key function to delay the
                                                            # closing of windows till any ke is pressed
        cv2.destroyAllWindows()                             # menutup semua jendela windows
        ratio = 8/average_length                            # ratio sebelum dan sesudah di compre
        clientsocket.send(str(ratio).encode())              # kirim hasil ke client
