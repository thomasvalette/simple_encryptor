# simple_encryptor

A simple PyQt5 GUI based program that allow cyphering/decyphering on files and folders.

![alt text](https://raw.githubusercontent.com/thomasvalette/simple_encryptor/master/assets/screenshot.png)

- Cypher part is handled by Fernet algorithm from the cryptography library, it uses AES 128.
- Users can provide a password or a key file for cypher/decypher operations.
- File keys and passwords can be generated in the File menu.