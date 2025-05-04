import os
import gi
from gi.repository import Gio
import logging

# Set up logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Register resources
resource_path = os.path.join(os.path.dirname(__file__), 'resources.gresource')
try:
    resource = Gio.Resource.load(resource_path)
    Gio.resources_register(resource)
except Exception as e:
    logger.error(f"Failed to load resources: {e}")
