import base64

def main():
    try:
        # Sửa lỗi thụt lề (indentation) cho toàn bộ khối lệnh bên trong hàm main
        with open("data.txt", "r", encoding="utf-8") as file:  # Nên thêm encoding="utf-8" khi đọc file
            encoded_string = file.read().strip()
            
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode("utf-8")
        print("Chuỗi sau khi giải mã:", decoded_string)
        
    except FileNotFoundError:
        # Xử lý riêng trường hợp file không tồn tại để thông báo rõ ràng hơn
        print("Lỗi: Không tìm thấy tệp 'data.txt'. Vui lòng chạy file mã hóa trước!")
    except Exception as e:
        print("Lỗi:", e)

# Sửa lại cú pháp kiểm tra block main chuẩn của Python
if __name__ == "__main__":
    main()