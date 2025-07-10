#!/usr/bin/env python3
import os
import shutil
import tempfile
import unittest
import argparse

from main import process_directory, replace_content, main as cli_main

class TestBulkStringReplacer(unittest.TestCase):
    def setUp(self):
        # create isolated temp dir
        self.base = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.base)

    def create_file(self, relpath, content=''):
        full = os.path.join(self.base, relpath)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8') as f:
            f.write(content)
        return full

    def test_replace_content(self):
        f = self.create_file('foo.txt', 'hello OLD world')
        replace_content(f, 'OLD', 'NEW', preview=False, verbose=False)
        with open(f, 'r', encoding='utf-8') as fp:
            self.assertIn('hello NEW world', fp.read())

    def test_rename_file(self):
        f = self.create_file('OLDfile.txt', '')
        process_directory(
            base_path=self.base,
            old_string='OLD', new_string='NEW',
            recursive=False,
            rename_folders=False, rename_files=True,
            replace_in_content=False,
            preview=False, verbose=False,
            include_hidden=True, rename_paths=False, auto_path=True
        )
        self.assertTrue(os.path.exists(os.path.join(self.base, 'NEWfile.txt')))
        self.assertFalse(os.path.exists(f))

    def test_rename_folder(self):
        os.makedirs(os.path.join(self.base, 'OLDfolder', 'x'))
        process_directory(
            base_path=self.base,
            old_string='OLD', new_string='NEW',
            recursive=False,
            rename_folders=True, rename_files=False,
            replace_in_content=False,
            preview=False, verbose=False,
            include_hidden=True, rename_paths=False, auto_path=True
        )
        self.assertTrue(os.path.isdir(os.path.join(self.base, 'NEWfolder')))
        self.assertFalse(os.path.isdir(os.path.join(self.base, 'OLDfolder')))

    def test_full_path_move(self):
        cfg = 'vars/configuration.yml'
        full = self.create_file(cfg, 'DATA')
        process_directory(
            base_path=self.base,
            old_string='vars/configuration.yml',
            new_string='config/main.yml',
            recursive=True,
            rename_folders=False, rename_files=False,
            replace_in_content=False,
            preview=False, verbose=False,
            include_hidden=True, rename_paths=True, auto_path=True
        )
        self.assertFalse(os.path.exists(full))
        self.assertTrue(os.path.exists(os.path.join(self.base, 'config', 'main.yml')))

    def test_path_and_folders_conflict(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-P', dest='rename_paths', action='store_true')
        parser.add_argument('-F', dest='folders', action='store_true')
        args = parser.parse_args(['-P', '-F'])
        with self.assertRaises(SystemExit):
            if args.rename_paths and args.folders:
                parser.error("Cannot use --path and --folders together.")

    def test_preview_does_nothing(self):
        f = self.create_file('OLD.txt', 'OLD')
        os.makedirs(os.path.join(self.base, 'OLDdir'))
        process_directory(
            base_path=self.base,
            old_string='OLD', new_string='NEW',
            recursive=True,
            rename_folders=True, rename_files=True,
            replace_in_content=True,
            preview=True, verbose=False,
            include_hidden=True, rename_paths=True, auto_path=True
        )
        self.assertTrue(os.path.exists(f))
        self.assertTrue(os.path.isdir(os.path.join(self.base, 'OLDdir')))
        with open(f, 'r', encoding='utf-8') as fp:
            self.assertIn('OLD', fp.read())

    def test_module_path_replacement_in_python_files(self):
        content = 'from old/path import func'
        src = self.create_file('old/path/module.py', content)
        process_directory(
            base_path=self.base,
            old_string='old/path', new_string='old.path',
            recursive=True,
            rename_folders=False, rename_files=False,
            replace_in_content=False,
            preview=False, verbose=False,
            include_hidden=True, rename_paths=True, auto_path=True
        )
        new_path = os.path.join(self.base, 'old.path', 'module.py')
        self.assertTrue(os.path.exists(new_path))
        with open(new_path, 'r', encoding='utf-8') as fp:
            self.assertIn('from old.path import func', fp.read())

    def test_non_python_files_are_not_content_updated(self):
        content = 'some reference to old/path in text'
        txt = self.create_file('old/path/readme.txt', content)
        process_directory(
            base_path=self.base,
            old_string='old/path', new_string='old.path',
            recursive=True,
            rename_folders=False, rename_files=False,
            replace_in_content=False,
            preview=False, verbose=False,
            include_hidden=True, rename_paths=True, auto_path=True
        )
        new_txt = os.path.join(self.base, 'old.path', 'readme.txt')
        self.assertTrue(os.path.exists(new_txt))
        with open(new_txt, 'r', encoding='utf-8') as fp:
            self.assertIn('old/path', fp.read())

    def test_auto_path_line_level_replacement(self):
        # create a Python file with two occurrences
        lines = [
            'import a\n',
            'path = "old/path/to/module"\n',
            'print("old/path/example")\n'
        ]
        py = self.create_file('old/path/test.py', ''.join(lines))
        process_directory(
            base_path=self.base,
            old_string='old/path', new_string='new/path',
            recursive=True,
            rename_folders=False, rename_files=False,
            replace_in_content=False,
            preview=False, verbose=False,
            include_hidden=True, rename_paths=True, auto_path=True
        )
        new_py = os.path.join(self.base, 'new', 'path', 'test.py')
        self.assertTrue(os.path.exists(new_py))
        with open(new_py, 'r', encoding='utf-8') as fp:
            content = fp.read()
            # all replaced slash-based
            self.assertIn('path = "new/path/to/module"', content)
            self.assertIn('print("new/path/example")', content)

if __name__ == '__main__':
    unittest.main()