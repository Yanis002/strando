from enum import IntEnum

shop_actor_ids = [
    "GORY", # Goron Village Shop Keeper
    "YUKY", # Snow Sanctuary Shop Keeper
    "WAWY", # Papuzia Shop Keeper
    "TERY", # Beedle
    "FOMY", # Mayscore Shop Keeper
    "CAMY", # Castle Town Shop Keeper
]

actor_ids = [
    "SZKU", # Tears of Light
    "KEYN", # Freestanding Small Keys
] + shop_actor_ids

mapobj_ids = [
    "TRES",
    "TRED",
    "TREW",
    "TREN",
    "TRWS",
    "TRLN",
    "TRLS",
    "TRLD",
    "TRLW",
    "GELG",
]


class ItemId(IntEnum):
    # special handling
    RupeesShops = -21 # adjustable rupee count
    ProgressiveShield = -20
    DefeatBubble = -19 # bombs or bow or whip or (sword and (boomerang or whirlwind))
    RingBell = -18 # sword or boomerang
    RabbitsAll = -17
    RabbitsAny = -16
    RabbitsGrass = -15
    RabbitsSnow = -14
    RabbitsOcean = -13
    RabbitsMountain = -12
    RabbitsSand = -11
    Repeater = -10 # sword or boomerang or whip
    BoomerangOrBeam = -9
    RangeOrBeam = -8
    Weapons = -7 # sword or bombs or bow or whip
    RangeWeapons = -6 # boomerang or bow
    SmallKeys = -5
    Rupees = -4
    ProgressiveBow = -3
    ProgressiveBombBag = -2
    ProgressiveSword = -1

    Nothing = 0 # 0x00
    NormalShield = 1 # 0x01
    NormalSword = 2 # 0x02
    Whirlwind = 3 # 0x03
    BombBag = 4 # 0x04
    NormalBow = 5 # 0x05
    Boomerang = 6 # 0x06
    Whip = 7 # 0x07
    SandRod = 8 # 0x08
    Unk_9 = 9 # 0x09
    NormalKey = 10 # 0x0A
    BossKey = 11 # 0x0B
    GreenRupee = 12 # 0x0C
    BlueRupee = 13 # 0x0D
    RedRupee = 14 # 0x0E
    BigGreenRupee = 15 # 0x0F
    BigRedRupee = 16 # 0x10
    BigGoldRupee = 17 # 0x11
    ForceGem_18 = 18 # 0x12
    ForceGem_19 = 19 # 0x13
    ForceGem_20 = 20 # 0x14
    ForestGlyph = 21 # 0x15
    SnowGlyph = 22 # 0x16
    OceanGlyph = 23 # 0x17
    FireGlyph = 24 # 0x18
    Unk_25 = 25 # 0x19
    Unk_26 = 26 # 0x1A
    Unk_27 = 27 # 0x1B
    Unk_28 = 28 # 0x1C
    Unk_29 = 29 # 0x1D
    FinalTrack = 30 # 0x1E
    Unk_31 = 31 # 0x1F
    Unk_32 = 32 # 0x20
    Unk_33 = 33 # 0x21
    Unk_34 = 34 # 0x22
    ForceGem_35 = 35 # 0x23
    ForceGem_36 = 36 # 0x24
    ForceGem_37 = 37 # 0x25
    RecruitUniform = 38 # 0x26
    PostmasterLetter = 39 # 0x27
    HeartContainer = 40 # 0x28
    QuiverMedium = 41 # 0x29
    BombBagMedium = 42 # 0x2A
    ForceGem_43 = 43 # 0x2B
    ForceGem_44 = 44 # 0x2C
    ForceGem_45 = 45 # 0x2D
    ForceGem_46 = 46 # 0x2E
    ForceGem_47 = 47 # 0x2F
    ForceGem_48 = 48 # 0x30
    ForceGem_49 = 49 # 0x31
    ForceGem_50 = 50 # 0x32
    ForceGem_51 = 51 # 0x33
    ForceGem_52 = 52 # 0x34
    ForceGem_53 = 53 # 0x35
    ForceGem_54 = 54 # 0x36
    ForceGem_55 = 55 # 0x37
    ForceGem_56 = 56 # 0x38
    ForceGem_57 = 57 # 0x39
    ForceGem_58 = 58 # 0x3A
    ForceGem_59 = 59 # 0x3B
    ForceGem_60 = 60 # 0x3C
    ForceGem_61 = 61 # 0x3D
    PanFlute = 62 # 0x3E
    StampBook = 63 # 0x3F
    LightBow = 64 # 0x40
    LokomoSword = 65 # 0x41
    TenPriceCard = 66 # 0x42
    RedPotion = 67 # 0x43
    PurplePotion = 68 # 0x44
    YellowPotion = 69 # 0x45
    DemonFossil = 70 # 0x46
    StalfosSkull = 71 # 0x47
    StarFragment = 72 # 0x48
    BeeLarvae = 73 # 0x49
    WoodHeart = 74 # 0x4A
    DarkPearlLoop = 75 # 0x4B
    WhitePearlLoop = 76 # 0x4C
    RutoCrown = 77 # 0x4D
    DragonScale = 78 # 0x4E
    PirateNecklace = 79 # 0x4F
    PalaceDish = 80 # 0x50
    GoronAmber = 81 # 0x51
    MysticJade = 82 # 0x52
    AncientCoin = 83 # 0x53
    PricelessStone = 84 # 0x54
    RegalRing = 85 # 0x55
    ArrowsRefill = 86 # 0x56
    BombsRefill = 87 # 0x57
    SoldOutSign = 88 # 0x58
    AncientShield = 89 # 0x59
    QuiverLarge = 90 # 0x5A
    BombBagLarge = 91 # 0x5B
    RandCommonTreasure = 92 # 0x5C
    RandUncommonTreasure = 93 # 0x5D
    RandRareTreasure = 94 # 0x5E
    RandLegendaryTreasure = 95 # 0x5F
    TearLight = 96 # 0x60
    LightCompass = 97 # 0x61
    ScrollSpinAttack = 98 # 0x62
    ScrollBeam = 99 # 0x63
    LinebeckLetter = 100 # 0x64
    PanFluteSong_101 = 101 # 0x65
    PanFluteSong_102 = 102 # 0x66
    PanFluteSong_103 = 103 # 0x67
    PanFluteSong_104 = 104 # 0x68
    PanFluteSong_105 = 105 # 0x69
    RabbitNet = 106 # 0x6A
    BeedleCard = 107 # 0x6B
    SilverCard = 108 # 0x6C
    GoldCard = 109 # 0x6D
    PlatinumCard = 110 # 0x6E
    DiamondCard = 111 # 0x6F
    FreebieCard = 112 # 0x70
    QuintupleCard = 113 # 0x71
    CarbenLetter = 114 # 0x72
    RecruitUniform2 = 115 # 0x73
    EngineerUniform = 116 # 0x74


item_id_to_name = {
    0x00: "Nothing",
    0x01: "Normal Shield",
    0x02: "Normal Sword",
    0x03: "Whirlwind",
    0x04: "Bomb Bag",
    0x05: "Normal Bow",
    0x06: "Boomerang",
    0x07: "Whip",
    0x08: "Sand Rod",
    0x09: "Unk 9",
    0x0A: "Normal Key",
    0x0B: "Boss Key",
    0x0C: "Green Rupee",
    0x0D: "Blue Rupee",
    0x0E: "Red Rupee",
    0x0F: "Big Green Rupee",
    0x10: "Big Red Rupee",
    0x11: "Big Gold Rupee",
    0x12: "Force Gem 18",
    0x13: "Force Gem 19",
    0x14: "Force Gem 20",
    0x15: "Forest Glyph",
    0x16: "Snow Glyph",
    0x17: "Ocean Glyph",
    0x18: "Fire Glyph",
    0x19: "Unk 25",
    0x1A: "Unk 26",
    0x1B: "Unk 27",
    0x1C: "Unk 28",
    0x1D: "Unk 29",
    0x1E: "Final Track",
    0x1F: "Unk 31",
    0x20: "Unk 32",
    0x21: "Unk 33",
    0x22: "Unk 34",
    0x23: "Force Gem 35",
    0x24: "Force Gem 36",
    0x25: "Force Gem 37",
    0x26: "Recruit Uniform",
    0x27: "Postmaster Letter",
    0x28: "Heart Container",
    0x29: "Quiver Medium",
    0x2A: "Bomb Bag Medium",
    0x2B: "Force Gem 43",
    0x2C: "Force Gem 44",
    0x2D: "Force Gem 45",
    0x2E: "Force Gem 46",
    0x2F: "Force Gem 47",
    0x30: "Force Gem 48",
    0x31: "Force Gem 49",
    0x32: "Force Gem 50",
    0x33: "Force Gem 51",
    0x34: "Force Gem 52",
    0x35: "Force Gem 53",
    0x36: "Force Gem 54",
    0x37: "Force Gem 55",
    0x38: "Force Gem 56",
    0x39: "Force Gem 57",
    0x3A: "Force Gem 58",
    0x3B: "Force Gem 59",
    0x3C: "Force Gem 60",
    0x3D: "Force Gem 61",
    0x3E: "Pan Flute",
    0x3F: "Stamp Book",
    0x40: "Light Bow",
    0x41: "Lokomo Sword",
    0x42: "Ten Price Card",
    0x43: "Red Potion",
    0x44: "Purple Potion",
    0x45: "Yellow Potion",
    0x46: "Demon Fossil",
    0x47: "Stalfos Skull",
    0x48: "Star Fragment",
    0x49: "Bee Larvae",
    0x4A: "Wood Heart",
    0x4B: "Dark Pearl Loop",
    0x4C: "White Pearl Loop",
    0x4D: "Ruto Crown",
    0x4E: "Dragon Scale",
    0x4F: "Pirate Necklace",
    0x50: "Palace Dish",
    0x51: "Goron Amber",
    0x52: "Mystic Jade",
    0x53: "Ancient Coin",
    0x54: "Priceless Stone",
    0x55: "Regal Ring",
    0x56: "Arrows Refill",
    0x57: "Bombs Refill",
    0x58: "Sold Out Sign",
    0x59: "Ancient Shield",
    0x5A: "Quiver Large",
    0x5B: "Bomb Bag Large",
    0x5C: "Rand Common Treasure",
    0x5D: "Rand Uncommon Treasure",
    0x5E: "Rand Rare Treasure",
    0x5F: "Rand Legendary Treasure",
    0x60: "Tear Light",
    0x61: "Light Compass",
    0x62: "Scroll Spin Attack",
    0x63: "Scroll Beam",
    0x64: "Linebeck Letter",
    0x65: "PanFlute Song 101",
    0x66: "PanFlute Song 102",
    0x67: "PanFlute Song 103",
    0x68: "PanFlute Song 104",
    0x69: "PanFlute Song 105",
    0x6A: "Rabbit Net",
    0x6B: "Beedle Card",
    0x6C: "Silver Card",
    0x6D: "Gold Card",
    0x6E: "Platinum Card",
    0x6F: "Diamond Card",
    0x70: "Freebie Card",
    0x71: "Quintuple Card",
    0x72: "Carben Letter",
    0x73: "Recruit Uniform 2",
    0x74: "Engineer Uniform",
}

class ItemKind(IntEnum):
    Default = 0
    Shop = 1
    Song = 2


class ItemWeight(IntEnum):
    Progressive = 0
    Priority = 1
    Normal = 2


class SceneId(IntEnum):
    test_trn = 0x00 #
    test_trn2 = 0x01 #
    test_pre = 0x02 #
    test_iwa = 0x03 #
    t_area0 = 0x04 # Forest Realm
    t_area1 = 0x05 # Snow Realm
    t_area2 = 0x06 # Ocean Realm
    t_area3 = 0x07 # Fire Realm
    t_tutorial = 0x08 #
    t_forest = 0x09 #
    t_smarine = 0x0A #
    t_smount = 0x0B # rocktite scene?
    t_smount2 = 0x0C # rocktite scene?
    t_smount3 = 0x0D # rocktite fire realm scene?
    t_minigame = 0x0E # goron target range minigame
    t_dark = 0x0F # Dark Realm
    t_eviltrain = 0x10 # train cole fight
    t_eviltrain2 = 0x11 # same as above
    t_eviltrain3 = 0x12 # same as above
    d_main = 0x13 # Tower Of Spirits
    d_main_f = 0x14 # ToS base
    d_main_s = 0x15 # ToS top stairs
    d_main_a = 0x16 # ToS altar
    d_main_w = 0x17 # ToS inner Stairs
    d_tutorial = 0x18 # Tunnel to ToS
    d_forest = 0x19 # Forest Temple
    d_snow26 = 0x1A # Snow Temple
    d_water27 = 0x1B # Water Temple
    d_flame = 0x1C # Fire Temple
    d_sand = 0x1D # Sand Temple
    b_forest = 0x1E # Stagnox
    b_snow = 0x1F # Fraaz
    b_water = 0x20 # Phytops
    b_flame = 0x21 # Cragma
    b_sand = 0x22 # Skeldritch
    b_deago = 0x23 # Byrne
    b_last1 = 0x24 # demon zelda train
    b_last2 = 0x25 # malladus beast 1
    b_last22 = 0x26 # malladus song
    b_last23 = 0x27 # mallasdus beast 2
    f_hyral = 0x28 # hyrule castle
    f_htown = 0x29 # castle town
    f_forest1 = 0x2A # Whittleton
    f_snow = 0x2B # Anouki Village
    f_water = 0x2C # Papuchia Village
    f_flame = 0x2D # Goron Village
    f_flame5 = 0x2E # ,
    f_first = 0x2F # Aboda Village
    f_forest2 = 0x30 # Forest Sanctuary
    f_snow2 = 0x31 # Snow Sanctuary
    f_water2 = 0x32 # Water Sanctuary
    f_flame2 = 0x33 # Fire Sanctuary
    f_sand = 0x34 # Sand Sanctuary
    f_tetsuo = 0x35 # Icy Spring
    f_bridge = 0x36 # Bridge Worker's House
    f_bridge2 = 0x37 # Trading Post
    f_forest3 = 0x38 # whittleton forest
    f_water3 = 0x39 # papuchia south
    f_ajito = 0x3A # Pirate Hideout
    f_ajito2 = 0x3B # same as above
    f_flame3 = 0x3C # Goron Target Range
    f_flame4 = 0x3D # Dark Ore Mine
    f_rabbit = 0x3E # Rabbit Haven
    f_kakushi1 = 0x3F # Snowdrift Station
    f_kakushi2 = 0x40 # Disorientation Station
    f_kakushi3 = 0x41 # Ends of the Earth Station
    f_kakushi4 = 0x42 # train required?
    f_pirate = 0x43 # Train passenger pirate attack (including Carben)
    f_passenger = 0x44 # Anjean force gem
    f_trnnpc = 0x45 # Ferrus encounter
    tekiya00 = 0x46 # take em all on
    tekiya01 = 0x47 # take em all on
    tekiya02 = 0x48 # take em all on
    tekiya03 = 0x49 # take em all on
    tekiya04 = 0x4A # take em all on
    tekiya05 = 0x4B # take em all on
    tekiya06 = 0x4C # take em all on
    tekiya07 = 0x4D # take em all on
    tekiya08 = 0x4E # take em all on
    tekiya09 = 0x4F # take em all on
    demo_train = 0x50 # overworld cutscenes (including the title screen)
    e3_train = 0x51 # ?
    e3_dungeon = 0x52 # ?
    e3_boss = 0x53 # forest temple boss
    e3_bossm = 0x54 # fake forest temple room
    e3_smount = 0x55 # ?
    test_hiratsu = 0x56 # ?
    test_sik = 0x57 # ?
    test_fuj = 0x58 # ?
    test_nit = 0x59 # ?
    test_mri = 0x5A # ?
    test_morita = 0x5B # ?
    test_yamaz = 0x5C # ?
    test_sako = 0x5D # ?
    test_kita = 0x5E # ?
    test_take = 0x5F # ?
    test_suzuki = 0x60 # ?
    test_okane = 0x61 # ?
    test_dera = 0x62 # ?
    test_hosaka = 0x63 # ?
    test_hosaka_f = 0x64 # ?
    test_kato = 0x65 # ?
    test_okane_f = 0x66 # ?
    test_yamaz_f = 0x67 # ?
    test_sako_f = 0x68 # ?
    test_take_f = 0x69 # ?
    test_kiuchi = 0x6A # ?
    test_dera_f = 0x6B # ?
    test_slope = 0x6C # ?
    battle01 = 0x6D # battle mode?
    battle02 = 0x6E # battle mode?
    battle03 = 0x6F # battle mode?
    battle04 = 0x70 # battle mode?
    battle05 = 0x71 # battle mode?
    battle06 = 0x72 # battle mode?
    battle07 = 0x73 # battle mode?
    battle08 = 0x74 # battle mode?
    battle09 = 0x75 # battle mode?
    battle10 = 0x76 # battle mode?
    battle11 = 0x77 # battle mode?
    battle12 = 0x78 # battle mode?


class AdventureFlag(IntEnum):
    Unk_000 = 0x000 # FLAG(0, 0)
    Unk_001 = 0x001 # FLAG(0, 1)
    ObtainedSpiritTrain = 0x002 # FLAG(0, 2)
    ObtainedRecruitSword = 0x003 # FLAG(0, 3)
    ObtainedForestSource = 0x004 # FLAG(0, 4)
    ObtainedSnowSource = 0x005 # FLAG(0, 5)
    ObtainedOceanSource = 0x006 # FLAG(0, 6)
    ObtainedFireSource = 0x007 # FLAG(0, 7)
    CompletedForestRestorationSong = 0x008 # FLAG(0, 8)
    CompletedOceanRestorationSong = 0x009 # FLAG(0, 9)
    CompletedSnowRestorationSong = 0x00A # FLAG(0, 10)
    CompletedFireRestorationSong = 0x00B # FLAG(0, 11)
    CompletedSandRestorationSong = 0x00C # FLAG(0, 12)
    OpenedDarkRealmPortal = 0x00D # FLAG(0, 13)
    TalkedToDovokLostWoods = 0x00E # FLAG(0, 14)
    ObtainedForestGlyph = 0x00F # FLAG(0, 15)
    ObtainedSnowGlyph = 0x010 # FLAG(0, 16)
    ObtainedOceanGlyph = 0x011 # FLAG(0, 17)
    ObtainedFireGlyph = 0x012 # FLAG(0, 18)
    Unk_013 = 0x013 # FLAG(0, 19)
    CompletedSwordTutorial = 0x014 # FLAG(0, 20)
    PlayedHyruleGuardGetLostText = 0x015 # FLAG(0, 21)
    HyruleGuardMovesAfterCole = 0x016 # FLAG(0, 22)
    WatchedHyruleGuardColeCS = 0x017 # FLAG(0, 23)
    ObtainedEngineerCertificate = 0x018 # FLAG(0, 24)
    WatchedZeldasBedroomFirstCS = 0x019 # FLAG(0, 25)
    WatchedSpiritTowerSplitCS = 0x01A # FLAG(0, 26)
    MayscoreLostWoodsHintBranches = 0x01B # FLAG(0, 27)
    MayscoreLostWoodsHint4thTree = 0x01C # FLAG(0, 28)
    TalkedToYamahikoFirstTime = 0x01D # FLAG(0, 29)
    EnteredForestTemple = 0x01E # FLAG(0, 30)
    ObtainedTrainCannon = 0x01F # FLAG(0, 31)
    Unk_020 = 0x020 # FLAG(1, 0)
    ObtainedTrainWagon = 0x021 # FLAG(1, 1)
    MetAnjeanFirstTime = 0x022 # FLAG(1, 2)
    Unk_023 = 0x023 # FLAG(1, 3)
    FleeFirstPhantomTOS = 0x024 # FLAG(1, 4)
    SpawnFirstPhantomTOS = 0x025 # FLAG(1, 5)
    Unk_026 = 0x026 # FLAG(1, 6)
    Unk_027 = 0x027 # FLAG(1, 7)
    SummonKeyMastersOnceForestTemple = 0x028 # FLAG(1, 8)
    SummonKeyMastersTwiceForestTemple = 0x029 # FLAG(1, 9)
    InteractedWithForestTempleBossKeyMap = 0x02A # FLAG(1, 10)
    Unk_02B = 0x02B # FLAG(1, 11)
    BossKeyTextForestTemple = 0x02C # FLAG(1, 12)
    RouteDrawTutorial = 0x02D # FLAG(1, 13)
    EnteredLostWoodsFirstTime = 0x02E # FLAG(1, 14)
    WrongPathLostWoodsPostHints = 0x02F # FLAG(1, 15)
    Unk_030 = 0x030 # FLAG(1, 16)
    Unk_031 = 0x031 # FLAG(1, 17)
    WatchedHyruleCastleSpiritZeldaCS = 0x032 # FLAG(1, 18)
    EscortedZeldaToCastleTown = 0x033 # FLAG(1, 19)
    ObtainedSpiritPipes = 0x034 # FLAG(1, 20)
    OutsetVillageBoardTrainFirstTime = 0x035 # FLAG(1, 21)
    TalkedToHyruleCastleBackExitGuardNoSword = 0x036 # FLAG(1, 22)
    WatchedThroneRoomSpiritZeldaCS = 0x037 # FLAG(1, 23)
    MetPostmanFirstLetter = 0x038 # FLAG(1, 24)
    ReceivedZeldasLetter = 0x039 # FLAG(1, 25)
    ReceivedAlfonzosLetter = 0x03A # FLAG(1, 26)
    ReceivedRussellsLetter = 0x03B # FLAG(1, 27)
    ObtainedLinebecksLetter = 0x03C # FLAG(1, 28)
    ReceivedBeedlesFirstLetter = 0x03D # FLAG(1, 29)
    Unk_03E = 0x03E # FLAG(1, 30)
    Unk_03F = 0x03F # FLAG(1, 31)
    Unk_040 = 0x040 # FLAG(2, 0)
    Unk_041 = 0x041 # FLAG(2, 1)
    Unk_042 = 0x042 # FLAG(2, 2)
    Unk_043 = 0x043 # FLAG(2, 3)
    Unk_044 = 0x044 # FLAG(2, 4)
    Unk_045 = 0x045 # FLAG(2, 5)
    ReceivedCarbensLetter = 0x046 # FLAG(2, 6)
    ReceivedNikosLetter = 0x047 # FLAG(2, 7)
    ReceivedFerrusLetter1 = 0x048 # FLAG(2, 8)
    ReceivedFerrusLetter2 = 0x049 # FLAG(2, 9)
    ReceivedFerrusLetter3 = 0x04A # FLAG(2, 10)
    ReceivedKagoronsLetter = 0x04B # FLAG(2, 11)
    CarbenBoardsTrain = 0x04C # FLAG(2, 12)
    CarbenEnterSanctuary = 0x04D # FLAG(2, 13)
    OpenedMarineTemplePath = 0x04E # FLAG(2, 14)
    WonCarbenPirateAmbush = 0x04F # FLAG(2, 15)
    EnteredMarineTemple = 0x050 # FLAG(2, 16)
    TalkedToFerrusOceanRealm = 0x051 # FLAG(2, 17)
    EnteredOceanFloorFirstTime = 0x052 # FLAG(2, 18)
    MetWiseOne = 0x053 # FLAG(2, 19)
    VisitedPapuziaFirstTime = 0x054 # FLAG(2, 20)
    SawCarbenWithBirdsPapuzia = 0x055 # FLAG(2, 21)
    IslandSanctuaryFirstTime = 0x056 # FLAG(2, 22)
    ReadCarbensSignInSanctuary = 0x057 # FLAG(2, 23)
    TalkedToCarbenPapuzia = 0x058 # FLAG(2, 24)
    AnoukiPuzzleStart = 0x059 # FLAG(2, 25)
    Unk_05A = 0x05A # FLAG(2, 26)
    FerrusBlizzardTempleHint = 0x05B # FLAG(2, 27)
    AnoukiPuzzleComplete = 0x05C # FLAG(2, 28)
    Unk_05D = 0x05D # FLAG(2, 29)
    Unk_05E = 0x05E # FLAG(2, 30)
    ReadMapInFerrusHouse = 0x05F # FLAG(2, 31)
    Unk_060 = 0x060 # FLAG(3, 0)
    EnteredBlizzardTemple = 0x061 # FLAG(3, 1)
    BeatSnowRealmRocktite = 0x062 # FLAG(3, 2)
    AnoukiHonchoBlizzardAdvice = 0x063 # FLAG(3, 3)
    BoughtMegaIceFromNoko = 0x064 # FLAG(3, 4)
    TalkedToLinebeckRegalRingPreKenzo = 0x065 # FLAG(3, 5)
    MetBridgeWorkerFirstTime = 0x066 # FLAG(3, 6)
    MetLinebeckFirstTime = 0x067 # FLAG(3, 7)
    ObtainedLuciaForceGem = 0x068 # FLAG(3, 8)
    ObtainedOrcaForceGem = 0x069 # FLAG(3, 9)
    ObtainedCarbenForceGem = 0x06A # FLAG(3, 10)
    ObtainedRaelForceGem = 0x06B # FLAG(3, 11)
    ObtainedJoeForceGem = 0x06C # FLAG(3, 12)
    ObtainedMonaForceGem = 0x06D # FLAG(3, 13)
    ObtainedHarryForceGem = 0x06E # FLAG(3, 14)
    ObtainedMashForceGem = 0x06F # FLAG(3, 15)
    ObtainedFerrusForceGem1 = 0x070 # FLAG(3, 16)
    ObtainedYekoForceGem = 0x071 # FLAG(3, 17)
    ObtainedNokoForceGem = 0x072 # FLAG(3, 18)
    ObtainedGoronAdultAnoukiForceGem = 0x073 # FLAG(3, 19)
    ObtainedSteemForceGem = 0x074 # FLAG(3, 20)
    ObtainedLinebeckForceGem = 0x075 # FLAG(3, 21)
    ObtainedWadatsumiForceGem = 0x076 # FLAG(3, 22)
    ObtainedNiboshiForceGem = 0x077 # FLAG(3, 23)
    ObtainedGoronAdultMegaIceForceGem = 0x078 # FLAG(3, 24)
    ObtainedFerrusForceGem2 = 0x079 # FLAG(3, 25)
    ObtainedKofuForceGem = 0x07A # FLAG(3, 26)
    ObtainedChildGoronForceGem = 0x07B # FLAG(3, 27)
    WatchedWarpPhantomFirstTimeWarpingCS = 0x07C # FLAG(3, 28)
    FailedFirstTrainRide = 0x07D # FLAG(3, 29)
    TextPhantomInLava = 0x07E # FLAG(3, 30)
    TextTOSEntrance4F = 0x07F # FLAG(3, 31)
    Unk_080 = 0x080 # FLAG(4, 0)
    Unk_081 = 0x081 # FLAG(4, 1)
    Unk_082 = 0x082 # FLAG(4, 2)
    Unk_083 = 0x083 # FLAG(4, 3)
    TalkedToWoodAboutWhipMinigame = 0x084 # FLAG(4, 4)
    BeatRecordFirstTimeWhipMinigame = 0x085 # FLAG(4, 5)
    BeatRecordFirstTimeWhipMinigameText = 0x086 # FLAG(4, 6)
    Unk_087 = 0x087 # FLAG(4, 7)
    Unk_088 = 0x088 # FLAG(4, 8)
    DefeatSpinutsAroundHyruleCastleGuard = 0x089 # FLAG(4, 9)
    TeacherPanicHyruleCastle = 0x08A # FLAG(4, 10)
    HitBeehiveOutsetVillage = 0x08B # FLAG(4, 11)
    JoeRunsOffAfterHittingBeehive = 0x08C # FLAG(4, 12)
    TalkedToAlfonzoHyruleCastle = 0x08D # FLAG(4, 13)
    AlfonzoBoardsTrainToOutsetVillage = 0x08E # FLAG(4, 14)
    Unk_08F = 0x08F # FLAG(4, 15)
    WatchedIntroCS = 0x090 # FLAG(4, 16)
    WatchedFirstPhantomPossessionCS = 0x091 # FLAG(4, 17)
    WatchedForestTempleCompletedCS = 0x092 # FLAG(4, 18)
    TalkedToZeldaMayscoreFirstTime = 0x093 # FLAG(4, 19)
    TalkedToZeldaPhantomPossessionFirstTime = 0x094 # FLAG(4, 20)
    Unk_095 = 0x095 # FLAG(4, 21)
    TalkedToPhantomWithZeldaTOS2F = 0x096 # FLAG(4, 22)
    Unk_097 = 0x097 # FLAG(4, 23)
    Unk_098 = 0x098 # FLAG(4, 24)
    Unk_099 = 0x099 # FLAG(4, 25)
    Unk_09A = 0x09A # FLAG(4, 26)
    WhipMinigameTutorial = 0x09B # FLAG(4, 27)
    Unk_09C = 0x09C # FLAG(4, 28)
    Unk_09D = 0x09D # FLAG(4, 29)
    Unk_09E = 0x09E # FLAG(4, 30)
    Unk_09F = 0x09F # FLAG(4, 31)
    Unk_0A0 = 0x0A0 # FLAG(5, 0)
    Unk_0A1 = 0x0A1 # FLAG(5, 1)
    TalkedPapuziaNagi = 0x0A2 # FLAG(5, 2)
    TalkedPapuziaNigoshi = 0x0A3 # FLAG(5, 3)
    TalkedPapuziaOrca = 0x0A4 # FLAG(5, 4)
    TalkedPapuziaFuku = 0x0A5 # FLAG(5, 5)
    ObtainedAnjeanDesertForceGem = 0x0A6 # FLAG(5, 6)
    Unk_0A7 = 0x0A7 # FLAG(5, 7)
    Unk_0A8 = 0x0A8 # FLAG(5, 8)
    Unk_0A9 = 0x0A9 # FLAG(5, 9)
    Unk_0AA = 0x0AA # FLAG(5, 10)
    TextForestTempleBossKeyDoor = 0x0AB # FLAG(5, 11)
    TalkedAnjeanAfterFirstPhantom = 0x0AC # FLAG(5, 12)
    HitByFirstPhantomInsteadOfFleeing = 0x0AD # FLAG(5, 13)
    ReenterTOS1FAfterFleeing = 0x0AE # FLAG(5, 14)
    Unk_0AF = 0x0AF # FLAG(5, 15)
    ObtainedBowOfLight = 0x0B0 # FLAG(5, 16)
    Unk_0B1 = 0x0B1 # FLAG(5, 17)
    Unk_0B2 = 0x0B2 # FLAG(5, 18)
    ForestSongPracticeReady = 0x0B3 # FLAG(5, 19)
    ForestSongPracticeDone = 0x0B4 # FLAG(5, 20)
    ForestSnowSandSongsFailedOnce = 0x0B5 # FLAG(5, 21)
    Unk_0B6 = 0x0B6 # FLAG(5, 22)
    WatchedBlizzardTempleCompletedCS = 0x0B7 # FLAG(5, 23)
    WatchedMarineTempleCompletedCS = 0x0B8 # FLAG(5, 24)
    MetStavenInTOSAfterFireGlyphCS = 0x0B9 # FLAG(5, 25)
    Unk_0BA = 0x0BA # FLAG(5, 26)
    ForestTracksRestoredFromGlyphCS = 0x0BB # FLAG(5, 27)
    OpenedOceanRealm = 0x0BC # FLAG(5, 28)
    TalkedToAnjeanAfterGlyph = 0x0BD # FLAG(5, 29)
    TalkedToAnjeanAfterTemple = 0x0BE # FLAG(5, 30)
    PlayRussellSwordTrainingMinigame = 0x0BF # FLAG(5, 31)
    HyruleCastleZeldaControlsTutorial = 0x0C0 # FLAG(6, 0)
    WatchedZeldaSpiritThroneCS = 0x0C1 # FLAG(6, 1)
    WatchedEnterZeldasBedroomCS = 0x0C2 # FLAG(6, 2)
    MetKagoronFirstTime = 0x0C3 # FLAG(6, 3)
    ZeldaTextAfterAnoukiPuzzleStart = 0x0C4 # FLAG(6, 4)
    KenzoBoardsTrainToFixBridge = 0x0C5 # FLAG(6, 5)
    GotKenzoToTradingPost = 0x0C6 # FLAG(6, 6)
    LinebeckTalksToKenzoAboutPayment = 0x0C7 # FLAG(6, 7)
    MetSteemFirstTime = 0x0C8 # FLAG(6, 8)
    SnowSongPracticeDone = 0x0C9 # FLAG(6, 9)
    Unk_0CA = 0x0CA # FLAG(6, 10)
    ObtainedSandWand = 0x0CB # FLAG(6, 11)
    DefeatedRocktiteInDesertCave = 0x0CC # FLAG(6, 12)
    MetRaelFirstTime = 0x0CD # FLAG(6, 13)
    SandSongPraticeDone = 0x0CE # FLAG(6, 14)
    Unk_0CF = 0x0CF # FLAG(6, 15)
    ObtainedDesertSource = 0x0D0 # FLAG(6, 16)
    FerrusPassengerTutorial = 0x0D1 # FLAG(6, 17)
    TextRockNearRabbitland = 0x0D2 # FLAG(6, 18)
    TextZeldaRequireCannon = 0x0D3 # FLAG(6, 19)
    CannonTutorial = 0x0D4 # FLAG(6, 20)
    Unk_0D5 = 0x0D5 # FLAG(6, 21)
    ObtainedRabbitNet = 0x0D6 # FLAG(6, 22)
    Unk_0D7 = 0x0D7 # FLAG(6, 23)
    FailedKenzoTrainRideToTradingPost = 0x0D8 # FLAG(6, 24)
    WatchedOutsetTrainGarageCS = 0x0D9 # FLAG(6, 25)
    MetCarbenFirstTime = 0x0DA # FLAG(6, 26)
    OceanSongPracticeDone = 0x0DB # FLAG(6, 27)
    OceanSongFailedOnce = 0x0DC # FLAG(6, 28)
    ZeldaTextTOS8F = 0x0DD # FLAG(6, 29)
    ZeldaTextTOS13F = 0x0DE # FLAG(6, 30)
    ZeldaTextTorchPhantomTOS9F = 0x0DF # FLAG(6, 31)
    ZeldaTextKeyMastersTOS10F = 0x0E0 # FLAG(7, 0)
    Unk_0E1 = 0x0E1 # FLAG(7, 1)
    TorchPhantomPossession = 0x0E2 # FLAG(7, 2)
    Unk_0E3 = 0x0E3 # FLAG(7, 3)
    Unk_0E4 = 0x0E4 # FLAG(7, 4)
    ZeldaTextDefeatedGeozardChiefTOS11F = 0x0E5 # FLAG(7, 5)
    Unk_0E6 = 0x0E6 # FLAG(7, 6)
    Unk_0E7 = 0x0E7 # FLAG(7, 7)
    Unk_0E8 = 0x0E8 # FLAG(7, 8)
    PlayGoronTargetRangeMinigame = 0x0E9 # FLAG(7, 9)
    WarpPhantomPossession = 0x0EA # FLAG(7, 10)
    Unk_0EB = 0x0EB # FLAG(7, 11)
    ZeldaTextTorchPhantomPossession = 0x0EC # FLAG(7, 12)
    ZeldaTextWarpPhantomPossession = 0x0ED # FLAG(7, 13)
    ZeldaTextWreckerPhantomPossession = 0x0EE # FLAG(7, 14)
    WreckerPhantomPossession = 0x0EF # FLAG(7, 15)
    Unk_0F0 = 0x0F0 # FLAG(7, 16)
    Unk_0F1 = 0x0F1 # FLAG(7, 17)
    Unk_0F2 = 0x0F2 # FLAG(7, 18)
    Unk_0F3 = 0x0F3 # FLAG(7, 19)
    Unk_0F4 = 0x0F4 # FLAG(7, 20)
    Unk_0F5 = 0x0F5 # FLAG(7, 21)
    TalkedFerrusOceanTwice = 0x0F6 # FLAG(7, 22)
    MetEmbroseFirstTime = 0x0F7 # FLAG(7, 23)
    FireSongPracticeDone = 0x0F8 # FLAG(7, 24)
    FireSongFailedOnce = 0x0F9 # FLAG(7, 25)
    ObtainedThreeKeysToMountainTemple = 0x0FA # FLAG(7, 26)
    TalkedToGoronAdultNearStationFirstTime = 0x0FB # FLAG(7, 27)
    GoronAdultTextAfterObtainingWagon = 0x0FC # FLAG(7, 28)
    Unk_0FD = 0x0FD # FLAG(7, 29)
    Unk_0FE = 0x0FE # FLAG(7, 30)
    GiveMegaIceToKagoron = 0x0FF # FLAG(7, 31)
    WatchedStavenPostBattleCS = 0x100 # FLAG(8, 0)
    TalkedToGoronElderAfterFireSong = 0x101 # FLAG(8, 1)
    WatchedMalladusOnTOSSummitCS = 0x102 # FLAG(8, 2)
    Unk_103 = 0x103 # FLAG(8, 3)
    WatchedMountainTempleCompletedCS = 0x104 # FLAG(8, 4)
    MegaIceToGoronVillageMainQuest = 0x105 # FLAG(8, 5)
    Unk_106 = 0x106 # FLAG(8, 6)
    Unk_107 = 0x107 # FLAG(8, 7)
    Unk_108 = 0x108 # FLAG(8, 8)
    MetGoronElderFirstTime = 0x109 # FLAG(8, 9)
    TalkedToGoronElderAfterMountainTemple = 0x10A # FLAG(8, 10)
    ReturnedToGoronAdultAfterMeetingKagoron = 0x10B # FLAG(8, 11)
    KagoronTextAfterGivingMegaIce = 0x10C # FLAG(8, 12)
    OpenedLargeDoorsTOS23F = 0x10D # FLAG(8, 13)
    Unk_10E = 0x10E # FLAG(8, 14)
    Unk_10F = 0x10F # FLAG(8, 15)
    Unk_110 = 0x110 # FLAG(8, 16)
    BoughtBombBagFromBeedle = 0x111 # FLAG(8, 17)
    WatchedFireLandVolcanoEruptionCS = 0x112 # FLAG(8, 18)
    PurchasedLumberFirstTime = 0x113 # FLAG(8, 19)
    PurchasedFishFirstTime = 0x114 # FLAG(8, 20)
    PurchasedVesselFirstTime = 0x115 # FLAG(8, 21)
    Unk_116 = 0x116 # FLAG(8, 22)
    Unk_117 = 0x117 # FLAG(8, 23)
    Unk_118 = 0x118 # FLAG(8, 24)
    Unk_119 = 0x119 # FLAG(8, 25)
    Unk_11A = 0x11A # FLAG(8, 26)
    Unk_11B = 0x11B # FLAG(8, 27)
    Unk_11C = 0x11C # FLAG(8, 28)
    Unk_11D = 0x11D # FLAG(8, 29)
    Unk_11E = 0x11E # FLAG(8, 30)
    ZeldaTextVisitPirateHideoutFirstTime = 0x11F # FLAG(8, 31)
    Unk_120 = 0x120 # FLAG(9, 0)
    WadatsumiBoardsTrain2 = 0x121 # FLAG(9, 1)
    PurchasedCuccosFirstTime = 0x122 # FLAG(9, 2)
    HyruleGuardsOutsideEntranceMoveAside = 0x123 # FLAG(9, 3)
    LinebeckTextAfterKenzoTakesRegalRing = 0x124 # FLAG(9, 4)
    TalkedToJoeAfterHeRanFromBees = 0x125 # FLAG(9, 5)
    ObtainedRussellHeartContainer = 0x126 # FLAG(9, 6)
    Unk_127 = 0x127 # FLAG(9, 7)
    Unk_128 = 0x128 # FLAG(9, 8)
    ObtainedStampBook = 0x129 # FLAG(9, 9)
    ObtainedAncientShield = 0x12A # FLAG(9, 10)
    ObtainedEngineersClothes = 0x12B # FLAG(9, 11)
    ObtainedSwordsmansScroll2 = 0x12C # FLAG(9, 12)
    ObtainedCompassOfLight = 0x12D # FLAG(9, 13)
    ZeldaTextAfterCompassOfLight = 0x12E # FLAG(9, 14)
    WatchedLokomoSwordCS = 0x12F # FLAG(9, 15)
    ObtainedWoodBombBag = 0x130 # FLAG(9, 16)
    ObtainedWoodHeartContainer = 0x131 # FLAG(9, 17)
    WatchedEndTOS1SwordFadeCS = 0x132 # FLAG(9, 18)
    ZeldaTextEndTOS1 = 0x133 # FLAG(9, 19)
    WatchedEndTOS3SwordFadeCS = 0x134 # FLAG(9, 20)
    ZeldaTextEndTOS3 = 0x135 # FLAG(9, 21)
    StateTorch1TOS8F = 0x136 # FLAG(9, 22)
    StateTorch2TOS8F = 0x137 # FLAG(9, 23)
    StateTorch3TOS8F = 0x138 # FLAG(9, 24)
    StateTorch4TOS8F = 0x139 # FLAG(9, 25)
    StateTorch5TOS8F = 0x13A # FLAG(9, 26)
    StateTorch6TOS8F = 0x13B # FLAG(9, 27)
    StateTorch1TOS9F = 0x13C # FLAG(9, 28)
    StateTorch2TOS9F = 0x13D # FLAG(9, 29)
    StateTorch3TOS9F = 0x13E # FLAG(9, 30)
    StateTorch4TOS9F = 0x13F # FLAG(9, 31)
    StateTorch5TOS9F = 0x140 # FLAG(10, 0)
    StateTorch6TOS9F = 0x141 # FLAG(10, 1)
    StateTorch7TOS9F = 0x142 # FLAG(10, 2)
    StateTorch8TOS9F = 0x143 # FLAG(10, 3)
    StateTorch9TOS9F = 0x144 # FLAG(10, 4)
    StateTorch10TOS9F = 0x145 # FLAG(10, 5)
    StateTorch11TOS9F = 0x146 # FLAG(10, 6)
    StateTorch12TOS9F = 0x147 # FLAG(10, 7)
    StateTorch13TOS9F = 0x148 # FLAG(10, 8)
    Unk_149 = 0x149 # FLAG(10, 9)
    StateBlueDoorTOS9F = 0x14A # FLAG(10, 10)
    StateBlueDoorTOS10F = 0x14B # FLAG(10, 11)
    DefeatedGeozardChiefTOS11F = 0x14C # FLAG(10, 12)
    StateRoomLightTOS10F = 0x14D # FLAG(10, 13)
    StateWestBlueDoorTOS13F = 0x14E # FLAG(10, 14)
    ZeldaTextGeozardTOS6F = 0x14F # FLAG(10, 15)
    ZeldaTextDefeatedTOS6F = 0x150 # FLAG(10, 16)
    ZeldaTextPhantomSpawnTOS30F = 0x151 # FLAG(10, 17)
    Unk_152 = 0x152 # FLAG(10, 18)
    Unk_153 = 0x153 # FLAG(10, 19)
    Unk_154 = 0x154 # FLAG(10, 20)
    PlayGoronTargetRangeExtendedTrack = 0x155 # FLAG(10, 21)
    Unk_156 = 0x156 # FLAG(10, 22)
    Unk_157 = 0x157 # FLAG(10, 23)
    Unk_158 = 0x158 # FLAG(10, 24)
    Unk_159 = 0x159 # FLAG(10, 25)
    GaveMegaIceToGoronAdultSidequest = 0x15A # FLAG(10, 26)
    Unk_15B = 0x15B # FLAG(10, 27)
    StateBlueDoorTOS15F = 0x15C # FLAG(10, 28)
    StateBridgeTOS13F = 0x15D # FLAG(10, 29)
    StateTorchTOS13F = 0x15E # FLAG(10, 30)
    StateExistenceSWKeyChestTOS13F = 0x15F # FLAG(10, 31)
    StateBlueDoorCenterTOS14F = 0x160 # FLAG(11, 0)
    StateSWSandBridgeTOS14F = 0x161 # FLAG(11, 1)
    StateSEBlueDoorTOS14F = 0x162 # FLAG(11, 2)
    ActivatedSWSandBridgeTOS14F = 0x163 # FLAG(11, 3)
    StateBlueDoorTOS16F = 0x164 # FLAG(11, 4)
    StateWestBlueDoorTOS20F = 0x165 # FLAG(11, 5)
    StateNWBlueDoorTOS20F = 0x166 # FLAG(11, 6)
    StateFlamesTOS22F = 0x167 # FLAG(11, 7)
    PressedNWSwitchTOS18F = 0x168 # FLAG(11, 8)
    StateSpikesTOS18F = 0x169 # FLAG(11, 9)
    HitEyeSwitchCenterTOS19F = 0x16A # FLAG(11, 10)
    Unk_16B = 0x16B # FLAG(11, 11)
    StateSEBridgeTOS19F = 0x16C # FLAG(11, 12)
    WatchedCameraPanCSToNWBlueDoorTOS20F = 0x16D # FLAG(11, 13)
    DefeatedEnemiesTOS21F = 0x16E # FLAG(11, 14)
    StateFarWestBlueDoorTOS29F = 0x16F # FLAG(11, 15)
    StateRightTorchTOS29F = 0x170 # FLAG(11, 16)
    StateLeftTorchTOS29F = 0x171 # FLAG(11, 17)
    SpawnedSWLargeChestsTOS28F = 0x172 # FLAG(11, 18)
    StateNWLeftTorchTOS28F = 0x173 # FLAG(11, 19)
    StateNWRightTorchTOS28F = 0x174 # FLAG(11, 20)
    Unk_175 = 0x175 # FLAG(11, 21)
    StateEastSpikesTOS30F = 0x176 # FLAG(11, 22)
    StateFarNEBlueDoorTOS30F = 0x177 # FLAG(11, 23)
    WatchedEndTOS2SwordFadeCS = 0x178 # FLAG(11, 24)
    StateNEBlueDoorTOS29F = 0x179 # FLAG(11, 25)
    Unk_17A = 0x17A # FLAG(11, 26)
    StateBlueDoorTOS26F = 0x17B # FLAG(11, 27)
    DestroyedRocksAroundReisHouse = 0x17C # FLAG(11, 28)
    TalkedToReiAfterDestroyingRocks = 0x17D # FLAG(11, 29)
    MetLinebeckFirstTime2 = 0x17E # FLAG(11, 30)
    TalkedToHyruleCastleBackExitGuardWithSword = 0x17F # FLAG(11, 31)
    CompletedLuciaSidequest = 0x180 # FLAG(12, 0)
    CompletedFerrusSidequest1 = 0x181 # FLAG(12, 1)
    GoronTargetRangeShortTrack = 0x182 # FLAG(12, 2)
    ActivatedSWSnowPortal = 0x183 # FLAG(12, 3)
    ActivatedSouthSnowPortal = 0x184 # FLAG(12, 4)
    ActivateSEForestPortal = 0x185 # FLAG(12, 5)
    ActivatedSWForestPortal = 0x186 # FLAG(12, 6)
    ActivatedSWFirePortal = 0x187 # FLAG(12, 7)
    ActivatedNEDesertPortal = 0x188 # FLAG(12, 8)
    ActivatedNESnowPortal = 0x189 # FLAG(12, 9)
    ActivatedWestOceanPortal = 0x18A # FLAG(12, 10)
    WatchedSecondPhantomPossessionCS = 0x18B # FLAG(12, 11)
    ZeldaTextSecondPhantomPossession = 0x18C # FLAG(12, 12)
    WrongPathLostWoodsPreHints = 0x18D # FLAG(12, 13)
    Unk_18E = 0x18E # FLAG(12, 14)
    Unk_18F = 0x18F # FLAG(12, 15)
    Unk_190 = 0x190 # FLAG(12, 16)
    Unk_191 = 0x191 # FLAG(12, 17)
    ObtainedBeedleFreebieCard = 0x192 # FLAG(12, 18)
    ObtainedBeedleQuintuplePointsCard = 0x193 # FLAG(12, 19)
    ObtainedBeedlePointsCard = 0x194 # FLAG(12, 20)
    Unk_195 = 0x195 # FLAG(12, 21)
    Unk_196 = 0x196 # FLAG(12, 22)
    Unk_197 = 0x197 # FLAG(12, 23)
    Unk_198 = 0x198 # FLAG(12, 24)
    MetGoronIronSellerFirstTime = 0x199 # FLAG(12, 25)
    MetMiddleGoronInDarkOreMine = 0x19A # FLAG(12, 26)
    AcceptGoronAdultRequestForMegaIceSidequest = 0x19B # FLAG(12, 27)
    Unk_19C = 0x19C # FLAG(12, 28)
    TalkedToNiboshiAboutIceForFish = 0x19D # FLAG(12, 29)
    GaveIceToNiboshi = 0x19E # FLAG(12, 30)
    TalkedToMashAboutIronForAxes = 0x19F # FLAG(12, 31)
    GaveIronToMash = 0x1A0 # FLAG(13, 0)
    Unk_1A1 = 0x1A1 # FLAG(13, 1)
    Unk_1A2 = 0x1A2 # FLAG(13, 2)
    ObtainedBowAndArrows = 0x1A3 # FLAG(13, 3)
    MetMashFirstTime = 0x1A4 # FLAG(13, 4)
    MetWadatsumiFirstTime = 0x1A5 # FLAG(13, 5)
    WadatsumiBoardsTrain = 0x1A6 # FLAG(13, 6)
    WadatsumiMeetsOrca = 0x1A7 # FLAG(13, 7)
    Unk_1A8 = 0x1A8 # FLAG(13, 8)
    Unk_1A9 = 0x1A9 # FLAG(13, 9)
    WatchedOrcaWadatsumiCS = 0x1AA # FLAG(13, 10)
    Unk_1AB = 0x1AB # FLAG(13, 11)
    MetOrcaFirstTime = 0x1AC # FLAG(13, 12)
    TalkedToOrcaAboutManToMarry = 0x1AD # FLAG(13, 13)
    YamahikoBoardsTrain = 0x1AE # FLAG(13, 14)
    MorrisBoardsTrain = 0x1AF # FLAG(13, 15)
    MashBoardsTrain = 0x1B0 # FLAG(13, 16)
    Unk_1B1 = 0x1B1 # FLAG(13, 17)
    DovokBoardsTrain = 0x1B2 # FLAG(13, 18)
    WatchedOrcaDovokCS = 0x1B3 # FLAG(13, 19)
    WatchedOrcaYamahikoCS = 0x1B4 # FLAG(13, 20)
    WatchedOrcaMorrisCS = 0x1B5 # FLAG(13, 21)
    WatchedOrcaMashCS = 0x1B6 # FLAG(13, 22)
    Unk_1B7 = 0x1B7 # FLAG(13, 23)
    Unk_1B8 = 0x1B8 # FLAG(13, 24)
    CompletedLinebeckSidequest = 0x1B9 # FLAG(13, 25)
    CompletedHarrySidequest = 0x1BA # FLAG(13, 26)
    CompletedChildGoronSidequest = 0x1BB # FLAG(13, 27)
    TalkedToTeacherPostSpiritZelda = 0x1BC # FLAG(13, 28)
    KofuBoardsTrain = 0x1BD # FLAG(13, 29)
    FailedKofuTrainRide = 0x1BE # FLAG(13, 30)
    Unk_1BF = 0x1BF # FLAG(13, 31)
    CompletedKofuSidequest = 0x1C0 # FLAG(14, 0)
    GoronAdultBoardsTrain = 0x1C1 # FLAG(14, 1)
    FailedGoronAdultTrainRide = 0x1C2 # FLAG(14, 2)
    ConfirmedToGoronAdultAboutSnow = 0x1C3 # FLAG(14, 3)
    CompletedGoronAdultSidequest = 0x1C4 # FLAG(14, 4)
    FailedWadatsumiTrainRide = 0x1C5 # FLAG(14, 5)
    FailedYamahikoTrainRide = 0x1C6 # FLAG(14, 6)
    FailedMorrisTrainRide = 0x1C7 # FLAG(14, 7)
    FailedMashTrainRide = 0x1C8 # FLAG(14, 8)
    Unk_1C9 = 0x1C9 # FLAG(14, 9)
    FailedDovokTrainRide = 0x1CA # FLAG(14, 10)
    GotYamahikoToPapuzia = 0x1CB # FLAG(14, 11)
    GotMorrisToPapuzia = 0x1CC # FLAG(14, 12)
    GotMashToPapuzia = 0x1CD # FLAG(14, 13)
    Unk_1CE = 0x1CE # FLAG(14, 14)
    GotDovokToPapuzia = 0x1CF # FLAG(14, 15)
    ChildGoronBoardsTrain = 0x1D0 # FLAG(14, 16)
    FailedChildGoronTrainRide = 0x1D1 # FLAG(14, 17)
    TalkedToChildGoronAboutCastleTown = 0x1D2 # FLAG(14, 18)
    GotChildGoronToCastleTown = 0x1D3 # FLAG(14, 19)
    NokoBoardsTrain = 0x1D4 # FLAG(14, 20)
    FailedNokoTrainRide = 0x1D5 # FLAG(14, 21)
    GotNokoToIcySpring = 0x1D6 # FLAG(14, 22)
    FerrusBoardsTrainToOutset = 0x1D7 # FLAG(14, 23)
    FailedFerrusTrainRideToOutset = 0x1D8 # FLAG(14, 24)
    GotFerrusToOutsetVillage = 0x1D9 # FLAG(14, 25)
    FerrusBoardsTrainToMarineTemple = 0x1DA # FLAG(14, 26)
    FailedFerrusTrainRideToMarineTemple = 0x1DB # FLAG(14, 27)
    CompletedFerrusSidequest2 = 0x1DC # FLAG(14, 28)
    MonaBoardsTrain = 0x1DD # FLAG(14, 29)
    FailedMonaTrainRide = 0x1DE # FLAG(14, 30)
    GotMonaToRabbitHaven = 0x1DF # FLAG(14, 31)
    FailedCarbenTrainRide = 0x1E0 # FLAG(15, 0)
    JoeBoardsTrain = 0x1E1 # FLAG(15, 1)
    FailedJoeTrainRide = 0x1E2 # FLAG(15, 2)
    GotJoeToBeedlesAirShop = 0x1E3 # FLAG(15, 3)
    KenzoBoardsTrainToBuildFence = 0x1E4 # FLAG(15, 4)
    FailedKenzoTrainRideToAnouki = 0x1E5 # FLAG(15, 5)
    GotKenzoToAnouki = 0x1E6 # FLAG(15, 6)
    ZeldaTextBigRockBlockingSnowLand = 0x1E7 # FLAG(15, 7)
    YekoTextAfterKenzoStartsWorkOnFence = 0x1E8 # FLAG(15, 8)
    TalkedToYekoAboutLumberAndHandyman = 0x1E9 # FLAG(15, 9)
    YekoTextAfterBringingKenzo = 0x1EA # FLAG(15, 10)
    YekoTextAfterKenzoStartsWorkOnFence2 = 0x1EB # FLAG(15, 11)
    NokoTextAfterReceivingForceGem = 0x1EC # FLAG(15, 12)
    SafeZoneTutorial = 0x1ED # FLAG(15, 13)
    EnteredSnowLandFirstTime = 0x1EE # FLAG(15, 14)
    ReadStoneTabletDisorientationStation = 0x1EF # FLAG(15, 15)
    HyruleGuardTextDisorientationStation = 0x1F0 # FLAG(15, 16)
    FoundTreasureDisorientationStation = 0x1F1 # FLAG(15, 17)
    FailedToSaveWadatsumi = 0x1F2 # FLAG(15, 18)
    GoronAdultTextAfterAcceptingMegaIceRequest = 0x1F3 # FLAG(15, 19)
    FoundRegalRingTradingPost = 0x1F4 # FLAG(15, 20)
    Unk_1F5 = 0x1F5 # FLAG(15, 21)
    WatchedBunnioMonaCS = 0x1F6 # FLAG(15, 22)
    Unk_1F7 = 0x1F7 # FLAG(15, 23)
    VisitedDarkOreMineFirstTime = 0x1F8 # FLAG(15, 24)
    PlayedGoronTargetRange = 0x1F9 # FLAG(15, 25)
    MetGoronAtGoronTargetRangeFirstTime = 0x1FA # FLAG(15, 26)
    Unk_1FB = 0x1FB # FLAG(15, 27)
    Unk_1FC = 0x1FC # FLAG(15, 28)
    Unk_1FD = 0x1FD # FLAG(15, 29)
    CompletedMonaSidequest = 0x1FE # FLAG(15, 30)
    Unk_1FF = 0x1FF # FLAG(15, 31)
    TalkedToFerrusAboutOutset = 0x200 # FLAG(16, 0)
    TalkedToKofuInGoronHouse = 0x201 # FLAG(16, 1)
    ZeldaTextActivatePortalFirstTime = 0x202 # FLAG(16, 2)
    FailedToSaveWadatsumi2 = 0x203 # FLAG(16, 3)
    Unk_204 = 0x204 # FLAG(16, 4)
    GaveVesselToSteem = 0x205 # FLAG(16, 5)
    Unk_206 = 0x206 # FLAG(16, 6)
    Unk_207 = 0x207 # FLAG(16, 7)
    ZeldaTextTOS18F = 0x208 # FLAG(16, 8)
    ZeldaTextTOS30F = 0x209 # FLAG(16, 9)
    Unk_20A = 0x20A # FLAG(16, 10)
    Unk_20B = 0x20B # FLAG(16, 11)
    Unk_20C = 0x20C # FLAG(16, 12)
    CompletedSteemSidequest = 0x20D # FLAG(16, 13)
    Unk_20E = 0x20E # FLAG(16, 14)
    Unk_20F = 0x20F # FLAG(16, 15)
    Unk_210 = 0x210 # FLAG(16, 16)
    ZeldaTextKeyMastersTOS22F = 0x211 # FLAG(16, 17)
    ZeldaTextPostCameraPanCSTOS20F = 0x212 # FLAG(16, 18)
    Unk_213 = 0x213 # FLAG(16, 19)
    TeacherBoardsTrain = 0x214 # FLAG(16, 20)
    Unk_215 = 0x215 # FLAG(16, 21)
    TalkedToHarryWithInsufficientCuccos = 0x216 # FLAG(16, 22)
    ZeldaTextMayscoreFirstTime = 0x217 # FLAG(16, 23)
    Unk_218 = 0x218 # FLAG(16, 24)
    Unk_219 = 0x219 # FLAG(16, 25)
    Unk_21A = 0x21A # FLAG(16, 26)
    Unk_21B = 0x21B # FLAG(16, 27)
    Unk_21C = 0x21C # FLAG(16, 28)
    Unk_21D = 0x21D # FLAG(16, 29)
    GotTeacherToAnoukiVillage = 0x21E # FLAG(16, 30)
    Unk_21F = 0x21F # FLAG(16, 31)
    FailedTeacherTrainRide = 0x220 # FLAG(17, 0)
    ZeldaTextSWPerchTOS6F = 0x221 # FLAG(17, 1)
    TalkedToRaelAboutCuccos = 0x222 # FLAG(17, 2)
    CompletedRaelSidequest = 0x223 # FLAG(17, 3)
    Unk_224 = 0x224 # FLAG(17, 4)
    TalkedToFerrusAboutMarineTemple = 0x225 # FLAG(17, 5)
    StateBlueDoor1TOS25F = 0x226 # FLAG(17, 6)
    StateBlueDoor2TOS25F = 0x227 # FLAG(17, 7)
    StateFarSWTorchTOS29F = 0x228 # FLAG(17, 8)
    SpawnWarpPhantomsTOS29F = 0x229 # FLAG(17, 9)
    ObtainedNESmallKeyTOS6F = 0x22A # FLAG(17, 10)
    StateCenterBlueDoorTOS27F = 0x22B # FLAG(17, 11)
    PressedNWSwitch = 0x22C # FLAG(17, 12)
    StateSouthBlueDoorTOS30F = 0x22D # FLAG(17, 13)
    StateEastBlueDoorTOS30F = 0x22E # FLAG(17, 14)
    Unk_22F = 0x22F # FLAG(17, 15)
    OpenedDoubleDoorsTOS1F = 0x230 # FLAG(17, 16)
    Unk_231 = 0x231 # FLAG(17, 17)
    StateSETorchNextToEyeTOS29F = 0x232 # FLAG(17, 18)
    ShotSEEyeSwitch29F = 0x233 # FLAG(17, 19)
    ShotSEEyeSwitch29F2 = 0x234 # FLAG(17, 20)
    ZeldaTextAfterEndTOS2SwordFadeCS = 0x235 # FLAG(17, 21)
    UncoveredSongOfBirdsStatue = 0x236 # FLAG(17, 22)
    Unk_237 = 0x237 # FLAG(17, 23)
    Unk_238 = 0x238 # FLAG(17, 24)
    LeftBeedleAfterJoeSidequest = 0x239 # FLAG(17, 25)
    Unk_23A = 0x23A # FLAG(17, 26)
    WiseOneFortuneForSongOfBirdsStatue = 0x23B # FLAG(17, 27)
    WiseOneFortuneFirstTime = 0x23C # FLAG(17, 28)
    Unk_23D = 0x23D # FLAG(17, 29)
    Unk_23E = 0x23E # FLAG(17, 30)
    Unk_23F = 0x23F # FLAG(17, 31)
    Unk_240 = 0x240 # FLAG(18, 0)
    Unk_241 = 0x241 # FLAG(18, 1)
    WadatsumiMinigameSequence = 0x242 # FLAG(18, 2)
    EncouragedChildGoronCityLife = 0x243 # FLAG(18, 3)
    WatchedAlfonzoCannonCS = 0x244 # FLAG(18, 4)
    Unk_245 = 0x245 # FLAG(18, 5)
    ShotNorthEyeSwitchTOS27F = 0x246 # FLAG(18, 6)
    ShotSouthEyeSwitchTOS27F = 0x247 # FLAG(18, 7)
    BrokeLeftWestArmosTOS30F = 0x248 # FLAG(18, 8)
    BrokeSouthArmosTOS30F2 = 0x249 # FLAG(18, 9)
    BrokeRightWestArmorTOS30F = 0x24A # FLAG(18, 10)
    BrokeSouthArmosTOS30F = 0x24B # FLAG(18, 11)
    StateSouthBlueDoorTOS27F = 0x24C # FLAG(18, 12)
    Unk_24D = 0x24D # FLAG(18, 13)
    SpawnThreePhantomEyesTOS27F = 0x24E # FLAG(18, 14)
    ReachedBeyondWestSandPitTOS27F = 0x24F # FLAG(18, 15)
    ReachedLargeFarWestSandPitTOS27F = 0x250 # FLAG(18, 16)
    StateTorch1TOS29F = 0x251 # FLAG(18, 17)
    StateTorch2TOS29F = 0x252 # FLAG(18, 18)
    StateTorch3TOS29F = 0x253 # FLAG(18, 19)
    StateTorch4TOS29F = 0x254 # FLAG(18, 20)
    Unk_255 = 0x255 # FLAG(18, 21)
    Unk_256 = 0x256 # FLAG(18, 22)
    Unk_257 = 0x257 # FLAG(18, 23)
    Unk_258 = 0x258 # FLAG(18, 24)
    Unk_259 = 0x259 # FLAG(18, 25)
    TalkedToWarpPhantomWithZeldaTOS29F = 0x25A # FLAG(18, 26)
    Unk_25B = 0x25B # FLAG(18, 27)
    TalkedToPhantomWithZeldaTOS25F = 0x25C # FLAG(18, 28)
    Unk_25D = 0x25D # FLAG(18, 29)
    Unk_25E = 0x25E # FLAG(18, 30)
    Unk_25F = 0x25F # FLAG(18, 31)
    Unk_260 = 0x260 # FLAG(19, 0)
    Unk_261 = 0x261 # FLAG(19, 1)
    TalkedToGoronElderAfterChildGoronSidequest = 0x262 # FLAG(19, 2)
    Unk_263 = 0x263 # FLAG(19, 3)
    Unk_264 = 0x264 # FLAG(19, 4)
    StateTorch5TOS29F = 0x265 # FLAG(19, 5)
    BrokeArmos2TOS27F = 0x266 # FLAG(19, 6)
    BrokeArmos4TOS27F = 0x267 # FLAG(19, 7)
    BrokeArmos3TOS27F = 0x268 # FLAG(19, 8)
    BrokeArmos1TOS27F = 0x269 # FLAG(19, 9)
    BrokeBlockPillar1TOS27F = 0x26A # FLAG(19, 10)
    BrokeBlockPillar2TOS27F = 0x26B # FLAG(19, 11)
    BrokeBlockPillar3TOS27F = 0x26C # FLAG(19, 12)
    BrokeBlockPillar4TOS27F = 0x26D # FLAG(19, 13)
    Unk_26E = 0x26E # FLAG(19, 14)
    Unk_26F = 0x26F # FLAG(19, 15)
    Unk_270 = 0x270 # FLAG(19, 16)
    Unk_271 = 0x271 # FLAG(19, 17)
    BrokeArmos2TOS25F = 0x272 # FLAG(19, 18)
    BrokeArmos3TOS25F = 0x273 # FLAG(19, 19)
    BrokeArmos4TOS25F = 0x274 # FLAG(19, 20)
    TalkedToKenzoDuringFenceWork = 0x275 # FLAG(19, 21)
    Unk_276 = 0x276 # FLAG(19, 22)
    ZeldaTextGotLostInBlizzard = 0x277 # FLAG(19, 23)
    Unk_278 = 0x278 # FLAG(19, 24)
    Unk_279 = 0x279 # FLAG(19, 25)
    WatchedOrcaWadatsumiCS2 = 0x27A # FLAG(19, 26)
    ObtainedWhip = 0x27B # FLAG(19, 27)
    OrcaSidequestStart = 0x27C # FLAG(19, 28)
    Unk_27D = 0x27D # FLAG(19, 29)
    Unk_27E = 0x27E # FLAG(19, 30)
    Unk_27F = 0x27F # FLAG(19, 31)
    EnteredOceanLandFirstTime = 0x280 # FLAG(20, 0)
    EnteredFireLandFirstTime = 0x281 # FLAG(20, 1)
    StateNESouthOrbSwitchTOS30F = 0x282 # FLAG(20, 2)
    StateNENorthOrbSwitchTOS30F = 0x283 # FLAG(20, 3)
    StateSETorchTOS29F = 0x284 # FLAG(20, 4)
    ObtainedSmallKeyFromSpinutTOS5F = 0x285 # FLAG(20, 5)
    Unk_286 = 0x286 # FLAG(20, 6)
    WatchedCameraPanEyeSwitch1CSTOS27F = 0x287 # FLAG(20, 7)
    WatchedCameraPanEyeSwitch2CSTOS27F = 0x288 # FLAG(20, 8)
    SpawnedPhantomTOS30F = 0x289 # FLAG(20, 9)
    Unk_28A = 0x28A # FLAG(20, 10)
    ObtainedBunnioHeartContainer5Rabbits = 0x28B # FLAG(20, 11)
    ObtainedBunnioRewardEveryVariety = 0x28C # FLAG(20, 12)
    ObtainedBunnioReward10ForestRabbits = 0x28D # FLAG(20, 13)
    ObtainedBunnioReward10SnowRabbits = 0x28E # FLAG(20, 14)
    ObtainedBunnioReward10OceanRabbits = 0x28F # FLAG(20, 15)
    ObtainedBunnioReward10MountainRabbits = 0x290 # FLAG(20, 16)
    ObtainedBunnioReward10DesertRabbits = 0x291 # FLAG(20, 17)
    BunnioTextAfterMonaAndHimGetAlong = 0x292 # FLAG(20, 18)
    ObtainedSwordsmansScroll1 = 0x293 # FLAG(20, 19)
    Unk_294 = 0x294 # FLAG(20, 20)
    Unk_295 = 0x295 # FLAG(20, 21)
    Unk_296 = 0x296 # FLAG(20, 22)
    EnteredTOSStaircaseFirstTime = 0x297 # FLAG(20, 23)
    ZeldaTextTOSStaircaseHigher = 0x298 # FLAG(20, 24)
    ZeldaTextTOS29F = 0x299 # FLAG(20, 25)
    ZeldaTextTOS28F = 0x29A # FLAG(20, 26)
    Unk_29B = 0x29B # FLAG(20, 27)
    ZeldaTextTOS26F = 0x29C # FLAG(20, 28)
    ZeldaTextDefeatedEnemiesTOS26F = 0x29D # FLAG(20, 29)
    ZeldaTextTOS25F = 0x29E # FLAG(20, 30)
    CompletedAllFerrusSidequests = 0x29F # FLAG(20, 31)
    Unk_2A0 = 0x2A0 # FLAG(21, 0)
    Unk_2A1 = 0x2A1 # FLAG(21, 1)
    GaveLumberToYeko = 0x2A2 # FLAG(21, 2)
    ZeldaTextEnterPortalFirstTime = 0x2A3 # FLAG(21, 3)
    Unk_2A4 = 0x2A4 # FLAG(21, 4)
    ZeldaTextEncounterSnurgleFirstTime = 0x2A5 # FLAG(21, 5)
    WatchedKagoronGoronAdultPreWagonCS = 0x2A6 # FLAG(21, 6)
    EnteredTwistedTunnelsFirstTime = 0x2A7 # FLAG(21, 7)
    WatchedStavenPreBattleCS = 0x2A8 # FLAG(21, 8)
    EscapedTwistedTunnelsFirstTime = 0x2A9 # FLAG(21, 9)
    GotDarkRealmTearOfLightFirstTime = 0x2AA # FLAG(21, 10)
    Unk_2AB = 0x2AB # FLAG(21, 11)
    ToldHyruleGuardTruthAboutFriendDisorientationStation = 0x2AC # FLAG(21, 12)
    BridgeRepairQuestStart = 0x2AD # FLAG(21, 13)
    DestroyDesertTempleCannonsQuestStart = 0x2AE # FLAG(21, 14)
    ZeldaTextBrokenBridge = 0x2AF # FLAG(21, 15)
    DefeatedRocktiteEastTunnelFireLand = 0x2B0 # FLAG(21, 16)
    Unk_2B1 = 0x2B1 # FLAG(21, 17)
    Unk_2B2 = 0x2B2 # FLAG(21, 18)
    Unk_2B3 = 0x2B3 # FLAG(21, 19)
    Unk_2B4 = 0x2B4 # FLAG(21, 20)
    Unk_2B5 = 0x2B5 # FLAG(21, 21)
    WatchedDarkTrainForestLandCS = 0x2B6 # FLAG(21, 22)
    CompletedSnowdriftStationPuzzle = 0x2B7 # FLAG(21, 23)
    ZeldaTextSlipperyStationFirstTime = 0x2B8 # FLAG(21, 24)
    CompletedSlipperyStationRaces = 0x2B9 # FLAG(21, 25)
    ObtainedRegalRingEndOfTheEarthStation = 0x2BA # FLAG(21, 26)
    RocktiteEastTunnelFireLandBattleStart = 0x2BB # FLAG(21, 27)
    ZeldaTextPreDemonTrainBattle = 0x2BC # FLAG(21, 28)
    DefeatedDemonTrain = 0x2BD # FLAG(21, 29)
    LearntSongOfAwakening = 0x2BE # FLAG(21, 30)
    ZeldaTextSandWand = 0x2BF # FLAG(21, 31)
    StateSWBridgeTOS27F = 0x2C0 # FLAG(22, 0)
    Unk_2C1 = 0x2C1 # FLAG(22, 1)
    StateWestBridgeTOS15F = 0x2C2 # FLAG(22, 2)
    Unk_2C3 = 0x2C3 # FLAG(22, 3)
    TalkedToMashAfterOrcaSidequest = 0x2C4 # FLAG(22, 4)
    TalkedToWoodNearWhipMinigameFirstTime = 0x2C5 # FLAG(22, 5)
    Unk_2C6 = 0x2C6 # FLAG(22, 6)
    VisitedIslandSanctuaryFirstTime = 0x2C7 # FLAG(22, 7)
    Unk_2C8 = 0x2C8 # FLAG(22, 8)
    GoronAdultTextAfterGivingMegaIce = 0x2C9 # FLAG(22, 9)
    WatchedLavaGoneGoronVillageCS = 0x2CA # FLAG(22, 10)
    SavedWadatsumi = 0x2CB # FLAG(22, 11)
    Unk_2CC = 0x2CC # FLAG(22, 12)
    DefeatedDemonTrain2 = 0x2CD # FLAG(22, 13)
    Unk_2CE = 0x2CE # FLAG(22, 14)
    Unk_2CF = 0x2CF # FLAG(22, 15)
    Unk_2D0 = 0x2D0 # FLAG(22, 16)
    Unk_2D1 = 0x2D1 # FLAG(22, 17)
    Unk_2D2 = 0x2D2 # FLAG(22, 18)
    Unk_2D3 = 0x2D3 # FLAG(22, 19)
    Unk_2D4 = 0x2D4 # FLAG(22, 20)
    Unk_2D5 = 0x2D5 # FLAG(22, 21)
    Unk_2D6 = 0x2D6 # FLAG(22, 22)
    Unk_2D7 = 0x2D7 # FLAG(22, 23)
    Unk_2D8 = 0x2D8 # FLAG(22, 24)
    Unk_2D9 = 0x2D9 # FLAG(22, 25)
    Unk_2DA = 0x2DA # FLAG(22, 26)
    Unk_2DB = 0x2DB # FLAG(22, 27)
    Unk_2DC = 0x2DC # FLAG(22, 28)
    Unk_2DD = 0x2DD # FLAG(22, 29)
    Unk_2DE = 0x2DE # FLAG(22, 30)
    Unk_2DF = 0x2DF # FLAG(22, 31)
    Unk_2E0 = 0x2E0 # FLAG(23, 0)
    Unk_2E1 = 0x2E1 # FLAG(23, 1)
    Unk_2E2 = 0x2E2 # FLAG(23, 2)
    Unk_2E3 = 0x2E3 # FLAG(23, 3)
    Unk_2E4 = 0x2E4 # FLAG(23, 4)
    Unk_2E5 = 0x2E5 # FLAG(23, 5)
    Unk_2E6 = 0x2E6 # FLAG(23, 6)
    Unk_2E7 = 0x2E7 # FLAG(23, 7)
    Unk_2E8 = 0x2E8 # FLAG(23, 8)
    Unk_2E9 = 0x2E9 # FLAG(23, 9)
    Unk_2EA = 0x2EA # FLAG(23, 10)
    Unk_2EB = 0x2EB # FLAG(23, 11)
    Unk_2EC = 0x2EC # FLAG(23, 12)
    Unk_2ED = 0x2ED # FLAG(23, 13)
    Unk_2EE = 0x2EE # FLAG(23, 14)
    Unk_2EF = 0x2EF # FLAG(23, 15)
    Unk_2F0 = 0x2F0 # FLAG(23, 16)
    Unk_2F1 = 0x2F1 # FLAG(23, 17)
    Unk_2F2 = 0x2F2 # FLAG(23, 18)
    Unk_2F3 = 0x2F3 # FLAG(23, 19)
    Unk_2F4 = 0x2F4 # FLAG(23, 20)
    Unk_2F5 = 0x2F5 # FLAG(23, 21)
    Unk_2F6 = 0x2F6 # FLAG(23, 22)
    Unk_2F7 = 0x2F7 # FLAG(23, 23)
    Unk_2F8 = 0x2F8 # FLAG(23, 24)
    Unk_2F9 = 0x2F9 # FLAG(23, 25)
    Unk_2FA = 0x2FA # FLAG(23, 26)
    Unk_2FB = 0x2FB # FLAG(23, 27)
    Unk_2FC = 0x2FC # FLAG(23, 28)
    Unk_2FD = 0x2FD # FLAG(23, 29)
    Unk_2FE = 0x2FE # FLAG(23, 30)
    Unk_2FF = 0x2FF # FLAG(23, 31)
    Unk_300 = 0x300 # FLAG(24, 0)
    Unk_301 = 0x301 # FLAG(24, 1)
    Unk_302 = 0x302 # FLAG(24, 2)
    Unk_303 = 0x303 # FLAG(24, 3)
    Unk_304 = 0x304 # FLAG(24, 4)
    Unk_305 = 0x305 # FLAG(24, 5)
    Unk_306 = 0x306 # FLAG(24, 6)
    Unk_307 = 0x307 # FLAG(24, 7)
    Unk_308 = 0x308 # FLAG(24, 8)
    Unk_309 = 0x309 # FLAG(24, 9)
    Unk_30A = 0x30A # FLAG(24, 10)
    Unk_30B = 0x30B # FLAG(24, 11)
    Unk_30C = 0x30C # FLAG(24, 12)
    Unk_30D = 0x30D # FLAG(24, 13)
    Unk_30E = 0x30E # FLAG(24, 14)
    Unk_30F = 0x30F # FLAG(24, 15)
    Unk_310 = 0x310 # FLAG(24, 16)
    Unk_311 = 0x311 # FLAG(24, 17)
    Unk_312 = 0x312 # FLAG(24, 18)
    Unk_313 = 0x313 # FLAG(24, 19)
    Unk_314 = 0x314 # FLAG(24, 20)
    Unk_315 = 0x315 # FLAG(24, 21)
    Unk_316 = 0x316 # FLAG(24, 22)
    Unk_317 = 0x317 # FLAG(24, 23)
    Unk_318 = 0x318 # FLAG(24, 24)
    Unk_319 = 0x319 # FLAG(24, 25)
    Unk_31A = 0x31A # FLAG(24, 26)
    Unk_31B = 0x31B # FLAG(24, 27)
    Unk_31C = 0x31C # FLAG(24, 28)
    Unk_31D = 0x31D # FLAG(24, 29)
    Unk_31E = 0x31E # FLAG(24, 30)
    Unk_31F = 0x31F # FLAG(24, 31)
    Unk_320 = 0x320 # FLAG(25, 0)
    Unk_321 = 0x321 # FLAG(25, 1)
    Unk_322 = 0x322 # FLAG(25, 2)
    Unk_323 = 0x323 # FLAG(25, 3)
    Unk_324 = 0x324 # FLAG(25, 4)
    Unk_325 = 0x325 # FLAG(25, 5)
    Unk_326 = 0x326 # FLAG(25, 6)
    Unk_327 = 0x327 # FLAG(25, 7)
    Unk_328 = 0x328 # FLAG(25, 8)
    Unk_329 = 0x329 # FLAG(25, 9)
    Unk_32A = 0x32A # FLAG(25, 10)
    Unk_32B = 0x32B # FLAG(25, 11)
    Unk_32C = 0x32C # FLAG(25, 12)
    Unk_32D = 0x32D # FLAG(25, 13)
    Unk_32E = 0x32E # FLAG(25, 14)
    Unk_32F = 0x32F # FLAG(25, 15)
    Unk_330 = 0x330 # FLAG(25, 16)
    Unk_331 = 0x331 # FLAG(25, 17)
    Unk_332 = 0x332 # FLAG(25, 18)
    Unk_333 = 0x333 # FLAG(25, 19)
    Unk_334 = 0x334 # FLAG(25, 20)
    Unk_335 = 0x335 # FLAG(25, 21)
    Unk_336 = 0x336 # FLAG(25, 22)
    Unk_337 = 0x337 # FLAG(25, 23)
    Unk_338 = 0x338 # FLAG(25, 24)
    Unk_339 = 0x339 # FLAG(25, 25)
    Unk_33A = 0x33A # FLAG(25, 26)
    Unk_33B = 0x33B # FLAG(25, 27)
    Unk_33C = 0x33C # FLAG(25, 28)
    Unk_33D = 0x33D # FLAG(25, 29)
    Unk_33E = 0x33E # FLAG(25, 30)
    Unk_33F = 0x33F # FLAG(25, 31)
    Unk_340 = 0x340 # FLAG(26, 0)
    Unk_341 = 0x341 # FLAG(26, 1)
    Unk_342 = 0x342 # FLAG(26, 2)
    Unk_343 = 0x343 # FLAG(26, 3)
    Unk_344 = 0x344 # FLAG(26, 4)
    Unk_345 = 0x345 # FLAG(26, 5)
    Unk_346 = 0x346 # FLAG(26, 6)
    Unk_347 = 0x347 # FLAG(26, 7)
    Unk_348 = 0x348 # FLAG(26, 8)
    Unk_349 = 0x349 # FLAG(26, 9)
    Unk_34A = 0x34A # FLAG(26, 10)
    Unk_34B = 0x34B # FLAG(26, 11)
    Unk_34C = 0x34C # FLAG(26, 12)
    Unk_34D = 0x34D # FLAG(26, 13)
    Unk_34E = 0x34E # FLAG(26, 14)
    Unk_34F = 0x34F # FLAG(26, 15)
    Unk_350 = 0x350 # FLAG(26, 16)
    Unk_351 = 0x351 # FLAG(26, 17)
    Unk_352 = 0x352 # FLAG(26, 18)
    Unk_353 = 0x353 # FLAG(26, 19)
    Unk_354 = 0x354 # FLAG(26, 20)
    Unk_355 = 0x355 # FLAG(26, 21)
    Unk_356 = 0x356 # FLAG(26, 22)
    Unk_357 = 0x357 # FLAG(26, 23)
    Unk_358 = 0x358 # FLAG(26, 24)
    Unk_359 = 0x359 # FLAG(26, 25)
    Unk_35A = 0x35A # FLAG(26, 26)
    Unk_35B = 0x35B # FLAG(26, 27)
    Unk_35C = 0x35C # FLAG(26, 28)
    Unk_35D = 0x35D # FLAG(26, 29)
    Unk_35E = 0x35E # FLAG(26, 30)
    Unk_35F = 0x35F # FLAG(26, 31)
    Unk_360 = 0x360 # FLAG(27, 0)
    Unk_361 = 0x361 # FLAG(27, 1)
    Unk_362 = 0x362 # FLAG(27, 2)
    Unk_363 = 0x363 # FLAG(27, 3)
    Unk_364 = 0x364 # FLAG(27, 4)
    Unk_365 = 0x365 # FLAG(27, 5)
    Unk_366 = 0x366 # FLAG(27, 6)
    Unk_367 = 0x367 # FLAG(27, 7)
    Unk_368 = 0x368 # FLAG(27, 8)
    Unk_369 = 0x369 # FLAG(27, 9)
    Unk_36A = 0x36A # FLAG(27, 10)
    Unk_36B = 0x36B # FLAG(27, 11)
    Unk_36C = 0x36C # FLAG(27, 12)
    Unk_36D = 0x36D # FLAG(27, 13)
    Unk_36E = 0x36E # FLAG(27, 14)
    Unk_36F = 0x36F # FLAG(27, 15)
    Unk_370 = 0x370 # FLAG(27, 16)
    Unk_371 = 0x371 # FLAG(27, 17)
    Unk_372 = 0x372 # FLAG(27, 18)
    Unk_373 = 0x373 # FLAG(27, 19)
    Unk_374 = 0x374 # FLAG(27, 20)
    Unk_375 = 0x375 # FLAG(27, 21)
    Unk_376 = 0x376 # FLAG(27, 22)
    Unk_377 = 0x377 # FLAG(27, 23)
    Unk_378 = 0x378 # FLAG(27, 24)
    Unk_379 = 0x379 # FLAG(27, 25)
    Unk_37A = 0x37A # FLAG(27, 26)
    Unk_37B = 0x37B # FLAG(27, 27)
    Unk_37C = 0x37C # FLAG(27, 28)
    Unk_37D = 0x37D # FLAG(27, 29)
    Unk_37E = 0x37E # FLAG(27, 30)
    Unk_37F = 0x37F # FLAG(27, 31)
    Unk_380 = 0x380 # FLAG(28, 0)
    Unk_381 = 0x381 # FLAG(28, 1)
    Unk_382 = 0x382 # FLAG(28, 2)
    Unk_383 = 0x383 # FLAG(28, 3)
    Unk_384 = 0x384 # FLAG(28, 4)
    Unk_385 = 0x385 # FLAG(28, 5)
    Unk_386 = 0x386 # FLAG(28, 6)
    Unk_387 = 0x387 # FLAG(28, 7)
    Unk_388 = 0x388 # FLAG(28, 8)
    Unk_389 = 0x389 # FLAG(28, 9)
    Unk_38A = 0x38A # FLAG(28, 10)
    Unk_38B = 0x38B # FLAG(28, 11)
    Unk_38C = 0x38C # FLAG(28, 12)
    Unk_38D = 0x38D # FLAG(28, 13)
    Unk_38E = 0x38E # FLAG(28, 14)
    Unk_38F = 0x38F # FLAG(28, 15)
    Unk_390 = 0x390 # FLAG(28, 16)
    Unk_391 = 0x391 # FLAG(28, 17)
    Unk_392 = 0x392 # FLAG(28, 18)
    Unk_393 = 0x393 # FLAG(28, 19)
    Unk_394 = 0x394 # FLAG(28, 20)
    Unk_395 = 0x395 # FLAG(28, 21)
    Unk_396 = 0x396 # FLAG(28, 22)
    Unk_397 = 0x397 # FLAG(28, 23)
    Unk_398 = 0x398 # FLAG(28, 24)
    Unk_399 = 0x399 # FLAG(28, 25)
    Unk_39A = 0x39A # FLAG(28, 26)
    Unk_39B = 0x39B # FLAG(28, 27)
    Unk_39C = 0x39C # FLAG(28, 28)
    Unk_39D = 0x39D # FLAG(28, 29)
    Unk_39E = 0x39E # FLAG(28, 30)
    Unk_39F = 0x39F # FLAG(28, 31)
    Unk_3A0 = 0x3A0 # FLAG(29, 0)
    Unk_3A1 = 0x3A1 # FLAG(29, 1)
    Unk_3A2 = 0x3A2 # FLAG(29, 2)
    Unk_3A3 = 0x3A3 # FLAG(29, 3)
    Unk_3A4 = 0x3A4 # FLAG(29, 4)
    Unk_3A5 = 0x3A5 # FLAG(29, 5)
    Unk_3A6 = 0x3A6 # FLAG(29, 6)
    Unk_3A7 = 0x3A7 # FLAG(29, 7)
    Unk_3A8 = 0x3A8 # FLAG(29, 8)
    Unk_3A9 = 0x3A9 # FLAG(29, 9)
    Unk_3AA = 0x3AA # FLAG(29, 10)
    Unk_3AB = 0x3AB # FLAG(29, 11)
    Unk_3AC = 0x3AC # FLAG(29, 12)
    Unk_3AD = 0x3AD # FLAG(29, 13)
    Unk_3AE = 0x3AE # FLAG(29, 14)
    Unk_3AF = 0x3AF # FLAG(29, 15)
    Unk_3B0 = 0x3B0 # FLAG(29, 16)
    Unk_3B1 = 0x3B1 # FLAG(29, 17)
    Unk_3B2 = 0x3B2 # FLAG(29, 18)
    Unk_3B3 = 0x3B3 # FLAG(29, 19)
    Unk_3B4 = 0x3B4 # FLAG(29, 20)
    Unk_3B5 = 0x3B5 # FLAG(29, 21)
    Unk_3B6 = 0x3B6 # FLAG(29, 22)
    Unk_3B7 = 0x3B7 # FLAG(29, 23)
    Unk_3B8 = 0x3B8 # FLAG(29, 24)
    Unk_3B9 = 0x3B9 # FLAG(29, 25)
    Unk_3BA = 0x3BA # FLAG(29, 26)
    Unk_3BB = 0x3BB # FLAG(29, 27)
    Unk_3BC = 0x3BC # FLAG(29, 28)
    Unk_3BD = 0x3BD # FLAG(29, 29)
    Unk_3BE = 0x3BE # FLAG(29, 30)
    Unk_3BF = 0x3BF # FLAG(29, 31)
    Unk_3C0 = 0x3C0 # FLAG(30, 0)
    Unk_3C1 = 0x3C1 # FLAG(30, 1)
    Unk_3C2 = 0x3C2 # FLAG(30, 2)
    Unk_3C3 = 0x3C3 # FLAG(30, 3)
    Unk_3C4 = 0x3C4 # FLAG(30, 4)
    Unk_3C5 = 0x3C5 # FLAG(30, 5)
    Unk_3C6 = 0x3C6 # FLAG(30, 6)
    Unk_3C7 = 0x3C7 # FLAG(30, 7)
    Unk_3C8 = 0x3C8 # FLAG(30, 8)
    Unk_3C9 = 0x3C9 # FLAG(30, 9)
    Unk_3CA = 0x3CA # FLAG(30, 10)
    Unk_3CB = 0x3CB # FLAG(30, 11)
    Unk_3CC = 0x3CC # FLAG(30, 12)
    Unk_3CD = 0x3CD # FLAG(30, 13)
    Unk_3CE = 0x3CE # FLAG(30, 14)
    Unk_3CF = 0x3CF # FLAG(30, 15)
    Unk_3D0 = 0x3D0 # FLAG(30, 16)
    Unk_3D1 = 0x3D1 # FLAG(30, 17)
    Unk_3D2 = 0x3D2 # FLAG(30, 18)
    Unk_3D3 = 0x3D3 # FLAG(30, 19)
    Unk_3D4 = 0x3D4 # FLAG(30, 20)
    Unk_3D5 = 0x3D5 # FLAG(30, 21)
    Unk_3D6 = 0x3D6 # FLAG(30, 22)
    Unk_3D7 = 0x3D7 # FLAG(30, 23)
    Unk_3D8 = 0x3D8 # FLAG(30, 24)
    Unk_3D9 = 0x3D9 # FLAG(30, 25)
    Unk_3DA = 0x3DA # FLAG(30, 26)
    Unk_3DB = 0x3DB # FLAG(30, 27)
    Unk_3DC = 0x3DC # FLAG(30, 28)
    Unk_3DD = 0x3DD # FLAG(30, 29)
    Unk_3DE = 0x3DE # FLAG(30, 30)
    Unk_3DF = 0x3DF # FLAG(30, 31)
    Unk_3E0 = 0x3E0 # FLAG(31, 0)
    Unk_3E1 = 0x3E1 # FLAG(31, 1)
    Unk_3E2 = 0x3E2 # FLAG(31, 2)
    Unk_3E3 = 0x3E3 # FLAG(31, 3)
    Unk_3E4 = 0x3E4 # FLAG(31, 4)
    Unk_3E5 = 0x3E5 # FLAG(31, 5)
    Unk_3E6 = 0x3E6 # FLAG(31, 6)
    Unk_3E7 = 0x3E7 # FLAG(31, 7)
    Unk_3E8 = 0x3E8 # FLAG(31, 8)
    Unk_3E9 = 0x3E9 # FLAG(31, 9)
    Unk_3EA = 0x3EA # FLAG(31, 10)
    Unk_3EB = 0x3EB # FLAG(31, 11)
    Unk_3EC = 0x3EC # FLAG(31, 12)
    Unk_3ED = 0x3ED # FLAG(31, 13)
    Unk_3EE = 0x3EE # FLAG(31, 14)
    Unk_3EF = 0x3EF # FLAG(31, 15)
    Unk_3F0 = 0x3F0 # FLAG(31, 16)
    Unk_3F1 = 0x3F1 # FLAG(31, 17)
    Unk_3F2 = 0x3F2 # FLAG(31, 18)
    Unk_3F3 = 0x3F3 # FLAG(31, 19)
    Unk_3F4 = 0x3F4 # FLAG(31, 20)
    Unk_3F5 = 0x3F5 # FLAG(31, 21)
    Unk_3F6 = 0x3F6 # FLAG(31, 22)
    Unk_3F7 = 0x3F7 # FLAG(31, 23)
    Unk_3F8 = 0x3F8 # FLAG(31, 24)
    Unk_3F9 = 0x3F9 # FLAG(31, 25)
    Unk_3FA = 0x3FA # FLAG(31, 26)
    Unk_3FB = 0x3FB # FLAG(31, 27)
    Unk_3FC = 0x3FC # FLAG(31, 28)
    Unk_3FD = 0x3FD # FLAG(31, 29)
    Unk_3FE = 0x3FE # FLAG(31, 30)
    Unk_3FF = 0x3FF # FLAG(31, 31)


class ConditionKind(IntEnum):
    ObtainedItem = 0
    ObtainedItemAny = 1
    AdventureFlag = 2
