#!/usr/bin/env python3
import os
import argparse

def replace_content(path, old_string, new_string, preview, verbose):
    """
    Replace occurrences of old_string with new_string inside the file at path.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if old_string in content:
            new_content = content.replace(old_string, new_string)
            print_verbose(f"Replacing content in: {path}", verbose)
            if not preview:
                with open(path, 'w', encoding='utf-8') as fw:
                    fw.write(new_content)
    except UnicodeDecodeError:
        print_verbose(f"Warning: Unicode decode error in file {path}. Skipping.", verbose)

def print_verbose(message, verbose):
    if verbose:
        print(message)

def process_directory(base_path, old_string, new_string, recursive,
                      rename_folders, rename_files, replace_in_content,
                      preview, verbose, include_hidden, rename_paths, auto_path):
    """
    Traverse directory tree and perform operations based on flags:
    - replace_in_content: replace inside file contents
    - rename_files: rename files whose names contain old_string
    - rename_folders: rename folders whose names contain old_string
    - rename_paths: match old_string as a relative path and move matching items to new_string path.
      When rename_paths is set, for each matching line in Python files, show 3 lines of context before and after,
      and prompt whether to apply slash-based or dot-based replacement, unless auto_path is True.
    """
    # Full-path move logic
    if rename_paths:
        # Move matching files and folders
        for root, dirs, files in os.walk(base_path):
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                files = [f for f in files if not f.startswith('.')]
            for name in files + dirs:
                full_src = os.path.join(root, name)
                rel = os.path.relpath(full_src, base_path)
                if old_string in rel:
                    new_rel = rel.replace(old_string, new_string)
                    full_dst = os.path.join(base_path, new_rel)
                    print_verbose(f"Moving {full_src} → {full_dst}", verbose)
                    if not preview:
                        os.makedirs(os.path.dirname(full_dst), exist_ok=True)
                        os.rename(full_src, full_dst)
            if not recursive:
                break
        # Line-by-line replacement in Python files
        for root, dirs, files in os.walk(base_path):
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                files = [f for f in files if not f.startswith('.')]
            for f in files:
                if f.endswith('.py'):
                    file_path = os.path.join(root, f)
                    print_verbose(f"Processing Python file for path replacement: {file_path}", verbose)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as ff:
                            lines = ff.readlines()
                    except UnicodeDecodeError:
                        print_verbose(f"Warning: Unicode decode error in file {file_path}. Skipping.", verbose)
                        continue
                    old_slash = old_string.replace('/', os.sep)
                    new_dot = new_string.replace('/', '.')
                    changed = False
                    for idx, line in enumerate(lines):
                        if old_slash in line:
                            # Show context
                            start = max(0, idx - 3)
                            end = min(len(lines), idx + 4)
                            print(f"\nContext for replacement in {file_path}, line {idx+1}:")
                            for i in range(start, end):
                                prefix = '>' if i == idx else ' '
                                print(f"{prefix} {i+1}: {lines[i].rstrip()}")
                            # Determine replacement style
                            if auto_path:
                                choice = '1'
                            else:
                                choice = None
                                while choice not in ('1', '2'):
                                    choice = input(
                                        f"Replace this line:\n"
                                        f"  1) slash-based: '{old_slash}' → '{new_string}'\n"
                                        f"  2) dot-based:   '{old_slash}' → '{new_dot}'\n"
                                        f"Choose [1/2]: "
                                    ).strip()
                            if choice == '1':
                                lines[idx] = line.replace(old_slash, new_string)
                            else:
                                lines[idx] = line.replace(old_slash, new_dot)
                            changed = True
                            print_verbose(f"Replaced line {idx+1} in {file_path}", verbose)
                    if changed and not preview:
                        with open(file_path, 'w', encoding='utf-8') as fw:
                            fw.writelines(lines)
            if not recursive:
                break
        # Only return early when only path-mode is active
        if not (rename_files or replace_in_content):
            return

    # Collect folder renames to apply after traversal
    folders_to_rename = []
    for root, dirs, files in os.walk(base_path):
        if not include_hidden:
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]

        # Content replacement
        if replace_in_content:
            for f in files:
                replace_content(os.path.join(root, f), old_string, new_string, preview, verbose)

        # File renaming
        if rename_files:
            for f in files:
                if old_string in f:
                    src = os.path.join(root, f)
                    dst = os.path.join(root, f.replace(old_string, new_string))
                    print_verbose(f"Renaming file: {src} → {dst}", verbose)
                    if not preview:
                        os.rename(src, dst)

        # Gather folder renames
        if rename_folders:
            for d in dirs:
                if old_string in d:
                    src = os.path.join(root, d)
                    dst = os.path.join(root, d.replace(old_string, new_string))
                    folders_to_rename.append((src, dst))

        if not recursive:
            break

    # Apply folder renames
    for src, dst in folders_to_rename:
        print_verbose(f"Renaming directory: {src} → {dst}", verbose)
        if not preview:
            os.rename(src, dst)

def main():
    parser = argparse.ArgumentParser(
        description="Bulk string replacer with optional full-path moves."
    )
    parser.add_argument('paths', nargs='+', help="Base directories to process.")
    parser.add_argument('old_string', help="String or relative path to replace.")
    parser.add_argument('-n', '--new', dest='new_string', default='',
                        help="Replacement string or new relative path.")
    parser.add_argument('-r', '--recursive', action='store_true',
                        help="Recurse into subdirectories.")
    parser.add_argument('-F', '--folders', action='store_true',
                        help="Rename folder names.")
    parser.add_argument('-f', '--files', action='store_true',
                        help="Rename file names.")
    parser.add_argument('-c', '--content', action='store_true',
                        help="Replace inside file contents.")
    parser.add_argument('-p', '--preview', action='store_true',
                        help="Preview only; no changes.")
    parser.add_argument('-P', '--path', dest='rename_paths', action='store_true',
                        help="Match old_string as relative path and move to new_string path.")
    parser.add_argument('-y', '--yes', dest='auto_path', action='store_true',
                        help="Skip prompts in Python files and apply slash-based replacement by default.")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Verbose mode.")
    parser.add_argument('-H', '--hidden', action='store_true',
                        help="Include hidden files and folders.")

    args = parser.parse_args()

    # Disallow using --path and --folders together
    if args.rename_paths and args.folders:
        parser.error("Cannot use --path and --folders together.")

    base_paths = [os.path.expanduser(p) for p in args.paths]
    for base in base_paths:
        print_verbose(f"Processing: {base}", args.verbose)
        process_directory(
            base_path=base,
            old_string=args.old_string,
            new_string=args.new_string,
            recursive=args.recursive,
            rename_folders=args.folders,
            rename_files=args.files,
            replace_in_content=args.content,
            preview=args.preview,
            verbose=args.verbose,
            include_hidden=args.hidden,
            rename_paths=args.rename_paths,
            auto_path=args.auto_path
        )

if __name__ == '__main__':
    main()
