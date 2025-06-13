import hashlib

def checksum(file_path: str, algorithm: str = "md5") -> str:
    # This comment is in English
    try:
        h = hashlib.new(algorithm)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        print(e)
        return -1