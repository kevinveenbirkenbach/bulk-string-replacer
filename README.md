# bulk-string-replacer
bulk-string-replacer is a tool designed to traverse directories and perform bulk string replacement in filenames, folder names, and file contents. Whether you want to target hidden items, preview changes before execution, or recursively navigate through folders, this versatile utility has you covered.

## Author

Kevin Veen-Birkenbach  
- 📧 Email: [kevin@veen.world](mailto:kevin@veen.world)
- 🌍 Website: [https://www.veen.world/](https://www.veen.world/)

## Link to Original Conversation

For more context on how this tool was developed, you can [view the original conversation here](https://chat.openai.com/share/8567c240-3905-4521-b30e-04104015bb9b).

## Setup and Usage

1. Clone the repository:
    ```bash
    git clone https://github.com/kevinveenbirkenbach/bulk-string-replacer.git
    ```

2. Navigate to the cloned directory:
    ```bash
    cd bulk-string-replacer
    ```

3. Run the script with Python:
    ```bash
    python replace_string.py [path] [old_string] [new_string] [options]
    ```

### Options:

- `--recursive`: Replace in all subdirectories and files.
- `--folder`: Replace in folder names.
- `--files`: Replace in file names.
- `--content`: Replace inside file contents.
- `--preview`: Preview changes without making actual replacements.
- `--verbose`: Verbose mode - view detailed outputs.
- `--hidden`: Target hidden files and folders.

For more detailed options, refer to the inline script help or the aforementioned conversation.

## License

This project is licensed under the GNU Affero General Public License v3.0. The full license text is available in the `LICENSE` file of this repository.
