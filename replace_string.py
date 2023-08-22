import os
import argparse

def replace_content(path, old_string, new_string, preview, verbose):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_string in content:  # Prüfen, ob der alte String im Inhalt vorkommt
        new_content = content.replace(old_string, new_string)
        
        if verbose:
            print(f"Replacing content in: {path}")
            
        if not preview:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)

def process_directory(base_path, old_string, new_string, recursive, folder, files, content, preview, verbose, hidden):
    for root, dirs, filenames in os.walk(base_path):
        # Wenn "hidden" nicht gesetzt ist, versteckte Dateien/Ordner aus der Liste entfernen
        if not hidden:
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            filenames = [f for f in filenames if not f.startswith(".")]

        if content:
            for f in filenames:
                replace_content(os.path.join(root, f), old_string, new_string, preview, verbose)

        if files:
            for f in filenames:
                if old_string in f:
                    old_path = os.path.join(root, f)
                    new_path = os.path.join(root, f.replace(old_string, new_string))
                    if verbose:
                        print(f"Renaming file from: {old_path} to: {new_path}")
                    if not preview:
                        os.rename(old_path, new_path)
                        
        if folder:
            for d in dirs:
                if old_string in d:
                    old_path = os.path.join(root, d)
                    new_path = os.path.join(root, d.replace(old_string, new_string))
                    if verbose:
                        print(f"Renaming directory from: {old_path} to: {new_path}")
                    if not preview:
                        os.rename(old_path, new_path)
                    
        if not recursive:
            break

def main():
    parser = argparse.ArgumentParser(description="Replace strings in directories and files.")
    parser.add_argument('path', help="Path in which replacements should be made.")
    parser.add_argument('old_string', help="The string to be replaced.")
    parser.add_argument('new_string', nargs='?', default="", help="The string to replace with. Default is empty string.")
    parser.add_argument('--recursive', action='store_true', help="Replace in all subdirectories and files.")
    parser.add_argument('--folder', action='store_true', help="Replace in folder names.")
    parser.add_argument('--files', action='store_true', help="Replace in file names.")
    parser.add_argument('--content', action='store_true', help="Replace inside file contents.")
    parser.add_argument('--preview', action='store_true', help="Preview changes without replacing.")
    parser.add_argument('--verbose', action='store_true', help="Verbose mode.")
    parser.add_argument('--hidden', action='store_true', help="Apply to hidden files and folders.")
    args = parser.parse_args()

    process_directory(args.path, args.old_string, args.new_string, args.recursive, args.folder, args.files, args.content, args.preview, args.verbose, args.hidden)

if __name__ == "__main__":
    main()
