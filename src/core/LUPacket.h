#ifndef __LU_LUPACKET_H__
#define __LU_LUPACKET_H__

#include "Serializable.h"

namespace OpenUniverse {
namespace Core {
class LUPacket : public Serializable {
protected:
    uint16_t connectionType;
    uint32_t packetID;

public:
    void serialize(RakNet::BitStream*);

    static LUPacket* deserialize(RakNet::BitStream*);
};
}
}

#endif
