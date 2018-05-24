#ifndef __LU_MINIFIGURECREATE_H__
#define __LU_MINIFIGURECREATE_H__

#include <string>

#include "../../core/Utils.h"
#include "../../core/LUPacket.h"

using namespace OpenUniverse::Core;

namespace OpenUniverse {
namespace World {
namespace Packets {
class MinifigureCreate : public LUPacket {
public:
    std::wstring name;
    uint32_t predef1;
    uint32_t predef2;
    uint32_t predef3;
    std::string unknown1;
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
    unsigned char unknown2;

    MinifigureCreate();

    static MinifigureCreate* deserialize(RakNet::BitStream* stream);
};
}
}
}

#endif
