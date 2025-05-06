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
    azure_container = os.environ.get('AZURE_STATIC_CONTAINER', 'static')
    
class AzureMediaStorage(CustomAzureStorage):
    """
    Storage class specifically for media files.
    """
    azure_container = os.environ.get('AZURE_STORAGE_CONTAINER', 'media') 