import sys
import unittest
from unittest.mock import patch

sys.path.append("..")
from similarity_checker import calculate_similarity

class TestCalculateSimilarity(unittest.TestCase):

    @patch('cache_manager.CacheManager.load_cache')
    @patch('similarity_checker.docx2txt_process')
    def test_calculate_similarity(self, mock_docx2txt_process, mock_load_cache):
        check_file = 'check_file.docx'
        docxs_in_dir = ['doc1.docx', 'doc2.docx', 'doc3.docx']

        mock_docx2txt_process.side_effect = [
            'abcdefgh',
            'ab123456', # 25
            'abcdef', # 75
            '123' # 0
        ]

        expected_result = [
            [docxs_in_dir[1], 75],
            [docxs_in_dir[0], 25],
            [docxs_in_dir[2], 0]
        ]

        result = calculate_similarity(check_file, docxs_in_dir)

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
