import GnuPG
import GapChecker
import GapFillerStego
import os


def main():
    GnuPG.main()  # initialises the GnuPG engine

    print("Do you wish to (e)ncrypt a message or (d)ecrypt a file?")
    choice = input("> ")

    if choice.lower() == "e":
        print("Please enter the Keybase username of the recipient")
        username = input(">")

        print("Please enter the email of the recipient")
        email = input(">")

        print("Please enter the path to the file you wish to encrypt and sign")
        path_to_file = input(">")

        print("%s %s %s" % (username, email, os.path.realpath(path_to_file)))  # DEBUG
        GnuPG.import_key(username)
        GnuPG.encrypt_message(path_to_file, email)
        file_size = os.path.getsize(path_to_file + '.gpg')

        gaps = getGaps(file_size)
        print(gaps)

        print("Please enter the directory that you wish to place the outputted files (leave blank for this dir)")
        path_to_output = input(">")
        if path_to_output == "":
            path_to_output = "./"

        GapFillerStego.place(path_to_file + '.gpg', gaps, path_to_output)

    elif choice.lower() == "d":
        print("Please enter the path to the file you wish to check for encrypted content")
        path_to_file = input(">")
        print("Please enter the directory that you wish to place the outputted file (leave blank for this dir)")
        path_to_output = input(">")
        if path_to_output == "":
            path_to_output = "./"


        print("%s" % (os.path.realpath(path_to_file)))
        ciphertext_path = GapFillerStego.retrieve(path_to_file, path_to_output)
        if ciphertext_path is not None:
            GnuPG.decrypt_message(ciphertext_path)
    elif choice.lower() == "exit":
        exit(0)
    else:
        print("Invalid input, please try again")
        main()


def getGaps(file_size):
    print("Please enter the directory you wish to find a file target from")
    stego_directory = input(">")

    gaps = GapChecker.main(os.path.realpath(stego_directory), file_size)
    if not gaps:
        print("No suitable files found in selection, please try again")
        getGaps(file_size)
    return gaps


if __name__ == "__main__":
    main()
