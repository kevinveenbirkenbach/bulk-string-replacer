#!/usr/bin/env python3
import os
import shutil
import tempfile
import unittest

from main import process_directory, replace_content

class TestBulkStringReplacer(unittest.TestCase):
    def setUp(self):
        # Create an isolated temporary directory for each test
        self.base = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up when done
        shutil.rmtree(self.base)

    def create_file(self, relpath, content=''):
        """Helper: make a file (and any parent dirs) under self.base."""
        full = os.path.join(self.base, relpath)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8') as f:
            f.write(content)
        return full

    def test_replace_content(self):
        f = self.create_file('foo.txt', 'hello old world')
        replace_content(f, 'old', 'new', preview=False, verbose=False)
        with open(f, 'r', encoding='utf-8') as fp:
            self.assertIn('hello new world', fp.read())

    def test_rename_file(self):
        f = self.create_file('oldfile.txt', '')
        process_directory(
            base_path=self.base,
            old_string='old',
            new_string='new',
            recursive=False,
            rename_folders=False,
            rename_files=True,
            replace_in_content=False,
            preview=False,
            verbose=False,
            include_hidden=True,
            rename_paths=False
        )
        self.assertTrue(os.path.exists(os.path.join(self.base, 'newfile.txt')))
        self.assertFalse(os.path.exists(f))

    def test_rename_folder(self):
        os.makedirs(os.path.join(self.base, 'oldfolder', 'inner'))
        process_directory(
            base_path=self.base,
            old_string='old',
            new_string='new',
            recursive=False,
            rename_folders=True,
            rename_files=False,
            replace_in_content=False,
            preview=False,
            verbose=False,
            include_hidden=True,
            rename_paths=False
        )
        self.assertTrue(os.path.isdir(os.path.join(self.base, 'newfolder')))
        self.assertFalse(os.path.isdir(os.path.join(self.base, 'oldfolder')))

    def test_full_path_move(self):
        # Create nested path vars/configuration.yml
        cfg = 'vars/configuration.yml'
        full_cfg = self.create_file(cfg, 'x')
        # Now move vars/configuration.yml -> config/main.yml
        process_directory(
            base_path=self.base,
            old_string='vars/configuration.yml',
            new_string='config/main.yml',
            recursive=True,
            rename_folders=False,
            rename_files=False,
            replace_in_content=False,
            preview=False,
            verbose=False,
            include_hidden=True,
            rename_paths=True
        )
        # Original should be gone
        self.assertFalse(os.path.exists(full_cfg))
        # New location should exist
        self.assertTrue(os.path.exists(os.path.join(self.base, 'config', 'main.yml')))

    def test_preview_mode(self):
        # Create file and folder that would match
        f = self.create_file('oldfile.txt', 'old')
        os.makedirs(os.path.join(self.base, 'oldfolder'))
        process_directory(
            base_path=self.base,
            old_string='old',
            new_string='new',
            recursive=True,
            rename_folders=True,
            rename_files=True,
            replace_in_content=True,
            preview=True,
            verbose=False,
            include_hidden=True,
            rename_paths=True
        )
        # Nothing changed
        self.assertTrue(os.path.exists(f))
        self.assertTrue(os.path.isdir(os.path.join(self.base, 'oldfolder')))
        with open(f, 'r', encoding='utf-8') as fp:
            self.assertIn('old', fp.read())

if __name__ == '__main__':
    unittest.main()
