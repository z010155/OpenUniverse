#include "Handshake.h"

namespace OpenUniverse {
namespace Core {
namespace Packets {
Handshake::Handshake()
{
    connectionType = ConnectionType::GENERAL;
    packetID = 0;
}

Handshake::~Handshake()
{
}

void Handshake::serialize(RakNet::BitStream* stream)
{
    LUPacket::serialize(stream);

    stream->Write(gameVersion);
    stream->Write((uint32_t)0x93);
    stream->Write(remoteConnectionType);
    stream->Write(pid);
    stream->Write(port);
    stream->Write(ip);
}

Handshake* Handshake::deserialize(RakNet::BitStream* stream)
{
    auto handshake = new Handshake();

    stream->Read(handshake->gameVersion);
    stream->Read(handshake->unknown1);
    stream->Read(handshake->remoteConnectionType);
    stream->Read(handshake->pid);
    stream->Read(handshake->port);
    stream->Read(handshake->ip);

    return handshake;
}
}
}
}
