# Secure Socket Communication with Ascon Encryption

This repository implements a secure client-server socket communication system using the Ascon lightweight authenticated encryption algorithm. It provides both single-key and dual-key modes for encryption and decryption.

## Features

* **Secure Communication:** Encrypted message transfer between client and server using the Ascon-128 algorithm.
* **Single-Key and Dual-Key Modes:** Supports both single shared key and separate encryption/decryption key modes.
* **Ascon Implementation:** Includes the `pyascon` library, a Python implementation of the Ascon v1.2 authenticated cipher and hash function.
* **Clear Modularity:** Code is organized into separate modules for socket handling, cryptography, and main application logic.
* **Error Handling:** Includes basic error handling for socket operations and decryption.
* **KAT Generation:** Includes scripts for generating Known Answer Tests (KATs) for the Ascon implementation.

## Files

* **`client.py`:**
    * Implements the client-side application.
    * Connects to the server, sends encrypted messages, and receives/decrypts messages from the server.
    * Supports single and dual-key modes.
* **`server.py`:**
    * Implements the server-side application.
    * Listens for client connections, receives encrypted messages, and sends encrypted responses.
    * Supports single and dual-key modes.
* **`crypto_handler.py`:**
    * Provides functions for encrypting and decrypting messages using the Ascon-128 algorithm.
    * Uses the `pyascon` library for cryptographic operations.

## Usage

### Prerequisites

* Python 3.x
* `pyascon` library (included in the repository)

### Running the Applications

1.  **Server:**

    python server.py <mode> <host-ip> <port>

    * `<mode>`:  1 for single-key mode, 2 for dual-key mode.
    * `<host-ip>`: The IP address to host the server (e.g., `0.0.0.0` for all interfaces, `localhost` or `127.0.0.1` for local).
    * `<port>`: The port number to listen on (e.g., `12345`).
    * If no arguments are provided, the default values of single-key mode, 0.0.0.0, and port 12345 will be used. If only a mode is provided, the default ip and port will be used.

    Example (single-key mode, default host and port):

    python server.py

    Example (dual-key mode, specific host and port):

    python server.py 2 192.168.1.100 5000
   
2.  **Client:**

    python client.py <mode> <host-ip> <port>


    * Arguments are the same as for the server.  The client must be run with the same mode as the server.

    Example (single-key mode, default host and port):

    python client.py
   

    Example (dual-key mode, specific host and port):

    python client.py 2 192.168.1.100 5000


### Important

* Ensure that the server is running before starting the client.
* The client and server must use the same mode (single-key or dual-key) to ensure correct encryption and decryption.

## `pyascon` Library

This repository includes a slightly modified version of the `pyascon` library. For detailed information about the Ascon algorithm and the `pyascon` implementation, please refer to `pyascon/README.md`.

## License

(You should add a license here, e.g., MIT License, Apache License 2.0, etc.  Choose the license that suits your needs.)
