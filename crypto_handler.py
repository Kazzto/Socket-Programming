from pyascon.ascon import ascon_encrypt, ascon_decrypt

def decrypt_message(encrypted_message, key, nonce, associated_data):
    try:
        decrypted_message = ascon_decrypt(key, nonce, associated_data, encrypted_message, variant="Ascon-128")
        # make sure decryption did not return None so that we can treat it as bytes
        assert decrypted_message != None
        # decode message from bytes into string
        return decrypted_message.decode('utf-8')
    except Exception as e:
        return f"Decryption Error: {e}"

def encrypt_message(message, key, nonce, associated_data):
    # encode message into bytes
    message_bytes = bytes(message, 'utf-8')
    ciphertext = ascon_encrypt(key, nonce, associated_data, message_bytes, variant="Ascon-128")
    return ciphertext
