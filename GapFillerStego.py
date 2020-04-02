import os
import pathlib
import time


def get_blob(stego, start):
    blob = []
    for i in range(start, len(stego) - 1):
        if stego[i] == b'\xBA':
            if stego[i + 1] == b'\xDC' and stego[i + 2] == b'\x0F' and stego[i + 3] == b'\xFE':
                print("Bad coffee located")
                return blob
            else:
                blob.append(stego[i])
        else:
            blob.append(stego[i])
    print("ERROR = no footer found")
    return []


def place(ciphertext, gaps, output_path):
    largest = ['', 0, 0, 0]  # [path, start, end, consec_empty - 1]
    for g in gaps:  # simple logic to take the largest gap available
        if g[3] >= largest[3]:
            largest = g
    # print(largest) # DEBUG

    target_bytes = []  # bytes to write out to new file

    to_write = [b'\xDE', b'\xAD', b'\xBE', b'\xEF']  # bytes of ciphertext with magic header

    with open(largest[0], "rb") as file:  # read in stego target as byte array
        for byte in iter(lambda: file.read(1), b''):
            target_bytes.append(byte)

    with open(ciphertext, "rb") as file:  # read in gpg blob as byte array
        for byte in iter(lambda: file.read(1), b''):
            to_write.append(byte)

    to_write.append(b'\xBA')  # magic footer
    to_write.append(b'\xDC')
    to_write.append(b'\x0F')
    to_write.append(b'\xFE')

    file_name = str(time.time()) + " - " + largest[0].split("/")[-1]

    dir = largest[0].split("/")[-2]

    print(file_name)

    file_path = os.path.join(output_path, dir)
    pathlib.Path(file_path).mkdir(parents=True, exist_ok=True)
    name = os.path.join(file_path, file_name)

    print(name)
    target_copy = open(os.path.realpath(name), "wb+")  # create output music file

    j = 0  # stego inner counter
    for i in range(largest[1] + 50, (largest[1] + 50 + len(to_write))):  # from the location 50 bytes into the gap
        target_bytes[i] = to_write[j]  # write each byte of ciphertext to stego target
        j += 1

    for b in target_bytes:  # write out to copy of stego target
        target_copy.write(bytes(b))
    target_copy.close()


def retrieve(stego_target, output_path):
    stego_bytes = []
    output_file = str(time.time()) + "message.txt.gpg"
    file_path = os.path.join(output_path, output_file)
    with open(stego_target, "rb") as file:  # read in stego target as byte array
        for byte in iter(lambda: file.read(1), b''):
            stego_bytes.append(byte)

    for i in range(0, len(stego_bytes) - 1):
        if stego_bytes[i] == b'\xDE':
            if stego_bytes[i + 1] == b'\xAD' and stego_bytes[i + 2] == b'\xBE' and stego_bytes[i + 3] == b'\xEF':
                print("Dead beef located")
                blob = get_blob(stego_bytes, i + 4)
                target_copy = open(file_path, "wb")
                for b in blob:
                    target_copy.write(b)
                target_copy.close()

                return os.path.join(output_path, output_file)
    print("No message encoded")
    return None


if __name__ == "__main__":
    gaps = [['/media/grant/DATA/Grant/Documents/Uni/CS408/Practical/gapchecker/17-Cant-Sleep-Love.m4a', 40340, 45048,
             4708]]

    text = os.path.realpath('out.txt.gpg')
    place(text, gaps, "/media/grant/DATA/Grant/Documents/Uni/CS408/Practical/gapfiller/")

    retrieve(os.path.realpath('output.m4a'))
