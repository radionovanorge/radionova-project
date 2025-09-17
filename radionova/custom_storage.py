from storages.backends.azure_storage import AzureStorage
import mimetypes
import os
import logging

logger = logging.getLogger(__name__)


class CustomAzureStorage(AzureStorage):
    def get_content_type(self, content=None, filename=None):
        """
        Get the content type for the file based on its filename.
        This ensures proper MIME types are set when uploading to Azure.
        """
        if filename:
            content_type, encoding = mimetypes.guess_type(filename)
            if content_type:
                logger.info(f"Content type for {filename}: {content_type}")
                return content_type

        # Default to the standard behavior if we can't determine the content type
        return super().get_content_type(content, filename)

    def url(self, name):
        url = super().url(name)
        logger.info(f"Generated URL for {name}: {url}")
        return url


class AzureStaticStorage(CustomAzureStorage):
    """
    Storage class specifically for static files.
    """

    azure_container = "static"


class AzureMediaStorage(CustomAzureStorage):
    """
    Storage class specifically for media files.
    """

    azure_container = "media"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        custom_container = os.environ.get("AZURE_STORAGE_CONTAINER")
        if custom_container:
            self.azure_container = custom_container
