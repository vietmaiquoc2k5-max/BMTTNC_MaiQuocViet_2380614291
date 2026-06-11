from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import hashlib

# Initialize client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))
# Generate RSA key pair
client_key = RSA.generate(2048)
# Receive server's public key
server_public_key = RSA.import_key(client_socket.recv(2048))
# Send client's public key to the server
client_socket.send(client_key.publickey().export_key(format='PEM'))
# Receive encrypted AES key from the server
encrypted_aes_key = client_socket.recv(2048)
# Decrypt the AES key using client's private key
cipher_rsa = PKCS1_OAEP.new(client_key) # Đã sửa: lỗi đánh máy số '0' thành chữ 'O' (0AEP -> OAEP)
aes_key = cipher_rsa.decrypt(encrypted_aes_key)

# Function to encrypt message
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC) # Đã sửa: thêm dấu '='
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext

# Function to decrypt message
def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv) # Đã sửa: thêm dấu '='
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()

# Function to receive messages from server
def receive_messages():
    try:
        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                print("\n[Kết nối với server đã bị ngắt]")
                break
            decrypted_message = decrypt_message(aes_key, encrypted_message)
            # Thêm \n để tránh bị đè lên dòng input hiện tại
            print(f"\nReceived: {decrypted_message}")
    except Exception as e:
        print(f"\n[Lỗi kết nối]: {e}")

# Start the receiving thread
# Đã sửa: 'target-receive_messages' thành 'target=receive_messages'
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True # Đảm bảo thread tự đóng khi chương trình chính kết thúc
receive_thread.start()

# Send messages from the client
try:
    while True:
        message = input("Enter message ('exit' to quit): ")
        encrypted_message = encrypt_message(aes_key, message)
        client_socket.send(encrypted_message)
        if message == "exit":
            break
except KeyboardInterrupt:
    print("\nĐang thoát...")
finally:
    # Close the connection when done
    client_socket.close() # Đã sửa: 'client socket.close()' thiếu dấu gạch dưới