Characters = {
    "AgentSmith": {
        "name": "Agent Smith",
        "slug": "character_c036",
        "emote": "<:AgentSmithIcon:1259926284713197620>",
    },
    "AryaStark": {
        "name": "Arya Stark",
        "slug": "character_arya",
        "emote": "<:AryaStarkIcon:1268459674978488413>"
    },
    "BananaGuard": {
        "name": "Banana Guard",
        "slug": "character_bananaguard",
        "emote": "<:BananaGuardIcon:1268459677679878207>"
    },
    "Batman": {
        "name": "Batman",
        "slug": "character_batman",
        "emote": "<:BatmanIcon:1268459684973514813>"
    },
    "BlackAdam": {
        "name": "Black Adam",
        "slug": "character_C021",
        "emote": "<:BlackAdamIcon:1268459687578435647>"
    },
    "BugsBunny": {
        "name": "Bugs Bunny",
        "slug": "character_bugs_bunny",
        "emote": "<:BugsBunnyIcon:1268459689780183070>"
    },
    "Finn": {
        "name": "Finn",
        "slug": "character_finn",
        "emote": "<:FinnTheHumanIcon:1268459691894116476>"
    },
    "Garnet": {
        "name": "Garnet",
        "slug": "character_garnet",
        "emote": "<:GarnetIcon:1268459694289326151>"
    },
    "Gizmo": {
        "name": "Gizmo",
        "slug": "character_C023A",
        "emote": "<:GizmoIcon2:1268459699641258018>"
    },
    "HarleyQuinn": {
        "name": "Harley Quinn",
        "slug": "character_harleyquinn",
        "emote": "<:HarleyQuinnIcon:1268459701838938112>"
    },
    "IronGiant": {
        "name": "Iron Giant",
        "slug": "character_C017",
        "emote": "<:TheIronGiantIcon:1268459704065986581>"
    },
    "Jake": {
        "name": "Jake",
        "slug": "character_jake",
        "emote": "<:JakeLogo:980375030947004416>"
    },
    "Jason": {
        "name": "Jason",
        "slug": "character_c035",
        "emote": "<:JasonIcon:1268459708486782976>",
    },
    "Joker": {
        "name": "Joker",
        "slug": "character_c028",
        "emote": "<:JokerIcon:1268459710382739516>",
    },
    "LebronJames": {
        "name": "Lebron James",
        "slug": "character_c16",
        "emote": "<:LebronIcon:1268459712974950410>"
    },
    "Marvin": {
        "name": "Marvin",
        "slug": "character_C018",
        "emote": "<:MarvinTheMartianIcon:1268459715495727114>"
    },
    "Morty": {
        "name": "Morty",
        "slug": "character_c019",
        "emote": "<:MortyIcon:1268459718209179648>"
    },
    "Reindog": {
        "name": "Reindog",
        "slug": "character_creature",
        "emote": "<:ReindogIcon:1268459720214052925>"
    },
    "Rick": {
        "name": "Rick",
        "slug": "character_C020",
        "emote": "<:RickIcon:1268459825218453534>"
    },
    "Shaggy": {
        "name": "Shaggy",
        "slug": "character_shaggy",
        "emote": "<:ShaggyIcon:1268459729747972147>"
    },
    "SamuraiJack": {
        "name": "Samurai Jack",
        "slug": "character_c026",
        "emote": "<:SamuraiJackIcon:1268459724920193115>"
    },
    "StevenUniverse": {
        "name": "Steven Universe",
        "slug": "character_steven",
        "emote": "<:StevenUniverseIcon:1268459733858390097>"
    },
    "Stripe": {
        "name": "Stripe",
        "slug": "character_C023B",
        "emote": "<:StripeIcon:1268459735980703808>"
    },
    "Superman": {
        "name": "Superman",
        "slug": "character_superman",
        "emote": "<:SupermanIcon:1268459738014941256>"
    },
    "Taz": {
        "name": "Taz",
        "slug": "character_taz",
        "emote": "<:TazIcon:1268459827647221800>"
    },
    "TomAndJerry": {
        "name": "Tom & Jerry",
        "slug": "character_tom_and_jerry",
        "emote": "<:TomAndJerryIcon:1268459742313971734>"
    },
    "Velma": {
        "name": "Velma",
        "slug": "character_velma",
        "emote": "<:VelmaIcon:1268459747968024610>"
    },
    "WonderWoman": {
        "name": "Wonder Woman",
        "slug": "character_wonder_woman",
        "emote": "<:WonderWomanIcon:1268459749914181724>"
    }
}


def get_character_by_key(key):
    """Get character information by dictionary key."""
    return Characters.get(key.strip())


def get_character_by_slug(slug):
    """Get character information by slug."""
    slug = slug.strip().lower()
    for character in Characters.values():
        if character['slug'].lower() == slug:
            return character
    return None


def get_slug_from_name(name):
    """Get character slug from name."""
    name = name.strip().lower()
    for character in Characters.values():
        if character['name'].lower() == name:
            return character['slug']
    return None


def get_name_from_slug(slug):
    """Get character name from slug."""
    character = get_character_by_slug(slug)
    return character['name'] if character else None


def get_emote_from_slug(slug):
    """Get character emote from slug."""
    character = get_character_by_slug(slug)
    return character['emote'] if character else None


def get_emote_from_name(name):
    """Get character emote from name."""
    name = name.strip().lower()
    for character in Characters.values():
        if character['name'].lower() == name:
            return character['emote']
    return None
