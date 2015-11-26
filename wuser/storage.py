from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):
    """
    Returns same name for existing file and deletes existing file on save.
    """
    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(OverwriteStorage, self)._save(name, content)

    def get_available_name(self, name):
        return name