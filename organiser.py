import pathlib
from constant import FILE_CATEGORIES
import shutil


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
    

def move_file(source, destination):
    try:
        if destination.exists():
            destination.unlink() 

        shutil.move(str(source), str(destination))
        print(f"Moved: {source.name} -> {destination.parent.name}")
        return True

    except Exception as e:
        print(f"Error moving {source.name}: {e}")
        return False

def write_log(action, source, destination=None):
    with open("moves.txt", "a") as file:
        if destination is not None:
            file.write(f"{action} | {source.name} -> {destination.parent.name}/{destination.name}\n")
        else:
            file.write(f"{action} | {source.name}\n")   

def display_summary(moved, skipped, renamed, failed):
    print("\nOrganization Complete!")
    print(f"Moved   : {moved}")
    print(f"Renamed : {renamed}")
    print(f"Skipped : {skipped}")
    print(f"Failed  : {failed}")

def main():
    path = folder_path()
    print("Scanning folder...")
    files = scan_folder(path)
    print(f"Found {len(files)} files.")
    if not files:
        print("Folder contains no files.")
        return
    duplicate_mode = None

    moved = 0
    skipped = 0
    renamed = 0
    failed = 0

    for file in files:
        category = categorize_file(file)
        category_folder = create_category_folder(path, category)
        destination = category_folder / file.name
        original_destination = destination

        if destination.exists():
            destination, duplicate_mode = duplicate_handler(
                file,
                destination,
                duplicate_mode
            )

            if destination is not None and destination != original_destination:
                renamed += 1

        if destination is not None:
            if move_file(file, destination):
                if destination != original_destination:
                    write_log("Renamed and Moved", file, destination)
                else:
                    write_log("Moved", file, destination)
                    
                moved += 1
            else:
                write_log("Failed to move", file)
                failed += 1
        else:
            write_log("Skipped", file)
            skipped += 1

    display_summary(moved, skipped, renamed, failed)


if __name__ == "__main__":
    main()