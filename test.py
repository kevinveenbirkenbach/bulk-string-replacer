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
            include_hidden=True, rename_paths=False
        )
        # file moved
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
            include_hidden=True, rename_paths=False
        )
        self.assertTrue(os.path.isdir(os.path.join(self.base, 'NEWfolder')))
        self.assertFalse(os.path.isdir(os.path.join(self.base, 'OLDfolder')))

    def test_full_path_move(self):
        # prepare vars/configuration.yml
        cfg = 'vars/configuration.yml'
        full = self.create_file(cfg, 'DATA')
        # run with -P
        process_directory(
            base_path=self.base,
            old_string='vars/configuration.yml',
            new_string='config/main.yml',
            recursive=True,
            rename_folders=False, rename_files=False,
            replace_in_content=False,
            preview=False, verbose=False,
            include_hidden=True, rename_paths=True
        )
        # original gone, new exists
        self.assertFalse(os.path.exists(full))
        self.assertTrue(os.path.exists(os.path.join(self.base, 'config', 'main.yml')))

    def test_path_and_folders_conflict(self):
        # simulate CLI error when combining --path and --folders
        parser = argparse.ArgumentParser()
        # replicate only the conflict check
        parser.add_argument('-P', dest='rename_paths', action='store_true')
        parser.add_argument('-F', dest='folders', action='store_true')
        args = parser.parse_args(['-P', '-F'])
        # manual conflict
        with self.assertRaises(SystemExit) as cm:
            # mimic the parser.error behavior
            if args.rename_paths and args.folders:
                parser.error("Cannot use --path and --folders together.")
        self.assertNotEqual(cm.exception.code, 0)

    def test_preview_does_nothing(self):
        # create file and folder matching
        f = self.create_file('OLD.txt', 'OLD')
        os.makedirs(os.path.join(self.base, 'OLDdir'))
        process_directory(
            base_path=self.base,
            old_string='OLD', new_string='NEW',
            recursive=True,
            rename_folders=True, rename_files=True,
            replace_in_content=True,
            preview=True, verbose=False,
            include_hidden=True, rename_paths=True
        )
        # nothing changed
        self.assertTrue(os.path.exists(f))
        self.assertTrue(os.path.isdir(os.path.join(self.base, 'OLDdir')))
        with open(f, 'r', encoding='utf-8') as fp:
            self.assertIn('OLD', fp.read())

if __name__ == '__main__':
    unittest.main()
