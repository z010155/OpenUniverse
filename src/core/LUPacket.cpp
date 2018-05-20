#include "LUPacket.h"

namespace OpenUniverse {
namespace Core {
void LUPacket::serialize(RakNet::BitStream* stream)
{
    stream->Write((unsigned char)0x53);
    stream->Write(connectionType);
    stream->Write(packetID);
    stream->Write((unsigned char)0);
}

LUPacket* LUPacket::deserialize(RakNet::BitStream*)
{
    return new LUPacket();
}
}
}
