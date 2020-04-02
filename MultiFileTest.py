# TEST FOR MULTIPLE FILES/MULTIPLE GAPS
import os

import GapChecker
import GapFillerStego
import GnuPG


def main():
    GnuPG.main()  # initialises the GnuPG engine
    gaps_placed = 0
    gaps_retrieved = 0

    print("Please enter the Keybase username of the recipient")
    username = input(">")

    if username == "auto1":  # Use this to automate multiple runs and reduce the amount of typing
        username = ""
        email = ""
        path_to_file = "out.txt"
        path_to_output = ""
    else:
        print("Please enter the email of the recipient")
        email = input(">")

        print("Please enter the path to the file you wish to encrypt and sign")
        path_to_file = input(">")

        print("Please enter the directory that you wish to place the outputted files")
        path_to_output = input(">")

    print("%s %s %s" % (username, email, os.path.realpath(path_to_file)))  # DEBUG
    GnuPG.import_key(username)
    GnuPG.encrypt_message(path_to_file, email)
    file_size = os.path.getsize(path_to_file + '.gpg')

    gaps = getGaps(file_size)
    print(gaps)
    gaps_placed = len(gaps)

    for x in gaps:
        GapFillerStego.place(path_to_file + '.gpg', [x], path_to_output)

    print("Please enter the directory that you wish to place the outputted files")
    msg_output = input(">")

    for root, dirs, files in os.walk(path_to_output):
        for name in files:  # for each file in path
            success = GapFillerStego.retrieve(os.path.join(root, name), os.path.realpath(msg_output))
            if success is not None:
                gaps_retrieved = gaps_retrieved + 1

    print("Gaps Placed - %s, Gaps Retrieved - %s, Percentage Recovered - %s" % (
        gaps_placed, gaps_retrieved, ((gaps_retrieved / gaps_placed) * 100)))


def getGaps(file_size):
    print("Please enter the directory you wish to find a file target from")
    stego_directory = input(">")

    gaps = GapChecker.main(os.path.realpath(stego_directory), file_size)
    if not gaps:
        print("No suitable files found in selection, please try again")
        getGaps(file_size)
    return gaps


if __name__ == '__main__':
    main()
