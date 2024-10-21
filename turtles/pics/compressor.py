import os
from PIL import Image
import shutil

def compress_image(input_path, output_path, max_size_mb=1):
    with Image.open(input_path) as img:
        quality = 95
        while True:
            img.save(output_path, optimize=True, quality=quality)
            if os.path.getsize(output_path) <= max_size_mb * 1024 * 1024:
                break
            quality -= 5
            if quality < 20:
                print(f"Warning: Could not compress {input_path} below {max_size_mb}MB")
                break

def main():
    current_dir = os.getcwd()
    original_dir = os.path.join(current_dir, "original")
    
    # Create the 'original' directory if it doesn't exist
    if not os.path.exists(original_dir):
        os.makedirs(original_dir)
    
    for filename in os.listdir(current_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            file_path = os.path.join(current_dir, filename)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
            
            if file_size > 1:
                print(f"Compressing {filename} ({file_size:.2f}MB)...")
                
                # Temporary file for compression
                temp_path = os.path.join(current_dir, f"temp_{filename}")
                
                compress_image(file_path, temp_path)
                
                # Move original file to 'original' directory
                original_file_path = os.path.join(original_dir, filename)
                shutil.move(file_path, original_file_path)
                
                # Replace original file with compressed version
                os.rename(temp_path, file_path)
                
                new_size = os.path.getsize(file_path) / (1024 * 1024)
                print(f"Compressed {filename} from {file_size:.2f}MB to {new_size:.2f}MB")
            else:
                print(f"Skipping {filename} ({file_size:.2f}MB) - already under 1MB")

if __name__ == "__main__":
    main()