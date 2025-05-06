from storages.backends.azure_storage import AzureStorage
import mimetypes
import os

class CustomAzureStorage(AzureStorage):
    def get_content_type(self, content=None, filename=None):
        """
        Get the content type for the file based on its filename.
        This ensures proper MIME types are set when uploading to Azure.
        """
        if filename:
            content_type, encoding = mimetypes.guess_type(filename)
            if content_type:
                return content_type
        
        # Default to the standard behavior if we can't determine the content type
        return super().get_content_type(content, filename)

class AzureStaticStorage(CustomAzureStorage):
    """
    Storage class specifically for static files.
    """
    azure_container = 'static'  # Use the static container that already exists
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You could override this with an environment variable if needed
        # but we'll use 'static' by default since the container exists

class AzureMediaStorage(CustomAzureStorage):
    """
    Storage class specifically for media files.
    """
    azure_container = 'media'  # Use the media container that already exists
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You could override this with AZURE_STORAGE_CONTAINER env var if needed
        custom_container = os.environ.get('AZURE_STORAGE_CONTAINER')
        if custom_container:
            self.azure_container = custom_container 