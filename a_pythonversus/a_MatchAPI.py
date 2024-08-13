from typing import Dict, Any, TYPE_CHECKING
if TYPE_CHECKING:
    from a_pythonversus import a_MvsAPI


class MatchAPI:
    def __init__(self, api: 'a_MvsAPI'):
        self.api = api

