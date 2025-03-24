import socket
import base64
import datetime
import sys
from crypto_handler import encrypt_message, decrypt_message

class Socket_handler:#required for automatically enter and exit which helps in automatically closing the sockets when not at use
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.socket = None
    
    def __enter__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        return self.socket
    
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.socket.close()
            print("Socket closed successfully")
        except OSError as e:
            print(f"Error closing socket: {e}")

def receive_messages(client_socket):
    while True:
        try:
            encrypt_message = client_socket.recv(1024)
            if not encrypt_message:
                print(f"Connection closed")
                break  # Client disconnected

            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] Client (Encrypted Message): {base64.b64encode(encrypt_message ).decode()}")# Print encrypted message
            decrypted_message = decrypt_message(encrypt_message, dec_key, nonce, associated_data)    # Decrypt the message
            print(f"[{timestamp}] Client (Decrypted Message): {decrypted_message}")

        except ConnectionResetError:
            print(f"Connection forcibly closed")
            break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break
    client_socket.close()

def send_messages(client_socket):
    while True:
        try:
            response = input("Server (You): ")
            client_socket.sendall(encrypt_message(response, enc_key, nonce, associated_data))
        except Exception as e:
            print(f"Error sending message: {e}")
            break
            

nonce = b'0000000000000000'  # 16-byte nonce
associated_data = b"Secure Communication"
def printUsage():
    print(f"Usage: {sys.argv[0]} <mode> <host-ip> <port>\nmode - 1 for single-key mode, 2 for dual-key mode.\nhost-ip - the ip to host the server\nport - the port to host the server\n\nIf no arguments are provided, the default values of single-key mode, 0.0.0.0, and port 12345 will be used.\nIf only a mode is provided, the default ip and port will be used.")
if len(sys.argv) == 1:
    mode = 1 # default to single-key mode
    host, port = '0.0.0.0', 12345
elif len(sys.argv) == 2:
    host, port = '0.0.0.0', 12345
    try:
        mode = int(sys.argv[1])
        # Throw exception if mode is not 1 or 2
        assert mode == 1 or mode == 2
    except:
        printUsage()
        exit()
elif len(sys.argv) == 4:
    try:
        mode = int(sys.argv[1])
        host = sys.argv[2]
        port = int(sys.argv[3])
        # Throw exception if mode is not 1 or 2
        assert mode == 1 or mode == 2
    except:
        printUsage()
        exit()
else:
    printUsage()    
    exit()

# Select keys based on mode - 1 shared key for single-key mode, 2 shared keys for dual-key mode
if mode == 1:
    print("Starting server in single-key mode...")
    enc_key = b'1234567890123456'  # 16-byte key for Ascon-128
    dec_key = b'1234567890123456'  # 16-byte key for Ascon-128
else:
    print("Starting server in dual-key mode...")
    enc_key = b'2468024680246802'
    dec_key = b'3690369036903690'


try:
    # Use "with" to automatically close the server socket when we are done, even if error occurs
    with Socket_handler(host, port) as server:
        server.listen(1)
        print(f"Server listening on {host}:{port}...")

        client_socket, addr = server.accept()
        print(f"Connection established with {addr}")

        receive_messages(client_socket)
        client_socket.close()
except Exception as e:
    print(f"Error: {e}")