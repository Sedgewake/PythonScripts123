from PIL import Image
import sys
import os

def png_to_ico(png_path, ico_path=None, sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]):
    # Validate PNG path
    if not os.path.isfile(png_path):
        print(f"Error: '{png_path}' not found.")
        return
    
    # Set default ico path
    if ico_path is None:
        ico_path = os.path.splitext(png_path)[0] + ".ico"

    # Open the PNG
    img = Image.open(png_path).convert("RGBA")

    # Ensure image is square
    if img.width != img.height:
        print("Warning: Image is not square. It will be padded to square.")
        size = max(img.width, img.height)
        square_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        square_img.paste(img, ((size - img.width) // 2, (size - img.height) // 2))
        img = square_img

    # Save as ICO with multiple resolutions
    img.save(ico_path, format="ICO", sizes=sizes)
    print(f"Icon saved to {ico_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python png_to_ico.py image.png [output.ico]")
    else:
        png_file = sys.argv[1]
        ico_file = sys.argv[2] if len(sys.argv) > 2 else None
        png_to_ico(png_file, ico_file)
