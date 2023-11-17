# Bulk String Replacer

`bulk-string-replacer` is a Python-based command-line utility that allows for comprehensive search and replacement operations within file and folder names, as well as within file contents across specified directories. It's designed to handle bulk updates quickly and efficiently, with support for recursive directory traversal, hidden files, and a preview mode to review changes before they're applied.

## Author

Kevin Veen-Birkenbach
- 📧 Email: [kevin@veen.world](mailto:kevin@veen.world)
- 🌍 Website: [https://www.veen.world/](https://www.veen.world/)

## Background

Learn more about the development and use cases of this tool in the [original conversation with the developer](https://chat.openai.com/share/cfdbc008-8374-47f8-8853-2e00ee27c959).

## Getting Started

### Prerequisites

- Python 3.x
- Access to a command-line interface

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/kevinveenbirkenbach/bulk-string-replacer.git
```

Change into the project directory:

```bash
cd bulk-string-replacer
```

### Usage

Run the script with Python, specifying your target paths, the string to be replaced, and the new string:

```bash
python replace_string.py old_string --new-string new_string_value --options paths...
```

#### Options

- `old_string`: The string you want to search for and replace.
- `--new-string`: The string that will replace `old_string`. Defaults to an empty string if not specified.
- `--recursive`: Recursively process all subdirectories and files within the given paths.
- `--folder`: Replace string occurrences within folder names.
- `--files`: Replace string occurrences within file names.
- `--content`: Replace string occurrences within the contents of the files.
- `--preview`: Preview changes without applying them. No files will be modified.
- `--verbose`: Output detailed information during the execution of the script.
- `--hidden`: Include hidden files and directories in the operation.

Paths are specified at the end of the command, separated by spaces. For example:

```bash
python replace_string.py "search_string" --new-string "replacement_string" --recursive --verbose /path/to/first/directory /path/to/second/directory
```

Replace `/path/to/first/directory` and `/path/to/second/directory` with the actual paths you want to process.

## Contributions

Contributions are welcome! Please feel free to submit a pull request or open an issue on the GitHub repository.

## License

This project is open-sourced under the GNU Affero General Public License v3.0. See the `LICENSE` file for more details.