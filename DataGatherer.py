import math
import os
import pathlib
import mutagen
import GapChecker
import soundfile as sf


def dump(data):
    f = open("data_dump1.dat", "w+")

    f.read()
    f.write("# [bandwidth, ext, duration, bitrate, file_size, max_gap, avg_gap, no_gaps]\r")

    for n in range(len(data)):
        for i in range(len(data[n])):
            f.write(str(data[n][i]))
            f.write(" ")


def main(path, threshold):
    per_file = []

    files_found = 0

    for root, dirs, files in os.walk(path):
        for name in files:  # for each file in path
            path = os.path.join(root, name)
            ext = pathlib.Path(path).suffix
            print("FILE: %s EXTENSION: %s" % (path, ext))  # DEBUG
            if GapChecker.ismusic(ext):  # if passes as music file
                if ext == ".wav":  # special way of calculating duration and bitrate for WAV files
                    f = sf.SoundFile(path)
                    duration = (len(f) / f.samplerate)
                    word = f.subtype
                    word = int(word.split("_")[-1])
                    bitrate = str((f.samplerate * word * f.channels) / 1000)


                else:
                    # get file metadata
                    cur_file = mutagen.File(path)
                    if cur_file is not None:
                        duration = math.floor(cur_file.info.length)
                        bitrate = math.floor(cur_file.info.bitrate / 1000)

                files_found += 1
                in_file = open(path, "rb")  # [r]ead as [b]yte array

                data = in_file.read()
                size = len(data)
                in_file.close()
                found = GapChecker.gapfinder(data, path, threshold)

                # aggregates all useful bandwidth in the file
                aggregate = [0, ext, duration, bitrate, size, 0, 0, 0]
                # [0=bandwidth, 1=ext, 2=duration, 3=bitrate, 4=file_size, 5=max_gap, 6=avg_gap, 7=no_gaps]

                # [path, start, end, consec_empty - 1]
                for f in found:  # for all gaps found
                    aggregate[7] += 1  # increment number of gaps
                    aggregate[0] += f[3]  # add to bandwidth value
                    if f[3] > aggregate[5]:  # if current size is bigger than max_size, replace
                        aggregate[5] = f[3]
                if aggregate[0] != 0 and aggregate[7] != 0:
                    aggregate[6] = math.floor(aggregate[0] / aggregate[7])  # avg = bandwidth/no_gaps
                    per_file.append(aggregate)

        for name in dirs:
            print("DIR: %s" % os.path.join(root, name))

    return per_file


if __name__ == "__main__":
    print("Please enter the directory/file you wish to search")
    path_to_file = input("> ")
    x = main(os.path.realpath(path_to_file), 900)

    print(x)

    dump(x)
