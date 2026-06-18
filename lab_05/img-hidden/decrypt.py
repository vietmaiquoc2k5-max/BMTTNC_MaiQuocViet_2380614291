import sys
from PIL import Image

def decode_image(encoded_image_path):
    img = Image.open(encoded_image_path)
    width, height = img.size
    binary_message = ""
    
    # 1. Quét qua từng pixel và gom tất cả các bit LSB (bit cuối) từ 3 kênh màu
    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))
            
            for color_channel in range(3):
                # format(..., '08b') chuyển giá trị màu thành chuỗi 8-bit nhị phân, 
                # và [-1] lấy ra bit cuối cùng của chuỗi đó
                binary_message += format(pixel[color_channel], '08b')[-1]

    # 2. Gom các cụm 8 bit (1 byte) lại thành ký tự tương ứng
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        
        # Kiểm tra dấu hiệu dừng của file mã hóa (chuỗi 16 bit '1111111111111110')
        # Khi gom byte kế tiếp mà phát hiện ra chuỗi kết thúc thì dừng lại luôn
        if binary_message[i:i+16] == '1111111111111110':
            break
            
        char = chr(int(byte, 2))
        
        # Kiểm tra dấu hiệu dừng theo ký tự Null '\0' (đề phòng ảnh mã hóa kiểu cũ)
        if char == '\0':
            break
            
        message += char
        
    return message


def main():
    # Kiểm tra tham số dòng lệnh (Cú pháp: python decrypt.py <đường_dẫn_ảnh_đã_mã_hóa>)
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return

    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    print("Decoded message:", decoded_message)


if __name__ == "__main__":
    main()
    