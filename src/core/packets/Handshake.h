#ifndef __LU_HANDSHAKE_H__
#define __LU_HANDSHAKE_H__

#include <string>

#include "../LUPacket.h"
#include "../Types.h"

namespace OpenUniverse {
namespace Core {
namespace Packets {
class Handshake : public LUPacket {
public:
    unsigned long gameVersion;
    unsigned long unknown1 = 0x93;
    unsigned long remoteConnectionType;
    unsigned long pid;
    unsigned short port = 0xff;
    std::string ip = "127.0.0.1";

    Handshake();

    virtual ~Handshake();

    void serialize(RakNet::BitStream*);

    static Handshake* deserialize(RakNet::BitStream*);
};
}
}
}

#endif
