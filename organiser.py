import pathlib
from constant.py import FILE_CATEGORIES


def folder_path():
    while True:
        folder = str(input("Enter folder path containing files: ")).strip()
        path = pathlib.Path(folder)
        if not path.exists():
             print("Path does not exist.")
             continue
        if not path.is_dir():
            print("Path is not a directory.")
            continue
        return path

def validate_folder():
    pass

def scan_folder(path):
    files = []

    for item in path.iterdir():
        if item.is_file():
            files.append(item)

    return files

def categorize_file(file):
    extension = file.suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"

def create_category_folder(base_path, category):
    category_folder = base_path / category
    category_folder.mkdir(exist_ok=True)
    return category_folder
    

def duplicate_handler(source, destination, duplicate_mode):

    if duplicate_mode is None:
        print(f"{destination.name} already exists.")
        print("Choose what you want to do:")
        print("1. Overwrite")
        print("2. Skip")
        print("3. Rename")
        print("4. Overwrite All")
        print("5. Skip All")
        print("6. Rename All")

        while True:
            try:
                choice = int(input("Your choice: "))
            except ValueError:
                print("Please enter a number from 1 to 6.")
                continue

            match choice:

                case 1:       
                    return destination, None

                case 2:        
                    return None, None

                case 3:      
                    original_stem = destination.stem
                    suffix = destination.suffix
                    counter = 1

                    while destination.exists():
                        new_name = f"{original_stem} ({counter}){suffix}"
                        destination = destination.with_name(new_name)
                        counter += 1

                    return destination, None

                case 4:     
                    return destination, "overwrite"

                case 5:      
                    return None, "skip"

                case 6:     
                    original_stem = destination.stem
                    suffix = destination.suffix
                    counter = 1

                    while destination.exists():
                        new_name = f"{original_stem} ({counter}){suffix}"
                        destination = destination.with_name(new_name)
                        counter += 1

                    return destination, "rename"

                case _:
                    print("Choose a number between 1 and 6.")

    elif duplicate_mode == "overwrite":
        return destination, "overwrite"

    elif duplicate_mode == "skip":
        return None, "skip"

    elif duplicate_mode == "rename":

        original_stem = destination.stem
        suffix = destination.suffix
        counter = 1

        while destination.exists():
            new_name = f"{original_stem} ({counter}){suffix}"
            destination = destination.with_name(new_name)
            counter += 1

        return destination, "rename"
    

def move_file():
    pass

def write_log():
    pass    

def display_summary():
    pass

def main():
    pass