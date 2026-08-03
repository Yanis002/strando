#include "036_MapA5.hpp"
#include "settings.hpp"

#include <FileSelect/FileSelect.hpp>
#include <Save/SaveManager.hpp>

class CustomFileSelectMain : public FileSelectMain {
  public:
    void Custom_ov019_020c9c70();
    void SetStartingFlags();
};

static u32 sAdventureFlagsToSet[] = {
    // for Tower Sections
    AdventureFlag_Nothing,
    AdventureFlag_Nothing,
    AdventureFlag_Nothing,
    AdventureFlag_Nothing,
    AdventureFlag_Nothing,

    AdventureFlag_ObtainedSpiritTrain,
    AdventureFlag_CompletedForestRestorationSong, // skips lost woods
    AdventureFlag_ObtainedForestGlyph, // allows going to castle town and the tower, see `GZ::OnScenePreInit`
    AdventureFlag_CompletedSwordTutorial,
    AdventureFlag_PlayedHyruleGuardGetLostText,
    AdventureFlag_HyruleGuardMovesAfterCole,
    AdventureFlag_WatchedHyruleGuardColeCS,
    AdventureFlag_WatchedZeldasBedroomFirstCS,
    AdventureFlag_WatchedSpiritTowerSplitCS,
    AdventureFlag_MetAnjeanFirstTime,
    AdventureFlag_FleeFirstPhantomTOS,
    AdventureFlag_SpawnFirstPhantomTOS,
    AdventureFlag_RouteDrawTutorial,
    AdventureFlag_WatchedHyruleCastleSpiritZeldaCS,
    AdventureFlag_WatchedThroneRoomSpiritZeldaCS,
    AdventureFlag_BeatSnowRealmRocktite,
    AdventureFlag_WatchedWarpPhantomFirstTimeWarpingCS,
    AdventureFlag_TextPhantomInLava,
    AdventureFlag_TextTOSEntrance4F,
    AdventureFlag_WatchedIntroCS,
    AdventureFlag_WatchedFirstPhantomPossessionCS,
    AdventureFlag_WatchedForestTempleCompletedCS,
    AdventureFlag_TalkedToZeldaMayscoreFirstTime,
    AdventureFlag_TalkedToZeldaPhantomPossessionFirstTime,
    AdventureFlag_WhipMinigameTutorial,
    AdventureFlag_MetStavenInTOSAfterFireGlyphCS, // prevents warp to a cutscene
    AdventureFlag_ForestTracksRestoredFromGlyphCS, // prevents warp to a cutscene
    AdventureFlag_HyruleCastleZeldaControlsTutorial,
    AdventureFlag_WatchedZeldaSpiritThroneCS,
    AdventureFlag_WatchedEnterZeldasBedroomCS,
    AdventureFlag_SnowSongPracticeDone,
    AdventureFlag_SandSongPraticeDone,
    AdventureFlag_FerrusPassengerTutorial,
    AdventureFlag_TextRockNearRabbitland,
    AdventureFlag_CannonTutorial,
    AdventureFlag_WatchedOutsetTrainGarageCS,
    AdventureFlag_ZeldaTextTOS8F,
    AdventureFlag_ZeldaTextTOS13F,
    AdventureFlag_ZeldaTextTorchPhantomTOS9F,
    AdventureFlag_ZeldaTextKeyMastersTOS10F,
    AdventureFlag_FireSongPracticeDone,
    AdventureFlag_WatchedStavenPostBattleCS,
    AdventureFlag_WatchedMalladusOnTOSSummitCS,
    AdventureFlag_WatchedMountainTempleCompletedCS,
    AdventureFlag_SafeZoneTutorial,
    AdventureFlag_ZeldaTextMayscoreFirstTime,
    AdventureFlag_DefeatedRocktiteEastTunnelFireLand,
};

void CustomFileSelectMain::SetStartingFlags() {
    ShuffleSettings* pSettings = gpSettings->GetShuffleSettings();

    switch (gpSettings->GetShuffleDungeonSettings()->tos_sections) {
        case ToSSectionsMode_Open:
        case ToSSectionsMode_OpenNo6:
            sAdventureFlagsToSet[0] = RandoAdventureFlag_TowerSection_1;
            sAdventureFlagsToSet[1] = RandoAdventureFlag_TowerSection_2;
            sAdventureFlagsToSet[2] = RandoAdventureFlag_TowerSection_3;
            sAdventureFlagsToSet[3] = RandoAdventureFlag_TowerSection_4;
            sAdventureFlagsToSet[4] = RandoAdventureFlag_TowerSection_5;
            break;
        default:
            break;
    }

    for (int i = 0; i < MAX_SAVE_SLOTS; i++) {
        u32* pFlags = gSaveManager.GetSaveSlot(i)->mInfoData[0].inventory.adventureFlags;

        if (pSettings->forest_glyph == ForestGlyphMode_Startwith) {
            SET_FLAG(pFlags, RandoAdventureFlag_ForestGlyph);
        } else {
            UNSET_FLAG(pFlags, RandoAdventureFlag_ForestGlyph);
        }

        for (int j = 0; j < ARRAY_LEN(sAdventureFlagsToSet); j++) {
            u32 flag = sAdventureFlagsToSet[j];

            if (!GET_FLAG(pFlags, flag)) {
                SET_FLAG(pFlags, flag);
            }
        }
    }
}

void CustomFileSelectMain::Custom_ov019_020c9c70() {
    this->SetStartingFlags();
    this->func_ov019_020c9c70();
}
