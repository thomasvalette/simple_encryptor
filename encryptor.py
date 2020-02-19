#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import base64
import shutil
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Encryptor:
    """ Provides simple tools for encrypt / decrypt file and folders
    """

    def __init__(self):
        # basic config
        self.ext_file = ".lock"
        self.ext_dir = ".dlock"

        # init the Fernet
        self.f = None

    @staticmethod
    def password_to_key(password, salt):
        """
        """
        password = password.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1000000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))


    def set_key_from_keyfile(self, key_file):
        """
        """
        self.key = open(key_file, "rb").read()
        self.f = Fernet(self.key)

    def set_key_from_password(self, password):
        """
        """
        salt = "DefaulSalt123456".encode()
        self.key = Encryptor.password_to_key(password, salt)
        self.f = Fernet(self.key)

    def generate_key_file(self, file_path):
        """
        """
        with open(file_path, "wb") as file:
            file.write(Fernet.generate_key())


    def encrypt_file(self, file_name):
        """ Given a filename (str) and key (bytes), it encrypts the file and write it
        """
        if self.f is None:
            raise ValueError(
                "A key must be created before encryption / decryption operations")

        with open(file_name, "rb") as file:
            # read all file data
            file_data = file.read()

        # encrypt data
        encrypted_data = self.f.encrypt(file_data)

        # write the encrypted file
        with open(file_name, "wb") as file:
            file.write(encrypted_data)

        # rename the file
        os.rename(file_name, "{}{}".format(
            file_name,
            self.ext_file))

    
    def decrypt_file(self, file_name):
        """ Given a filename (str) and key (bytes), it decrypts the file and write it
        """
        if self.f is None:
            raise ValueError(
                "A key must be created before encryption / decryption operations")

        with open(file_name, "rb") as file:
            # read the file data
            encrypted_data = file.read()

        # decrypt data
        decrypted_data = self.f.decrypt(encrypted_data)

        # write the original file
        with open(file_name, "wb") as file:
            file.write(decrypted_data)
        
        # rename the file
        new_name = os.path.splitext(file_name)[0]
        
        # os.rename(file_name, file_name[:-len(self.ext_file)])
        os.rename(file_name, new_name)

    
    def encrypt_directory(self, dir_name):
        """
        """
        if self.f is None:
            raise ValueError(
                "A key must be created before encryption / decryption operations")

        # Create an archive of the directory
        shutil.make_archive(dir_name, 'tar', dir_name)

        # encrypt the archive
        self.encrypt_file("{}.tar".format(dir_name))

        # rename the folder cypher
        os.rename(
            "{}.tar{}".format(dir_name, self.ext_file),
            "{}{}".format(dir_name, self.ext_dir))

        # remove the directory when the archive is created
        shutil.rmtree(dir_name)

    
    def decrypt_directory(self, file_name):
        """
        """
        if self.f is None:
            raise ValueError(
                "A key must be created before encryption / decryption operations")
        # decrypt tar archive
        self.decrypt_file(file_name)

        # removing the ".ld" and rename archive
        dir_name = os.path.splitext(file_name)[0]
        os.rename(dir_name, "{}.tar".format(dir_name))

        # unpack archive
        shutil.unpack_archive("{}.tar".format(dir_name), dir_name)

        # remove archive when the directory is created
        os.remove("{}.tar".format(dir_name))
