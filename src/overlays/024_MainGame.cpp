#include "gz.hpp"
#include "settings.hpp"

#include "Save/AdventureFlags.hpp"
#include <MainGame/CargoManager.hpp>
#include <MainGame/PassengerManager.hpp>
#include <Unknown/UnkStruct_027e09b8.hpp>
#include <Unknown/UnkStruct_027e0d34.hpp>

extern "C" SceneIndex func_ov000_0205c984();
extern "C" u32 func_ov000_0205c9b4();

class CustomPassengerManager : public PassengerManager {
  public:
    bool CustomTryBoardTrain(ActorId actorId, SceneIndex sceneIndex, u32 roomIndex);
};

struct PassengerPickUpInfos {
    u8 sceneIndex;
    ActorId actorId;
};

static PassengerPickUpInfos sPassengerPickUpInfos[Passenger_Max] = {
    {SceneIndex_f_tetsuo, ActorId_YKCP}, // Passenger_AnoukiNoko
    {SceneIndex_f_flame5, ActorId_YKAP}, // Passenger_AnoukiKofu
    {SceneIndex_f_rabbit, ActorId_CAWB}, // Passenger_CastleTownMona
    {SceneIndex_f_first, ActorId_SIRO}, // Passenger_CastleTownAlfonzo
    {SceneIndex_f_first, ActorId_TMNA}, // Passenger_SnowRealmFerrus
    {SceneIndex_d_water27, ActorId_TMNA}, // Passenger_FireRealmFerrus
    {SceneIndex_f_snow, ActorId_GORP}, // Passenger_GoronVillageSnowGoron
    {SceneIndex_f_htown, ActorId_GOCP}, // Passenger_GoronVillageCityGoron
    {SceneIndex_f_water, ActorId_FOMR}, // Passenger_MayscoreDovok
    {SceneIndex_f_water, ActorId_FOMB}, // Passenger_MayscoreMash
    {SceneIndex_f_water, ActorId_FOMA}, // Passenger_MayscoreMorris
    {SceneIndex_f_water, ActorId_FOMC}, // Passenger_MayscoreYamahiko
    {SceneIndex_f_water, ActorId_FOPD}, // Passenger_MayscoreWood
    {SceneIndex_f_trnnpc, ActorId_NCCA}, // Passenger_OutsetJoe
    {SceneIndex_f_water, ActorId_WAMA}, // Passenger_PirateHideoutWadatsumi
    {SceneIndex_f_bridge2, ActorId_CRFP}, // Passenger_BridgeWorkersHomeKenzo
    {SceneIndex_f_snow, ActorId_CRFP}, // Passenger_TradingPostKenzo
    {SceneIndex_f_water2, ActorId_SYWA}, // Passenger_PapuziaVillageCarben
};

int GetPassengerFromPickUpInfos(ActorId actorId, SceneIndex destSceneIndex) {
    for (int i = 0; i < Passenger_Max; i++) {
        PassengerPickUpInfos* pEntry = &sPassengerPickUpInfos[i];

        if (pEntry->actorId == actorId && pEntry->sceneIndex == destSceneIndex) {
            return i;
        }
    }

    return -1;
}

ItemId GetItemIdFromPassengerPickUpInfos(ActorId actorId, SceneIndex destSceneIndex) {
    int passenger = GetPassengerFromPickUpInfos(actorId, destSceneIndex);
    return passenger != -1 ? gSettings.GetPassengerPickUpItemId(passenger) : ItemId_None;
}

bool CustomPassengerManager::CustomTryBoardTrain(ActorId actorId, SceneIndex destSceneIndex, u32 roomIndex) {
    switch (gSettings.GetShuffleSettings()->passengers) {
        case PassengerMode_Vanilla:
            return this->TryBoardTrain(actorId, destSceneIndex, roomIndex);
        case PassengerMode_Abstract:
        case PassengerMode_Anywhere:
            gGZ.TryAddItemToQueue(GetItemIdFromPassengerPickUpInfos(actorId, destSceneIndex));
            break;
        default:
            break;
    }

    return false;
}

class CustomCargoManager : public CargoManager {
  public:
    void CustomReset();
    void CustomInit(unk32 type, unk32 amount);
};

void CustomCargoManager::CustomReset() {
    // this executes when an actor tries to clear the cargo

    switch (gSettings.GetShuffleSettings()->cargo) {
        case CargoMode_Vanilla:
            this->Reset();
            break;
        case CargoMode_Abstract:
        case CargoMode_Anywhere:
            // the actors will handle giving the item so we have nothing to do
            break;
        default:
            break;
    }
}

void CustomCargoManager::CustomInit(unk32 type, unk32 amount) {
    // this executes when an actor tries to initialize the cargo
    // instead of letting things happen normally (except for vanilla), we give a cargo pick up item

    switch (gSettings.GetShuffleSettings()->cargo) {
        case CargoMode_Vanilla:
            this->Init(type, amount);
            break;
        case CargoMode_Abstract:
        case CargoMode_Anywhere:
            gGZ.TryAddItemToQueue(gSettings.GetCargoPickUpItemId(type));
            break;
        default:
            break;
    }
}
