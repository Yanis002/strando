#include "036_MapA5.hpp"
#include "ItemIdMaps.hpp"
#include "rando.hpp"
#include "settings.hpp"

#include <Actor/ActorUnkKEYB.hpp>
#include <Actor/ActorUnkKEYT.hpp>
#include <Unknown/UnkStruct_027e09b8.hpp>

extern "C" bool func_ov041_02129ec0(Actor* thisx, ActorGrabParams grabParams);

bool BossKeyItemGive(ItemId itemId) {
    switch (gpSettings->GetShuffleDungeonSettings()->bksanity) {
        case BossKeysanityMode_Dungeon:
        case BossKeysanityMode_Anywhere:
            if (!data_027e09b8->HasAdventureFlag(gAdvFlagMap[itemId])) {
                // we can't use the give function directly because we're in a blocking interaction
                gRando.TryAddItemToQueue(itemId);
            }

            return false;
        case BossKeysanityMode_Off:
        case BossKeysanityMode_Removed:
        default:
            break;
    }

    return true;
}

class CustomBossKey : public ActorUnkKEYB {
  public:
    bool CustomGrab(ActorGrabParams grabParams);
};

bool CustomBossKey::CustomGrab(ActorGrabParams grabParams) {
    // prevent grabbing the key when interacting with it if bksanity is enabled
    // this is done simply by returning false

    if (BossKeyItemGive(this->mUnk_5C.mParams[3])) {
        return func_ov041_02129ec0(this, grabParams);
    }

    return false;
}

class CustomTrapBossKey : public ActorUnkKEYT {
  public:
    bool CustomGrab(ActorGrabParams grabParams);
};

bool CustomTrapBossKey::CustomGrab(ActorGrabParams grabParams) {
    if (BossKeyItemGive(this->mUnk_5C.mParams[3])) {
        return this->ActorUnkKEYT::Grab(grabParams);
    }

    return false;
}
