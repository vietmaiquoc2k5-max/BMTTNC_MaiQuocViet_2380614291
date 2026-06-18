import sys
from PIL import Image

def encode_image(image_path, message):
    img = Image.open(image_path)
    width, height = img.size
    
    # Chuyển đổi thông điệp sang chuỗi nhị phân (mỗi ký tự 8 bits)
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1111111111111110'  # Đánh dấu kết thúc thông điệp
    
    data_index = 0
    for row in range(height):
        for col in range(width):
            # Lấy giá trị pixel (R, G, B) tại tọa độ (col, row) và chuyển thành list để chỉnh sửa
            pixel = list(img.getpixel((col, row)))
            
            for color_channel in range(3): # Duyệt qua 3 kênh: 0->R, 1->G, 2->B
                if data_index < len(binary_message):
                    # Giải thích dòng xử lý cốt lõi:
                    # 1. format(..., '08b') biến giá trị màu (0-255) thành chuỗi nhị phân 8-bit
                    # 2. [:-1] cắt bỏ bit cuối cùng (LSB) của kênh màu đó đi
                    # 3. + binary_message[data_index] cộng bit dữ liệu mật vào vị trí cuối vừa cắt
                    # 4. int(..., 2) chuyển chuỗi nhị phân mới này ngược lại thành số nguyên hệ 10
                    pixel[color_channel] = int(format(pixel[color_channel], '08b')[:-1] + binary_message[data_index], 2)
                    data_index += 1
            
            # Cập nhật lại pixel đã chỉnh sửa vào ảnh
            img.putpixel((col, row), tuple(pixel))
            
            # Nếu đã giấu hết chuỗi bit mật thì thoát vòng lặp cột
            if data_index >= len(binary_message):
                break
        
        # Thoát vòng lặp hàng khi hoàn thành việc giấu tin
        if data_index >= len(binary_message):
            break

    # Lưu lại ảnh đã giấu tin mật dưới định dạng PNG chống nén mất dữ liệu
    encoded_image_path = 'encoded_image.png'
    img.save(encoded_image_path)
    print("Steganography complete. Encoded image saved as", encoded_image_path)


def main():
    # Kiểm tra xem người dùng có truyền đủ tham số qua dòng lệnh không (Cú pháp: python encrypt.py <ảnh> <tin_nhắn>)
    if len(sys.argv) != 3:
        print("Usage: python encrypt.py <image_path> <message>")
        return

    image_path = sys.argv[1]
    message = sys.argv[2]
    encode_image(image_path, message)


if __name__ == "__main__":
    main()
    