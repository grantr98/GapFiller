import os
import gnupg

homedir = ""
gpg = ""


def encrypt_message(file, email):  # takes given full real path, encrypts with Public key and signs
    print(file)  # DEBUG
    result = os.system("gpg --trust-model always --yes -se -r %s %s" % (email, file))
    if result != 0:
        print("Encryption failure")
        exit(1)


def decrypt_message(file):  # takes given full real path and decrypts it with private key
    result = os.system("gpg --trust-model always --decrypt %s" % file)
    if result != 0:
        print("Decryption failure")
        exit(1)


def import_key(uname):  # curls out to Keybase with given username and imports their pgp keys
    r = os.system("curl https://keybase.io/%s/pgp_keys.asc >> %s/%s.asc" % (uname, homedir, uname))
    os.system("gpg --import %s/%s.asc" % (homedir, uname))


def main():
    global homedir
    global gpg
    os.system("cd /")
    homedir = ".gnupg"
    homedir = os.path.join(os.getenv("HOME"), homedir)
    print(homedir)
    gpg = gnupg.GPG()


if __name__ == "__main__":
    main()
