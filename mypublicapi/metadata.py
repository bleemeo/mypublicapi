
from rest_framework.metadata import BaseMetadata


class MyMetadata(BaseMetadata):
    """
    Don't include field and other information for `OPTIONS` requests.
    Just return the name and description.
    """
    def determine_metadata(self, request, view):
        return {
            'name': view.get_view_name(),
            'description': view.get_view_description(),
            'renders': [renderer.media_type for renderer in view.renderer_classes],
            'parses': [parser.media_type for parser in view.parser_classes],
        }
