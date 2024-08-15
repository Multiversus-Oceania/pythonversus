import json
from typing import TYPE_CHECKING, Optional, List, Dict
from dataclasses import dataclass, field

from a_pythonversus.character import Character

if TYPE_CHECKING:
    from a_pythonversus import a_MvsAPI


@dataclass
class Player:
    account_id: str
    username: str
    character: Character
    team_index: int
    player_index: int
    perks: List[str]
    is_winner: bool
    damage_dealt: float = 0.0
    damage_taken: float = 0.0
    ringouts: int = 0
    ringouts_received: int = 0
    rp_delta: Optional[int] = None
    total_games_played: Optional[int] = None
    total_sets_played: Optional[int] = None


@dataclass
class Match:
    api: 'a_MvsAPI'
    match_id: Optional[str] = None
    raw_data: Optional[dict] = None
    mode: Optional[str] = None
    map: Optional[str] = None
    players: List[Player] = field(default_factory=list)
    score: Optional[List[int]] = None
    winning_team_index: Optional[int] = None

    @classmethod
    async def from_id(cls, api: 'a_MvsAPI', match_id: str) -> 'Match':
        match = cls(api=api, match_id=match_id)
        await match.fetch_data()
        return match

    async def fetch_data(self):
        if not self.match_id:
            raise ValueError("No match_id provided")

        self.raw_data = await self.api.match_api.get_match_by_id(self.match_id)
        self._parse_map()
        self._parse_mode()
        self._parse_players()
        self._parse_score()
        self._parse_winning_team()

    def _parse_map(self):
        match_map = self.raw_data.get("server_data", {}).get("GameplayConfig", {}).get("Map")
        self.map = self.api.get_map_from_key(match_map) or match_map

    def _parse_mode(self):
        self.mode = self.raw_data.get("server_data", {}).get("GameplayConfig", {}).get("ModeString")

    def _parse_players(self):
        players_data = self.raw_data.get("server_data", {}).get("GameplayConfig", {}).get("Players", {})
        player_stats = self.raw_data.get("players", {}).get("all", [])
        client_return_data = self.raw_data.get("server_data", {}).get("ClientReturnData", {})

        for account_id, player_data in players_data.items():
            username = self._get_username(account_id)
            character = self.api.character_manager.get_character_by_slug(player_data.get("Character", "Unknown"))
            team_index = player_data.get("TeamIndex", -1)
            player_index = player_data.get("PlayerIndex", -1)
            perks = player_data.get("Perks", [])

            player = Player(
                account_id=account_id,
                username=username,
                character=character,
                team_index=team_index,
                player_index=player_index,
                perks=perks,
                is_winner=False  # set this later when parsing the winning team
            )

            # Parse player stats
            for stat in player_stats:
                if stat.get("account_id") == account_id:
                    end_of_match_stats = stat.get("data", {}).get("EndOfMatchStats", {})
                    player_mission_updates = end_of_match_stats.get("PlayerMissionUpdates", {}).get(account_id, {})
                    print(f"Debug: player_mission_updates for {account_id}:")
                    print(json.dumps(player_mission_updates, indent=2))
                    player.damage_dealt = player_mission_updates.get("Stat:Game:Character:TotalDamageDealt", 0.0)
                    player.damage_taken = player_mission_updates.get("Stat:Game:Character:TotalDamageTaken", 0.0)
                    player.ringouts = player_mission_updates.get("Stat:Game:Character:TotalRingouts", 0)
                    player.ringouts_received = player_mission_updates.get("Stat:Game:Character:TotalRingoutsReceived",
                                                                          0)

                    # If ringouts_received is still 0, try to get it directly from player_mission_updates
                    if player.ringouts_received == 0:
                        player.ringouts_received = player_mission_updates.get(
                            "Stat:Game:Character:TotalRingoutsReceived", 0)

                    break

            # Parse RP Delta and other ranked data
            for _, return_data in client_return_data.items():
                account_data = return_data.get("AccountIdToReturnData", {}).get(account_id, {})
                ranked_data = account_data.get("Ranked", {})
                if ranked_data:
                    player.rp_delta = ranked_data.get("RpDelta")
                    player.total_games_played = ranked_data.get("TotalGamesPlayedForMode")
                    player.total_sets_played = ranked_data.get("TotalSetsPlayedForMode")
                    self.season = ranked_data.get("Season")
                    break

            self.players.append(player)

    def _get_username(self, account_id: str) -> str:
        for player in self.raw_data.get("players", {}).get("all", []):
            if player.get("account_id") == account_id:
                identity = player.get("identity", {})
                return identity.get("alternate").get("wb_network")[0].get("username") or "Unknown"
        return "Unknown"

    def _parse_score(self):
        self.score = self.raw_data.get("players", {}).get("all", [{}])[0].get("data", {}).get("EndOfMatchStats",
                                                                                              {}).get("Score")

    def _parse_winning_team(self):
        self.winning_team_index = self.raw_data.get("players", {}).get("all", [{}])[0].get("data", {}).get(
            "EndOfMatchStats", {}).get("WinningTeamIndex")

        # Set the is_winner flag for players
        for player in self.players:
            player.is_winner = player.team_index == self.winning_team_index

    def format_player_info(self) -> str:
        """
        Format player information for easy reading.
        """
        player_info = []
        for player in self.players:
            status = "Winner" if player.is_winner else "Loser"
            character_str = player.character.name
            info = (
                f"Player: {player.username}\n"
                f"  Account ID: {player.account_id}\n"
                f"  Character: {character_str}\n"
                f"  Team: {player.team_index}\n"
                f"  Index: {player.player_index}\n"
                f"  Status: {status}\n"
                f"  Damage Dealt: {player.damage_dealt:.2f}\n"
                f"  Damage Taken: {player.damage_taken:.2f}\n"
                f"  Ringouts: {player.ringouts}\n"
                f"  Ringouts Received: {player.ringouts_received}\n"
                f"  RP Delta: {player.rp_delta if player.rp_delta is not None else 'N/A'}\n"
                f"  Total Games Played: {player.total_games_played if player.total_games_played is not None else 'N/A'}\n"
                f"  Total Sets Played: {player.total_sets_played if player.total_sets_played is not None else 'N/A'}\n"
                f"  Perks: {', '.join(player.perks)}\n"
            )
            player_info.append(info)
        return "\n".join(player_info)

    @property
    def winners(self) -> List[Player]:
        return [player for player in self.players if player.is_winner]

    @property
    def losers(self) -> List[Player]:
        return [player for player in self.players if not player.is_winner]

    @property
    def teams(self) -> Dict[int, List[Player]]:
        teams = {}
        for player in self.players:
            if player.team_index not in teams:
                teams[player.team_index] = []
            teams[player.team_index].append(player)
        return teams


class Match1v1(Match):
    pass


class Match2v2(Match):
    pass


class MatchFFA(Match):
    pass
