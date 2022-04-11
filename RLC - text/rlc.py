def encode_message(message):
    encoded_string = ""
    i = 0
    # AAAuu
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
        encoded_string = encoded_string + str(count) + ch
        i = j + 1
    return encoded_string


def decode_message(our_message):
    decoded_message = ""
    i = 0
    j = 0
    # 3A2u
    while (i <= len(our_message) - 1):
        run_count = int(our_message[i])
        run_word = our_message[i + 1]
        for j in range(run_count):
            decoded_message = decoded_message + run_word
        i = i + 2
    return decoded_message


def display():
    our_message = "AAAuu"
    encoded_message = encode_message(our_message)
    decoded_message = decode_message(encoded_message)
    print("Original string: [" + our_message + "]")
    print("Encoded string: [" + encoded_message + "]")
    print("Decoded string: [" + decoded_message + "]")


display()
