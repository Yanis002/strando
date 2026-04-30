#include "gz.hpp"

#include <Actor/ActorManager.hpp>
#include <Item/ItemManager.hpp>
#include <Player/PlayerGet.hpp>
#include <Unknown/UnkStruct_027e09a4.hpp>

Actor* GetActor(ActorId actorId) {
    Actor** ppTable = gpActorManager->mActorTable;
    Actor** ppTableEnd = gpActorManager->mActorTableEnd;

    for (int i = 0; ppTable < ppTableEnd; i++) {
        Actor* pActor = ppTable[i];

        if (pActor != NULL && pActor->mpProfile->mActorId == actorId) {
            return pActor;
        }
    }

    return NULL;
}

extern "C" void GiveItemDuringCS(ItemManager* thisx, ItemFlag itemFlag) {
    ActorId actorId = ActorId_None;

    switch (data_027e09a4->mCutsceneIndex) {
        case CutsceneIndex_LokomoSword:
            actorId = ActorId_SYRN;
            break;
        case CutsceneIndex_SpiritPipes:
            actorId = ActorId_RMC3;
            break;
    }

    if (actorId != ActorId_None) {
        Actor* pActor = GetActor(actorId); // get anjean actor

        // hacky? idk (see GZ::OnGameModeUpdate)
        if (pActor != NULL) {
            gGZ.SetItemId(pActor->mUnk_5C.mParams[0]);
        }
    }
}
