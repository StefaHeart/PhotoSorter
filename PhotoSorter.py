"""
This program will help sort and rename photo files in batches. 
This is to help save time when completing file management and organization.
The test program will create a .jpg and prompt user to create a folder and 
then run the rest of the program to show functionality.  
"""

""" Instructions
1. Run the Program  
2. This program requires Pillow or PIL (Python Imaging Library) for image metadata extraction.
3. If Pillow is not intalled, the program will give a message to the user to install PIL
4. The user will get instructions on how to install inside the error message 
5. Once PIL is installed run the program
6. User will be prompted to enter the name of the folder they want to sort, enter folder name 
7. If the program finds the folder it will prompt user to enter the photo name
8. If the folder is not found the program will ask the user to create one with a Y/N
9. If Y the input name for the folder will be created 
10. The program will run and the output will be placed in a folder called Sorted_Photos with the custom/defaul naming convention
"""

import os                       # Access files and directories
import shutil                   # Allows file movement and renaming 
import csv                      # Enables reading and writing of CSV files
from datetime import datetime   # Provides date and time handling
from PIL import Image           # Allows image creation

# Check for Pillow installation. 
# If not installed give a message to tell the user to manually install with instructions
try:
    from PIL import Image
    from PIL.ExifTags import TAGS
except ImportError:
    print("Error: Pillow (PIL) is not installed.")
    print("Please install it manually by opening CMD and running: pip install pillow")
    input("Press Enter to exit...")  # Keeps the message on screen until user acknowledges
    quit()

# Main function to run the program
def main():
    # Ask the user for the folder containing images
    input_folder = input("Enter the name of the folder containing your images: ").strip()

    # Check if the folder exists
    if not os.path.exists(input_folder):
        print(f"The folder '{input_folder}' does not exist.")
        create_folder = input("Would you like to create this folder? (yes/no): ").strip().lower()
        if create_folder == "yes":
            os.makedirs(input_folder)
            print(f"Folder '{input_folder}' has been created.")

            # Create a blank image file - ensures program runs without real images
            blank_image_path = os.path.join(input_folder, "placeholder.jpg")
            image = Image.new("RGB", (100, 100), (255, 255, 255))  # Create a blank white image
            image.save(blank_image_path)
            print("A placeholder image (placeholder.jpg) has been created in the folder.")
        else:
            print("Exiting program. Please create the folder and add images before running again.")
            input("Press Enter to exit...")
            return  # Exit the function
        
    # **Ensure the program recognizes the newly created folder**
    if not os.path.exists(input_folder):
        print(f"Error: The folder '{input_folder}' was not created successfully. Please try again.")
        input("Press Enter to exit...")
        return

    # Define the output folder
    output_folder = "Sorted_Photos"  # This will be created automatically
    rename_pattern = "photo_###"

    # Run the sorting function
    rename_and_sort_images(input_folder, output_folder, rename_pattern)

"""Function to extract the date the photo was taken from EXIF metadata
EXIF (Exchnageable Image File Format) metadata is embedded in image files taken
by digital cameras and smartphones. 
This function extracts the DateTimeOriginal tag"""

def extract_exif_date(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                if TAGS.get(tag) == "DateTimeOriginal":
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"Error extracting EXIF data from {image_path}: {e}")
    return None

# Function to rename and sort images into folders based on the date taken
def rename_and_sort_images(input_folder, output_folder, rename_pattern=None):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    counter = 1
    custom_name = None
    
    # Allow the user to specify a single custom name for all files
    if rename_pattern:
        custom_name = input("Enter a custom name for all photos (leave blank to use default pattern): ").strip()
        
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            file_path = os.path.join(input_folder, filename)
                
            # Get date taken from EXIF metadata or fallback to file creation date
            date_taken = extract_exif_date(file_path) or datetime.fromtimestamp(os.path.getctime(file_path))
            folder_name = date_taken.strftime("%Y-%m")
            folder_path = os.path.join(output_folder, folder_name)
            os.makedirs(folder_path, exist_ok=True)
                
            # Generate new filename based on user input or default pattern
            if custom_name:
                new_name = f"{custom_name}_{str(counter).zfill(3)}{os.path.splitext(filename)[1]}"
            else:
                new_name = rename_pattern.replace("###", str(counter).zfill(3)) + os.path.splitext(filename)[1]
                
            new_path = os.path.join(folder_path, new_name)
                
            # Move and rename file
            shutil.move(file_path, new_path)
            print(f"Processed: {filename} -> {new_name} in {folder_name}")
                
            counter += 1
    
    print("Batch processing complete! Photos sorted and renamed.")

if __name__ == "__main__":
    main()

