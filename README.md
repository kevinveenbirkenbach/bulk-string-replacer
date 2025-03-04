# Bulk String Replacer CLI (bsr) 🔄

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.en.html) [![GitHub stars](https://img.shields.io/github/stars/kevinveenbirkenbach/bulk-string-replacer.svg?style=social)](https://github.com/kevinveenbirkenbach/bulk-string-replacer/stargazers)

Bulk String Replacer CLI (bsr) is a powerful Python-based command-line tool that lets you search and replace strings in file names, folder names, and within file contents across multiple directories. Perfect for performing bulk updates quickly and efficiently, bsr supports recursive traversal, hidden files, and a preview mode so you can review changes before they’re applied. 🔧📂

---

## 🛠 Features

- **Comprehensive Replacement:** Replace strings in folder names, file names, and inside file contents.
- **Recursive Processing:** Traverse directories recursively to update all matching files.
- **Hidden Files Support:** Option to include hidden files and directories.
- **Preview Mode:** Preview changes without modifying any files.
- **Verbose Output:** Display detailed logs of the operations performed.

---

## 📥 Installation

Install Bulk String Replacer CLI easily via [Kevin's Package Manager](https://github.com/kevinveenbirkenbach/package-manager) under the alias `bsr`:

```bash
package-manager install bsr
```

This command makes the tool globally available as `bsr` in your terminal. 🚀

---

## 🚀 Usage

Once installed, run Bulk String Replacer CLI using the alias:

```bash
bsr old_string --new-string "replacement_value" [options] [paths...]
```

### Options

- **`old_string`**: The string to search for and replace.
- **`--new-string`**: The string that will replace `old_string` (default is an empty string).
- **`--recursive`**: Process all subdirectories and files recursively.
- **`--folder`**: Replace occurrences within folder names.
- **`--files`**: Replace occurrences within file names.
- **`--content`**: Replace occurrences inside file contents.
- **`--preview`**: Preview changes without applying them.
- **`--verbose`**: Display detailed logs during execution.
- **`--hidden`**: Include hidden files and directories in the operation.

### Example Command

```bash
bsr "old_value" --new-string "new_value" --recursive --verbose /path/to/first/directory /path/to/second/directory
```

Replace `/path/to/first/directory` and `/path/to/second/directory` with the paths you wish to process.

---

## 🧑‍💻 Author

Developed by **Kevin Veen-Birkenbach**  
- 📧 [kevin@veen.world](mailto:kevin@veen.world)  
- 🌐 [https://www.veen.world/](https://www.veen.world/)

Learn more about the development of this tool in the [original ChatGPT conversation](https://chat.openai.com/share/cfdbc008-8374-47f8-8853-2e00ee27c959).

---

## 📜 License

This project is licensed under the **GNU Affero General Public License, Version 3, 19 November 2007**.  
For more details, see the [LICENSE](./LICENSE) file.

---

## 🤝 Contributions

Contributions are welcome! Feel free to fork the repository, submit pull requests, or open issues to help improve Bulk String Replacer CLI. Let’s make bulk updates even easier! 😊
