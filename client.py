import socket
import base64
import sys
import datetime
from crypto_handler import encrypt_message, decrypt_message

def handle_server_response(server_socket):
    encrypted_message = server_socket.recv(1024)
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] Server (Encrypted Message): {base64.b64encode(encrypted_message).decode()}")

    decrypted_message = decrypt_message(encrypted_message, dec_key, nonce, associated_data)# Decrypt the message
    print(f"[{timestamp}] Server (Decrypted Message): {decrypted_message}")

nonce = b'0000000000000000'  # 16-byte nonce
associated_data = b"Secure Communication"

if len(sys.argv) == 1:
    mode = 1 # default to single-key mode
    host, port = '127.0.0.1', 12345
elif len(sys.argv) == 2:
    host, port = '127.0.0.1', 12345
    try:
        mode = int(sys.argv[1])
        # Throw exception if mode is not 1 or 2
        assert mode == 1 or mode == 2
    except:
        print("Not same mode")
        exit()
elif len(sys.argv) == 4:
    try:
        mode = int(sys.argv[1])
        host = sys.argv[2]
        port = int(sys.argv[3])
        # Throw exception if mode is not 1 or 2
        assert mode == 1 or mode == 2
    except:
        print("Not same mode")
        exit()
else:
    exit()

# Select keys based on mode - 1 shared key for single-key mode, 2 shared keys for dual-key mode
if mode == 1:
    print("Starting client in single-key mode...")
    # Encryption and decryption keys are the same for single-key mode
    dec_key = b'1234567890123456'  # 16-byte key for Ascon-128
    enc_key = b'1234567890123456'  # 16-byte key for Ascon-128
else:
    print("Starting client in dual-key mode...")
    # Encryption and decryption keys are different for dual-key mode
    dec_key = b'2468024680246802'
    enc_key = b'3690369036903690'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((host, port))
    print("Connected to the server.")

    while True:
        message = input("Client (You): ")
        encrypted_message = encrypt_message(message, enc_key, nonce, associated_data)
        client.sendall(encrypted_message)

        # Handle response from server
        handle_server_response(client)

        # Optionally, exit after one round
        continue_communicating = input("Do you want to continue? (y/n): ")
        if continue_communicating.lower() != 'y':
            break

    client.close()
    print("Connection closed.")
    exit()