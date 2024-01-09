import pytesseract
from PIL import Image
import sys

# Ensure Tesseract is in your PATH or specify its path
# Oof.. ugly old windows code.. wuteva
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this line based on your Tesseract installation path

def transcribe_image_to_text(image_path):
    # Load the image from the given path
    try:
        img = Image.open(image_path)
    except IOError:
        print(f"Unable to open image file {image_path}.", file=sys.stderr)
        sys.exit(1)

    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(img, lang='eng')

    # Output the text to a .txt file
    output_file = image_path.replace('.jpg', '.txt')
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

    print(f"Transcription completed. Output saved to {output_file}")

# Replace 'path_to_image.jpg' with the path to your manga page image
transcribe_image_to_text('path_to_image.jpg')
