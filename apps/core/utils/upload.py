import uuid
import os


def upload_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    folder = instance.__class__.__name__.lower()

    return os.path.join(folder, filename)