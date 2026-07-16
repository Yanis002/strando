#include "036_MapA5.hpp"

#include <MapObject/MapObject.hpp>
#include <MapObject/MapObjectUnkDRBK.hpp>
#include <Unknown/UnkStruct_027e09a4.hpp>
#include <Unknown/UnkStruct_027e09b8.hpp>

class CustomMapObject : public MapObject {
    MapObject* KillMapObject();
    void OpenDoorBossKey();
};

extern "C" MapObject* _ZN16MapObjectUnkDRBKC1Ev(MapObject*);

MapObject* CustomMapObject::KillMapObject() {
    UNSET_FLAG(this->mFlags, MapObjFlag_Alive);
    return this;
}

struct SceneToFlag {
    SceneIndex scene;
    u16 room;
    AdventureFlag_Half flag;
};

static SceneToFlag sSceneToFlag[] = {
    {.scene = SceneIndex_d_main, .room = 9, .flag = RandoAdventureFlag_BossKey_3},
    {.scene = SceneIndex_d_main, .room = 24, .flag = RandoAdventureFlag_BossKey_5},
    {.scene = SceneIndex_d_forest, .room = 2, .flag = RandoAdventureFlag_BossKey_Wooded},
    {.scene = SceneIndex_d_snow26, .room = 2, .flag = RandoAdventureFlag_BossKey_Blizzard},
    {.scene = SceneIndex_d_water27, .room = 5, .flag = RandoAdventureFlag_BossKey_Marine},
    {.scene = SceneIndex_d_flame, .room = 4, .flag = RandoAdventureFlag_BossKey_Mountain},
    {.scene = SceneIndex_d_sand, .room = 3, .flag = RandoAdventureFlag_BossKey_Desert},
};

void CustomMapObject::OpenDoorBossKey() {
    // open the door if necessary
    for (int i = 0; i < ARRAY_LEN(sSceneToFlag); i++) {
        SceneToFlag* pEntry = &sSceneToFlag[i];
        UnkStruct_WarpUnk1* pUnkStruct_WarpUnk1 = data_027e09a4->mpWarpUnk1;

        if (pUnkStruct_WarpUnk1 != NULL && pEntry->scene == (u32)pUnkStruct_WarpUnk1->mCurEntrance.sceneIndex &&
            pEntry->room == pUnkStruct_WarpUnk1->mCurEntrance.roomIndex &&
            GET_FLAG(data_027e09b8->mAdventureFlags, pEntry->flag)) {
            this->mUnk_16 = 4; // note: 3 would also work but with 4 the door opens instantly
        }
    }

    ((MapObjectUnkDRBK*)this)->func_ov041_0212be5c();
}
