import shutil
import os

def replace_directory_contents(target_dir, source_dir):
    # Ensure target directory exists
    if not os.path.exists(target_dir):
        print(f"Target directory {target_dir} does not exist. Creating it.")
        os.makedirs(target_dir)
    
    # Step 1: Remove the contents of the target directory
    print(f"Starting to clear contents of {target_dir}")
    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)
        if os.path.isdir(item_path):
            print(f"Removing directory: {item_path}")
            shutil.rmtree(item_path)  # Recursively delete directory
        else:
            print(f"Removing file: {item_path}")
            os.remove(item_path)     # Delete file
    
    # Step 2: Copy contents from source directory to target directory
    print(f"Starting to copy contents from {source_dir} to {target_dir}")
    for item in os.listdir(source_dir):
        src_path = os.path.join(source_dir, item)
        dst_path = os.path.join(target_dir, item)
        if os.path.isdir(src_path):
            print(f"Copying directory from {src_path} to {dst_path}")
            shutil.copytree(src_path, dst_path)  # Recursively copy directory
        else:
            print(f"Copying file from {src_path} to {dst_path}")
            shutil.copy2(src_path, dst_path)     # Copy files

    print("Replacement of directory contents completed.")