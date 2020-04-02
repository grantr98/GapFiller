# GapFiller
A compression standard agnostic, tag scheme agnostic steganographic scheme that takes advantage of blank spaces present in MPEG files after compression.

Submitted for the degree of BSc (Hons) in Computer Science at Strathclyde University. 

This source code will be released after evaluation is complete for the benefit of the wider community.

## Prerequisites
*  A Python IDE (PyCharm is strongly recommended).
*  A Python virtual environment with the following packages:
	*  os
	*  pathlib
	*  gnupg
	*  time
	*  mutagen
	*  soundfile
	*  math
*  A Ubuntu/Linux distribution with GNUPG and Curl accessible from the command line (packages gnupg and curl if your distro doesn’t have them available by default).
*  An account at [keybase.io](https://keybase.io) - used to obtain your recipients public key and publish your public key
*  You and your recipient must have a keypair (generated with Keybase or gnupg), with the public key published to Keybase. (see [these instructions](https://help.github.com/en/github/authenticating-to-github/generating-a-new-gpg-key) for how to generate a keypair from the command line with GNUPG)
*  You and your recipient must also know your respective username, and the email tied to your public keys.
*  A text file containing the message you wish to send.
*  A music file (or ideally a set of music files) to perform steganography on.
*  A mechanism to send the file (most established messaging systems will do).

## Encryption
*  Run the ‘GapFiller.py’ file to start the program.
*  At the first prompt, type ‘e’ to start the encryption process.
*  At the second prompt, type the Keybase username of your recipient, then at the third prompt type the recipients email (this must match the email associated with the public key).
*  Finally, enter the (relative or full) path to the file containing your message.
*  The program will then fetch the recipients key from their Keybase profile, encrypt the text file with it, then attempt to sign the message with your private key. If prompted, enter the password to unlock your private key.
*  Once the encryption process is complete, the program will prompt you for a directory to search for suitable carrier files. It will then search every music file in this directory for gaps of a suitable size to place the message in.

	*  If this directory contains a lot of files, this may take some time. If the directory doesn’t contain any suitable files or does not exist, the program will reprompt you for a new path.

	*  Once the search process is complete, the program will select the file with the largest available gap, and prompt you for a location to save the carrier file to. You may leave this blank if you wish to place the carrier file in the program directory.
	*  The program will then perform the steganographic operation, and place the resulting file in the location [SpecifiedDirectory]/[OriginalDir]/[Epoch]-[OriginalMusicName].[ext], then displays the path to you. You may now send this file through any messaging means you wish.
*  The program prepends the current time (in Unix epoch) to the start of the file to prevent any overwriting resulting in reuse of carrier files. This can be renamed before sending.

## Decryption
*  Run the ‘GapFiller.py’ file to start the program.
*  At the first prompt, type ‘d’ to start the decryption process.
*  At the second prompt, type the path to the file you wish to check for encrypted content.
*  At the third prompt, type the path to the location you wish to place the encrypted file (which will be named as [Epoch]message.txt.gpg).
	*  The program will print ‘dead beef located’, ‘bad coffee located’ and the message itself if a message is embedded, and will print ‘no message encoded’ if not. It will then save the message to “out.txt” in the program directory.
	*  The gpg module will give you information on the messages signature and verify it as good if you have access to the senders public key.
	*  The gpg module will also warn you that you are using an untrusted key. Please disregard this, as gnupg will automatically distrust any key you haven’t explicitly “trusted and signed” through its system. It can be assumed any keys acquired from Keybase can be trusted.

## Licence
Once evaluation is complete, this program will be released under a GNU General Public License v3.0

## Author
[Grant Rodgers](https://twitter.com/gingerninja1998)
