from PIL import Image
import io

def image_to_byte_array(image: Image) -> bytes:
  
  # BytesIO is a file-like buffer stored in memory
  imgByteArr = io.BytesIO()

  # image.save expects a file-like as a argument
  image.save(imgByteArr, format=image.format)

  # Turn the BytesIO object back into a bytes object
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

# Example usage
image_path = 'D:\\Major Project\\DB1_B\\104_7.tif'      #specify file path accordingly
img = Image.open(image_path)

img_byte_array = image_to_byte_array(img)

# Print the first 100 bytes as a hex representation
print(img_byte_array[:100].hex())