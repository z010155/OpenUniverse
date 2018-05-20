#include "PacketHeader.h"

namespace OpenUniverse {
namespace Core {
namespace Packets {
PacketHeader::PacketHeader()
{
}

PacketHeader::~PacketHeader()
{
}

void PacketHeader::serialize(RakNet::BitStream* stream)
{
    stream->Write(rakID);
    stream->Write(remoteConnectionType);
    stream->Write(packetID);
    stream->Write(pad);
}

PacketHeader* PacketHeader::deserialize(RakNet::BitStream* stream)
{
    auto header = new PacketHeader();

    stream->Read(header->rakID);

    if (header->rakID == 0x53) {
        stream->Read(header->remoteConnectionType);
        stream->Read(header->packetID);
        stream->Read(header->pad);
    }

    return header;
}
}
}
}
