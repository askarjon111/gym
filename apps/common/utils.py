import mimetypes


def get_uploaded_file_type(file):
    mime_type, _ = mimetypes.guess_type(file.name)
    
    return mime_type


def user_upload_path(instance, filename):
    return f"user_{instance.user.id}/{filename}"