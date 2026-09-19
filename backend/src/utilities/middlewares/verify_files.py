from src.utilities.handlers.http_exceptions import BadRequest
import magic, os, uuid
from fastapi import UploadFile

ALLOWED_EXTENSIONS = {
    "pdf", "docx", "xlsx", "png", "jpg", "jpeg", "txt"
}

BLOCKED_TYPES = [
    "application/x-msdownload",  # .exe
    "application/x-sh",         # scripts
    "application/x-python",
    "application/javascript"
]

def verify_extension(file, complementary_message = None):
    ext = file.filename.split(".")[-1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise BadRequest(f"Tipo de archivo no permitido. {complementary_message}")
    
    return ext


def verify_mime(file):
    mime = magic.from_buffer(
        file,
        mime=True
    )

    if mime in BLOCKED_TYPES:
        raise BadRequest("Tipo MIME bloqueado.")

    return mime


def clean_name(file):
    return os.path.basename(file.filename)


def create_secure_name(filename: str) -> str:
    ext = filename.split(".")[-1].lower()
    return f"{uuid.uuid4()}.{ext}"