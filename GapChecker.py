import os
import pathlib
import mutagen


def gapfinder(array, path, threshold):  # parses through file to count gaps of "00"
    found = []
    # print("File size %s bytes" % threshold)  # DEBUG
    threshold += 100  # threshold
    # print("Safety threshold %s bytes" % threshold)  # DEBUG

    i = 0
    start = -1
    consec_empty = 0

    for b in array:  # for each byte in the array
        if b == 0:
            if start == -1:  # if byte empty, and no start has been identified
                start = i
            consec_empty += 1
        else:  # if b is not empty, start end action
            end = i - 1
            if consec_empty >= threshold:  # if consec_empty hits threshold
                print("File %s has %s bytes available from %s to %s" % (path, (consec_empty - 1), start, end))
                # print(array[start], array[end])  # DEBUG
                found.append([path, start, end, consec_empty - 1])  # add gap info to array to send back
            start = -1  # reset start counter and empty count
            consec_empty = 0
        i += 1  # iterate through counter
    return found


def ismusic(ext):
    return ext == ".mp3" or ext == ".m4a" or ext == ".wav" or ext == ".ogg" or ext == ".aac" or ext == ".wma"


def main(path, threshold):
    gaps = []
    files_found = 0
    for root, dirs, files in os.walk(path):
        for name in files:  # for each file in path
            path = os.path.join(root, name)
            ext = pathlib.Path(path).suffix
            print("FILE: %s EXTENSION: %s" % (path, ext))  # DEBUG
            if ismusic(ext):  # if passes as music file

                files_found += 1
                in_file = open(path, "rb")  # [r]ead as [b]yte array
                data = in_file.read()
                in_file.close()
                found = gapfinder(data, path, threshold)
                for f in found:
                    gaps.append(f)

        for name in dirs:
            print("DIR: %s" % os.path.join(root, name))

    return gaps


if __name__ == "__main__":
    print("Please enter the directory/file you wish to search")
    path_to_file = input("> ")
    x = main(os.path.realpath(path_to_file), 900)
    print(x)