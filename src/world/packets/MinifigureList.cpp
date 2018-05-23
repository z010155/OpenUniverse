#include "MinifigureList.h"

namespace OpenUniverse {
namespace World {
namespace Packets {
void Minifigure::serialize(RakNet::BitStream* stream)
{
    stream->Write(characterID);
    stream->Write((uint32_t)0);

    Utils::writeWString(stream, name, 33);
    Utils::writeWString(stream, unnaprovedName, 33);

    stream->Write((unsigned char)isNameRejected);
    stream->Write((unsigned char)isFreeToPlay);

    Utils::writeString(stream, "", 10);

    stream->Write(shirtColor);
    stream->Write(shirtStyle);
    stream->Write(pantsColor);
    stream->Write(hairStyle);
    stream->Write(hairColor);
    stream->Write(lh);
    stream->Write(rh);
    stream->Write(eyebrowStyle);
    stream->Write(eyeStyle);
    stream->Write(mouthStyle);
    stream->Write((uint32_t)0);

    stream->Write(zone);
    stream->Write(instance);
    stream->Write(clone);
    stream->Write(lastLogin);

    stream->Write((uint16_t)items.size());

    for (auto item : items)
        stream->Write(item);
}

MinifigureList::MinifigureList()
{
    connectionType = ConnectionType::SERVER;
    packetID = 6;
}

MinifigureList::~MinifigureList()
{
}

void MinifigureList::serialize(RakNet::BitStream* stream) {
    LUPacket::serialize(stream);

    stream->Write((unsigned char)characters.size());
    stream->Write(selectedIndex);

    for (auto character : characters)
        character->serialize(stream);
}
}
}
}
