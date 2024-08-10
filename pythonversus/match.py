class Match:
    """
    Represents a Match that has been played.
    """
    id = None
    players = []
    mode = None
    raw_data = None

    def __init__(self, match_info):
        self.raw_data = match_info
        self.id = int(match_info["matches"]["id"])