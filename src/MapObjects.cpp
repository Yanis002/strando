#include <MapObject/MapObject.hpp>

class CustomMapObject : public MapObject {
    MapObject* KillMapObject();
};

MapObject* CustomMapObject::KillMapObject() {
    UNSET_FLAG(this->mFlags, MapObjFlag_Alive);
    return this;
}
