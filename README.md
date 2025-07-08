# Bulk String Replacer CLI (bsr) 🔄

[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub%20Sponsors-blue?logo=github)](https://github.com/sponsors/kevinveenbirkenbach) [![Patreon](https://img.shields.io/badge/Support-Patreon-orange?logo=patreon)](https://www.patreon.com/c/kevinveenbirkenbach) [![Buy Me a Coffee](https://img.shields.io/badge/Buy%20me%20a%20Coffee-Funding-yellow?logo=buymeacoffee)](https://buymeacoffee.com/kevinveenbirkenbach) [![PayPal](https://img.shields.io/badge/Donate-PayPal-blue?logo=paypal)](https://s.veen.world/paypaldonate)

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.en.html) [![GitHub stars](https://img.shields.io/github/stars/kevinveenbirkenbach/bulk-string-replacer.svg?style=social)](https://github.com/kevinveenbirkenbach/bulk-string-replacer/stargazers)

Bulk String Replacer CLI (bsr) is a powerful Python-based command-line tool that lets you search and replace strings in file names, folder names, and within file contents across multiple directories. Perfect for performing bulk updates quickly and efficiently, bsr supports recursive traversal, hidden files, and a preview mode so you can review changes before they’re applied. 🔧📂

---

## 🛠 Features

* **Comprehensive Replacement:** Replace strings in folder names, file names, and inside file contents.
* **Recursive Processing:** Traverse directories recursively to update all matching files.
* **Hidden Files Support:** Option to include hidden files and directories.
* **Preview Mode:** Preview changes without modifying any files.
* **Verbose Output:** Display detailed logs of the operations performed.
* **Full-Path Moves:** Match an `old_string` as a relative path (including `/`) and move matching subtrees to a new location.

---

## 📥 Installation

Install Bulk String Replacer CLI easily via [Kevin's Package Manager](https://github.com/kevinveenbirkenbach/package-manager) under the alias `bsr`:

```bash
package-manager clone bsr
package-manager install bsr
```

This command makes the tool globally available as `bsr` in your terminal. 🚀

---

## 🚀 Usage

Once installed, run Bulk String Replacer CLI using the alias:

```bash
bsr old_string -n "replacement_value" [options] [paths...]
```

### Options

* **`old_string`**: The string or relative path to search for.
* **`-n, --new`**: The replacement string or new relative path (default is empty string).
* **`-r, --recursive`**: Recurse into all subdirectories and files.
* **`-F, --folders`**: Replace occurrences within folder names.
* **`-f, --files`**: Replace occurrences within file names.
* **`-c, --content`**: Replace occurrences inside file contents.
* **`-P, --path`**: Match `old_string` as a relative path (e.g. `vars/config.yml`) and move matching subtree to `new` relative path.
* **`-p, --preview`**: Preview changes without applying them.
* **`-v, --verbose`**: Display detailed logs during execution.
* **`-H, --hidden`**: Include hidden files and directories in the operation.

### Examples

Replace text within filenames, folder names, and file contents:

```bash
bsr "old_value" -n "new_value" -r -F -f -c /path/to/dir
```

Move every `vars/configuration.yml` to `config/main.yml` in each parent directory:

```bash
bsr "vars/configuration.yml" -n "config/main.yml" -r -P ./
```

Preview a full-path move without changes:

```bash
bsr "vars/configuration.yml" -n "config/main.yml" -r -P -p ./
```

---

## 🧑‍💻 Author

Developed by **Kevin Veen-Birkenbach**

* 📧 [kevin@veen.world](mailto:kevin@veen.world)
* 🌐 [https://www.veen.world/](https://www.veen.world/)

Learn more about the development of this tool in the [original ChatGPT conversation](https://chat.openai.com/share/cfdbc008-8374-47f8-8853-2e00ee27c959).

---

## 📜 License

This project is licensed under the **GNU Affero General Public License, Version 3, 19 November 2007**.
For more details, see the [LICENSE](./LICENSE) file.

---

## 🤝 Contributions

Contributions are welcome! Feel free to fork the repository, submit pull requests, or open issues to help improve Bulk String Replacer CLI. Let’s make bulk updates even easier! 😊
