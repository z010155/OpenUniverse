#ifndef __LU_PACKETHEADER_H__
#define __LU_PACKETHEADER_H__

#include "../Serializable.h"

namespace OpenUniverse {
namespace Core {
namespace Packets {
class PacketHeader : public Serializable {
public:
    unsigned char rakID = 0x53;
    uint16_t remoteConnectionType;
    uint32_t packetID;
    unsigned char pad = 0;

    PacketHeader();

    virtual ~PacketHeader();

    void serialize(RakNet::BitStream*);

    static PacketHeader* deserialize(RakNet::BitStream*);
};
}
}
}

#endif
