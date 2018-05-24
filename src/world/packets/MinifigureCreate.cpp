#include "MinifigureCreate.h"

namespace OpenUniverse {
namespace World {
namespace Packets {
MinifigureCreate::MinifigureCreate()
{
}

MinifigureCreate* MinifigureCreate::deserialize(RakNet::BitStream* stream)
{
    auto packet = new MinifigureCreate();

    packet->name = Utils::readWString(stream, 33);

    stream->Read(packet->predef1);
    stream->Read(packet->predef2);
    stream->Read(packet->predef3);

    packet->unknown1 = Utils::readString(stream, 9);

    stream->Read(packet->shirtColor);
    stream->Read(packet->shirtStyle);
    stream->Read(packet->pantsColor);
    stream->Read(packet->hairStyle);
    stream->Read(packet->hairColor);
    stream->Read(packet->lh);
    stream->Read(packet->rh);
    stream->Read(packet->eyebrowStyle);
    stream->Read(packet->eyeStyle);
    stream->Read(packet->mouthStyle);

    stream->Read(packet->unknown2);

    return packet;
}
}
}
}
