# Photo Sorter (Python)

This Python program automates the process of organizing and renaming photos in bulk using EXIF metadata (when available) or creation timestamps. It is ideal for batch-processing personal image collections to maintain clean and chronological photo folders.

## Features

- Sorts images into subfolders based on the date they were taken (e.g., "2024-06")
- Automatically renames photos using a user-defined naming pattern or a default sequence
- Creates missing folders and adds a placeholder image to demonstrate functionality
- Extracts metadata using the Pillow (PIL) library
- User-friendly prompts for folder creation, naming, and processing status

## Technologies Used

- Python 3.8+
- [Pillow (PIL)](https://pypi.org/project/Pillow/) for image handling and metadata extraction
- Built-in libraries: `os`, `shutil`, `datetime`, `csv`

## Setup & Requirements

Make sure Python is installed. Install the Pillow library if you don’t have it:

```bash
pip install pillow
