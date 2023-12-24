from Levenshtein import distance
from cache_manager import CacheManager
from docx_processor import docx2txt_process

def calculate_similarity(check_file, docxs_in_dir):
    results = []
    
    CacheManager.load_cache() # docx2txt_process uses cache

    try:
        txt1 = docx2txt_process(check_file)
    except Exception as e:
        print(e)
        exit()

    for docx_in_dir in docxs_in_dir:
        try:
            txt2 = docx2txt_process(docx_in_dir)
        except Exception as e:
            print(e)
            exit()

        len_txt1 = len(txt1)
        len_txt2 = len(txt2)

        distance_value = distance(txt1, txt2)

        similarity_percentage = 100 - (distance_value / max(len_txt1, len_txt2)) * 100

        results.append([docx_in_dir, round(similarity_percentage, 2)])

    sorted_res = sorted(results, key=lambda x: x[1], reverse=True)

    return sorted_res