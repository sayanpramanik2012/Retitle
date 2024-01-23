# file/file_renamer.py
import os

def rename_files(directory_path, remove_prefix, remove_postfix, prefix_entry, postfix_entry):
    # Get the list of files in the specified directory
    files = os.listdir(directory_path)

    # Iterate through each file in the directory
    for filename in files:
        # Split the filename and extension
        name, extension = os.path.splitext(filename)

        # Check if the filename starts with the specified prefix
        if remove_prefix and name.startswith(prefix_entry.get()):
            name = name[len(prefix_entry.get()):]

        # Check if the filename ends with the specified postfix
        if remove_postfix and name.endswith(postfix_entry.get()):
            name = name[:-len(postfix_entry.get())]

        # Construct the full paths for the old and new filenames
        old_path = os.path.join(directory_path, filename)
        new_path = os.path.join(directory_path, f"{name}{extension}")

        # Rename the file
        os.rename(old_path, new_path)

        # Print a message indicating the renaming process
        print(f'Renamed: {filename} to {name}{extension}')
