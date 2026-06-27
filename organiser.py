import pathlib


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

def scan_folder():
    pass

def get_category():
    pass

def create_category_folder():
    pass

def duplicate():
    pass

def move_file():
    pass

def write_log():
    pass    

def display_summary():
    pass

def main():
    pass