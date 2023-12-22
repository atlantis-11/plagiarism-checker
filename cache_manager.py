import os
import json
import hashlib

class CacheManager:
    cache_file = 'cache_data.json'
    cache = {}

    @staticmethod
    def load_cache():
        if os.path.exists(CacheManager.cache_file):
            with open(CacheManager.cache_file, 'r') as file:
                CacheManager.cache = json.load(file)

    @staticmethod
    def save_cache():
        with open(CacheManager.cache_file, 'w') as file:
            json.dump(CacheManager.cache, file)

    @staticmethod
    def get(file_path):
        file_hash = CacheManager.calculate_hash(file_path)
        cached_data = CacheManager.cache.get(file_hash)
        if cached_data:
            return cached_data
        return None

    @staticmethod
    def put(file_path, txt_data):
        file_hash = CacheManager.calculate_hash(file_path)
        CacheManager.cache[file_hash] = txt_data
        CacheManager.save_cache()

    @staticmethod
    def calculate_hash(file_path):
        file_metadata = CacheManager.get_metadata(file_path)
        return hashlib.md5(str(file_metadata).encode('utf-8')).hexdigest()

    @staticmethod
    def get_metadata(file_path):
        return {
            'size': os.path.getsize(file_path),
            'modified': os.path.getmtime(file_path),
            'created': os.path.getctime(file_path)
        }