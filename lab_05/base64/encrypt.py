import base64

def main():
    # Sửa lỗi thụt lề (indentation) cho các dòng bên trong hàm
    input_string = input("Nhập thông tin cần mã hóa: ")
    encoded_bytes = base64.b64encode(input_string.encode("utf-8"))
    encoded_string = encoded_bytes.decode("utf-8")
    
    with open("data.txt", "w", encoding="utf-8") as file:  # Thêm encoding để tránh lỗi font trên Windows
        file.write(encoded_string)
        
    print("Đã mã hóa và ghi vào tệp data.txt")

# Sửa lỗi cú pháp: Phải có 2 dấu gạch dưới (__) xung quanh name và main, và thay 'if_name' bằng 'if __name__'
if __name__ == "__main__":
    main()