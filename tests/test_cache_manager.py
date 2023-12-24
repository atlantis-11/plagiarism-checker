import os
import sys
import unittest
import json
import hashlib
from unittest.mock import patch
from tempfile import TemporaryDirectory

sys.path.append("..")
from cache_manager import CacheManager

class TestCacheManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        CacheManager.cache_file = os.path.join(self.temp_dir.name, 'cache_data.json')
        CacheManager.cache = {}

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_cache_existing_file(self):
        # Create a temporary cache file with some data
        test_data = {'abc123': 'test_content'}
        with open(CacheManager.cache_file, 'w') as file:
            json.dump(test_data, file)

        CacheManager.load_cache()

        self.assertEqual(CacheManager.cache, test_data)

    def test_load_cache_nonexistent_file(self):
        # Ensure that no error occurs when loading a nonexistent cache file
        CacheManager.load_cache()

        self.assertEqual(CacheManager.cache, {})

    def test_save_cache(self):
        # Save some data to the cache, then load it and check if it matches
        test_data = {'abc123': 'test_content'}
        CacheManager.cache = test_data
        CacheManager.save_cache()

        loaded_data = {}
        with open(CacheManager.cache_file, 'r') as file:
            loaded_data = json.load(file)

        self.assertEqual(loaded_data, test_data)

    @patch('cache_manager.CacheManager.calculate_hash', return_value='hash_value')
    def test_get_existing_data(self, mock_hash):
        # Add test data to the cache
        test_data = 'test data'
        file_path = 'test_file.docx'
        CacheManager.cache[CacheManager.calculate_hash(file_path)] = test_data

        # Check if the get method returns the correct data
        result = CacheManager.get(file_path)
        self.assertEqual(result, test_data)

    def test_get_nonexistent_data(self):
        # Check if the get method returns None for nonexistent data
        result = CacheManager.get('nonexistent_file.docx')
        self.assertIsNone(result)

    @patch('cache_manager.CacheManager.calculate_hash', return_value='hash_value')
    def test_put_data_file_exists(self, mock_hash):
        # Add test data using the put method
        test_data = 'test data'
        file_path = 'test_file.docx'

        CacheManager.put(file_path, test_data)

        # Check if the data was added to the cache and saved to the cache file
        self.assertEqual(CacheManager.cache[CacheManager.calculate_hash(file_path)], test_data)

        with open(CacheManager.cache_file, 'r') as file:
            saved_data = json.load(file)
        self.assertEqual(saved_data[CacheManager.calculate_hash(file_path)], test_data)

    @patch('cache_manager.CacheManager.calculate_hash', return_value=None)
    def test_put_data_file_doesnt_exists(self, mock_hash):
        # Add test data using the put method
        test_data = 'test data'
        file_path = 'test_file.docx'

        # Check if FileNotFoundError is raised
        with self.assertRaises(FileNotFoundError):
            CacheManager.put(file_path, test_data)

    @patch('cache_manager.CacheManager.get_metadata', return_value='metadata')
    def test_calculate_hash(self, mock_metadata):
        # Test if the calculate_hash method returns the expected hash
        file_path = 'test_file.docx'
        expected_hash = hashlib.md5('metadata'.encode('utf-8')).hexdigest()

        result = CacheManager.calculate_hash(file_path)
        self.assertEqual(result, expected_hash)

    def test_get_metadata(self):
        # Test if the get_metadata method returns the expected metadata
        file_path = os.path.join(self.temp_dir.name, 'test_file.docx')
        
        with open(file_path, 'x'): pass

        expected_metadata = {
            'size': os.path.getsize(file_path),
            'modified': os.path.getmtime(file_path),
            'created': os.path.getctime(file_path)
        }

        result = CacheManager.get_metadata(file_path)
        self.assertEqual(result, expected_metadata)

if __name__ == '__main__':
    unittest.main()
