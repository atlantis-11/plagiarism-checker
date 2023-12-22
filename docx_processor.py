import docx2txt
from zipfile import BadZipFile
from cache_manager import CacheManager

def docx2txt_process(file_path):
    try:
        txt = CacheManager.get(file_path)
        if txt is None:
            txt = docx2txt.process(file_path)
            CacheManager.put(file_path, txt)
        return txt
    except BadZipFile:
        raise BadZipFile(f'"{file_path}" is not a docx file')
    except FileNotFoundError:
        raise FileNotFoundError(f'"{file_path}" not found')
    except:
        raise Exception(f'Error processing "{file_path}"')