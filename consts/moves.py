MOVE_MAP = {
    0x00: "NO_MOVE",
    0x01: "POUND",
    0x02: "KARATE_CHOP",
    0x03: "DOUBLESLAP",
    0x04: "COMET_PUNCH",
    0x05: "MEGA_PUNCH",
    0x06: "PAY_DAY",
    0x07: "FIRE_PUNCH",
    0x08: "ICE_PUNCH",
    0x09: "THUNDERPUNCH",
    0x0A: "SCRATCH",
    0x0B: "VICEGRIP",
    0x0C: "GUILLOTINE",
    0x0D: "RAZOR_WIND",
    0x0E: "SWORDS_DANCE",
    0x0F: "CUT",
    0x10: "GUST",
    0x11: "WING_ATTACK",
    0x12: "WHIRLWIND",
    0x13: "FLY",
    0x14: "BIND",
    0x15: "SLAM",
    0x16: "VINE_WHIP",
    0x17: "STOMP",
    0x18: "DOUBLE_KICK",
    0x19: "MEGA_KICK",
    0x1A: "JUMP_KICK",
    0x1B: "ROLLING_KICK",
    0x1C: "SAND_ATTACK",
    0x1D: "HEADBUTT",
    0x1E: "HORN_ATTACK",
    0x1F: "FURY_ATTACK",
    0x20: "HORN_DRILL",
    0x21: "TACKLE",
    0x22: "BODY_SLAM",
    0x23: "WRAP",
    0x24: "TAKE_DOWN",
    0x25: "THRASH",
    0x26: "DOUBLE_EDGE",
    0x27: "TAIL_WHIP",
    0x28: "POISON_STING",
    0x29: "TWINEEDLE",
    0x2A: "PIN_MISSILE",
    0x2B: "LEER",
    0x2C: "BITE",
    0x2D: "GROWL",
    0x2E: "ROAR",
    0x2F: "SING",
    0x30: "SUPERSONIC",
    0x31: "SONICBOOM",
    0x32: "DISABLE",
    0x33: "ACID",
    0x34: "EMBER",
    0x35: "FLAMETHROWER",
    0x36: "MIST",
    0x37: "WATER_GUN",
    0x38: "HYDRO_PUMP",
    0x39: "SURF",
    0x3A: "ICE_BEAM",
    0x3B: "BLIZZARD",
    0x3C: "PSYBEAM",
    0x3D: "BUBBLEBEAM",
    0x3E: "AURORA_BEAM",
    0x3F: "HYPER_BEAM",
    0x40: "PECK",
    0x41: "DRILL_PECK",
    0x42: "SUBMISSION",
    0x43: "LOW_KICK",
    0x44: "COUNTER",
    0x45: "SEISMIC_TOSS",
    0x46: "STRENGTH",
    0x47: "ABSORB",
    0x48: "MEGA_DRAIN",
    0x49: "LEECH_SEED",
    0x4A: "GROWTH",
    0x4B: "RAZOR_LEAF",
    0x4C: "SOLARBEAM",
    0x4D: "POISONPOWDER",
    0x4E: "STUN_SPORE",
    0x4F: "SLEEP_POWDER",
    0x50: "PETAL_DANCE",
    0x51: "STRING_SHOT",
    0x52: "DRAGON_RAGE",
    0x53: "FIRE_SPIN",
    0x54: "THUNDERSHOCK",
    0x55: "THUNDERBOLT",
    0x56: "THUNDER_WAVE",
    0x57: "THUNDER",
    0x58: "ROCK_THROW",
    0x59: "EARTHQUAKE",
    0x5A: "FISSURE",
    0x5B: "DIG",
    0x5C: "TOXIC",
    0x5D: "CONFUSION",
    0x5E: "PSYCHIC_M",
    0x5F: "HYPNOSIS",
    0x60: "MEDITATE",
    0x61: "AGILITY",
    0x62: "QUICK_ATTACK",
    0x63: "RAGE",
    0x64: "TELEPORT",
    0x65: "NIGHT_SHADE",
    0x66: "MIMIC",
    0x67: "SCREECH",
    0x68: "DOUBLE_TEAM",
    0x69: "RECOVER",
    0x6A: "HARDEN",
    0x6B: "MINIMIZE",
    0x6C: "SMOKESCREEN",
    0x6D: "CONFUSE_RAY",
    0x6E: "WITHDRAW",
    0x6F: "DEFENSE_CURL",
    0x70: "BARRIER",
    0x71: "LIGHT_SCREEN",
    0x72: "HAZE",
    0x73: "REFLECT",
    0x74: "FOCUS_ENERGY",
    0x75: "BIDE",
    0x76: "METRONOME",
    0x77: "MIRROR_MOVE",
    0x78: "SELFDESTRUCT",
    0x79: "EGG_BOMB",
    0x7A: "LICK",
    0x7B: "SMOG",
    0x7C: "SLUDGE",
    0x7D: "BONE_CLUB",
    0x7E: "FIRE_BLAST",
    0x7F: "WATERFALL",
    0x80: "CLAMP",
    0x81: "SWIFT",
    0x82: "SKULL_BASH",
    0x83: "SPIKE_CANNON",
    0x84: "CONSTRICT",
    0x85: "AMNESIA",
    0x86: "KINESIS",
    0x87: "SOFTBOILED",
    0x88: "HI_JUMP_KICK",
    0x89: "GLARE",
    0x8A: "DREAM_EATER",
    0x8B: "POISON_GAS",
    0x8C: "BARRAGE",
    0x8D: "LEECH_LIFE",
    0x8E: "LOVELY_KISS",
    0x8F: "SKY_ATTACK",
    0x90: "TRANSFORM",
    0x91: "BUBBLE",
    0x92: "DIZZY_PUNCH",
    0x93: "SPORE",
    0x94: "FLASH",
    0x95: "PSYWAVE",
    0x96: "SPLASH",
    0x97: "ACID_ARMOR",
    0x98: "CRABHAMMER",
    0x99: "EXPLOSION",
    0x9A: "FURY_SWIPES",
    0x9B: "BONEMERANG",
    0x9C: "REST",
    0x9D: "ROCK_SLIDE",
    0x9E: "HYPER_FANG",
    0x9F: "SHARPEN",
    0xA0: "CONVERSION",
    0xA1: "TRI_ATTACK",
    0xA2: "SUPER_FANG",
    0xA3: "SLASH",
    0xA4: "SUBSTITUTE",
    0xA5: "STRUGGLE",
}
