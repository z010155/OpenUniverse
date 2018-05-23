#ifndef __LU_MINIFIGURELIST_H__
#define __LU_MINIFIGURELIST_H__

#include <vector>
#include <string>

#include "../../core/Utils.h"
#include "../../core/Types.h"
#include "../../core/LUPacket.h"

using namespace OpenUniverse::Core;

namespace OpenUniverse {
namespace World {
namespace Packets {
class Minifigure : public Serializable {
public:
    int64_t characterID;
    std::wstring name;
    std::wstring unnaprovedName;
    bool isNameRejected;
    bool isFreeToPlay;
    uint32_t shirtColor;
    uint32_t shirtStyle;
    uint32_t pantsColor;
    uint32_t hairStyle;
    uint32_t hairColor;
    uint32_t lh;
    uint32_t rh;
    uint32_t eyebrowStyle;
    uint32_t eyeStyle;
    uint32_t mouthStyle;
    uint16_t zone;
    uint16_t instance;
    uint32_t clone;
    uint64_t lastLogin;
    std::vector<uint32_t> items;

    void serialize(RakNet::BitStream*);
};

class MinifigureList : public LUPacket {
public:
    MinifigureList();

    virtual ~MinifigureList();

    unsigned char selectedIndex;
    std::vector<Minifigure*> characters;

    void serialize(RakNet::BitStream*);
};
}
}
}

#endif
