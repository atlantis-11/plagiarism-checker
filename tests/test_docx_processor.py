import sys
import unittest
from unittest.mock import patch
from zipfile import BadZipFile

sys.path.append("..")
from docx_processor import docx2txt_process

class TestDocxProcessor(unittest.TestCase):

    @patch('cache_manager.CacheManager.get')
    @patch('cache_manager.CacheManager.put')
    @patch('docx2txt.process')
    def test_docx2txt_process_no_cache(self, mock_process, mock_cache_put, mock_cache_get):
        file_path = 'test.docx'
        expected_text = 'Test document content'

        mock_cache_get.return_value = None
        mock_process.return_value = expected_text

        result = docx2txt_process(file_path)

        mock_process.assert_called_once_with(file_path)
        mock_cache_put.assert_called_once_with(file_path, expected_text)
        self.assertEqual(result, expected_text)

    @patch('cache_manager.CacheManager.get')
    @patch('cache_manager.CacheManager.put')
    @patch('docx2txt.process')
    def test_docx2txt_process_with_cache(self, mock_process, mock_cache_put, mock_cache_get):
        file_path = 'test.docx'
        expected_text = 'Test document content'

        mock_cache_get.return_value = expected_text

        result = docx2txt_process(file_path)

        mock_process.assert_not_called()
        mock_cache_put.assert_not_called()
        self.assertEqual(result, expected_text)

    @patch('docx2txt.process', side_effect=BadZipFile)
    def test_docx2txt_process_bad_zip_file_exception(self, mock_process):
        file_path = 'test.docx'

        with self.assertRaises(BadZipFile) as context:
            docx2txt_process(file_path)

        self.assertEqual(str(context.exception), f'"{file_path}" is not a docx file')

    @patch('docx2txt.process', side_effect=FileNotFoundError)
    def test_docx2txt_process_file_not_found_exception(self, mock_process):
        file_path = 'test.docx'

        with self.assertRaises(FileNotFoundError) as context:
            docx2txt_process(file_path)

        self.assertEqual(str(context.exception), f'"{file_path}" not found')

    @patch('docx2txt.process', side_effect=Exception)
    def test_docx2txt_process_generic_exception(self, mock_process):
        file_path = 'test.docx'

        with self.assertRaises(Exception) as context:
            docx2txt_process(file_path)

        self.assertEqual(str(context.exception), f'Error processing "{file_path}"')

if __name__ == '__main__':
    unittest.main()
