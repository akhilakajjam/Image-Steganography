from PIL import Image

def convert_to_binary(data):
  
    return [format(ord(char), '08b') for char in data]

def alter_pixels(pixels, binary_data):
 
    data_bits = convert_to_binary(binary_data)
    total_bits = len(data_bits)
    pixel_iterator = iter(pixels)
    
    for idx in range(total_bits):
        current_pixels = [value for value in pixel_iterator.__next__()[:3] +
                                      pixel_iterator.__next__()[:3] +
                                      pixel_iterator.__next__()[:3]]


        for bit_idx in range(8):
            if data_bits[idx][bit_idx] == '0' and current_pixels[bit_idx] % 2 != 0:
                current_pixels[bit_idx] -= 1
            elif data_bits[idx][bit_idx] == '1' and current_pixels[bit_idx] % 2 == 0:
                if current_pixels[bit_idx] > 0:
                    current_pixels[bit_idx] -= 1
                else:
                    current_pixels[bit_idx] += 1
        
      
        if idx == total_bits - 1:
            if current_pixels[-1] % 2 == 0:
                if current_pixels[-1] > 0:
                    current_pixels[-1] -= 1
                else:
                    current_pixels[-1] += 1
        else:
            if current_pixels[-1] % 2 != 0:
                current_pixels[-1] -= 1

        current_pixels = tuple(current_pixels)
        yield current_pixels[0:3]
        yield current_pixels[3:6]
        yield current_pixels[6:9]

def encode_data_into_image(image, data):
 
    width = image.size[0]
    x, y = 0, 0

    for pixel in alter_pixels(image.getdata(), data):
        image.putpixel((x, y), pixel)
        if x == width - 1:
            x = 0
            y += 1
        else:
            x += 1

def encode_image():
  
    image_path = input("Provide the image file name (with extension): ")
    try:
        img = Image.open(image_path)
    except IOError:
        print("Error: Cannot open the specified image file.")
        return

    text_data = input("Enter the data to be hidden: ")
    if len(text_data) == 0:
        raise ValueError('The data provided is empty')

    modified_img = img.copy()
    encode_data_into_image(modified_img, text_data)

    output_image_name = input("Provide the new image file name (with extension): ")
    file_ext = output_image_name.split(".")[-1].upper()

    format_conversion = {'JPG': 'JPEG', 'PNG': 'PNG', 'BMP': 'BMP'}
    img_format = format_conversion.get(file_ext, file_ext)
    
    try:
        modified_img.save(output_image_name, format=img_format)
        print(f"Image successfully saved as {output_image_name}")
    except KeyError:
        print(f"Error: Unsupported file format: {file_ext}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def decode_data_from_image():
   
    image_path = input("Provide the image file name (with extension): ")
    try:
        img = Image.open(image_path)
    except IOError:
        print("Error: Cannot open the specified image file.")
        return

    extracted_data = ''
    pixel_iterator = iter(img.getdata())

    while True:
        try:
            pixel_values = [value for value in pixel_iterator.__next__()[:3] +
                                        pixel_iterator.__next__()[:3] +
                                        pixel_iterator.__next__()[:3]]
        except StopIteration:
            break

        binary_string = ''.join(['0' if value % 2 == 0 else '1' for value in pixel_values[:8]])
        extracted_data += chr(int(binary_string, 2))
        
        if pixel_values[-1] % 2 != 0:
            return extracted_data

def main():
   
    try:
        user_choice = int(input("STEGANOGRAPHY \n1. Encode \n2. Decode \nChoose either 1 or 2: "))
        if user_choice == 1:
            encode_image()
        elif user_choice == 2:
            print("Hidden Message : " + decode_data_from_image())
        else:
            raise ValueError("Invalid selection. Please choose 1 or 2.")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()

