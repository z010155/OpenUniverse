#include "LoginInfo.h"

namespace OpenUniverse {
namespace Auth {
namespace Packets {
LoginInfo::LoginInfo()
{
}

LoginInfo::~LoginInfo()
{
}

void LoginInfo::serialize(RakNet::BitStream* stream)
{
    stream->Write(loginStatus);
    Utils::writeString(stream, "Talk_Like_A_Pirate", 33);

    for (int i = 0; i < 7; i++)
        Utils::writeString(stream, "", 33);

    stream->Write(clientVersionMajor);
    stream->Write(clientVersionCurrent);
    stream->Write(clientVersionMinor);
    
    Utils::writeWString(stream, userToken, 33);

    Utils::writeString(stream, serverInstanceIP, 33);
    Utils::writeString(stream, chatInstanceIP, 33);

    stream->Write(serverInstancePort);
    stream->Write(chatInstancePort);

    Utils::writeString(stream, ip, 33);
    Utils::writeString(stream, "00000000-0000-0000-0000-000000000000", 37);

    stream->Write((unsigned long)0);

    Utils::writeString(stream, locale, 3);

    stream->Write(firstLoginAfterSubscribing);
    stream->Write(freeToPlay);

    stream->Write((unsigned long long)0);

    stream->Write((unsigned short)errorMessage.size());
    Utils::writeWString(stream, errorMessage, (unsigned int)errorMessage.size());

    stream->Write(stampCount);
    // FIXME: add stamp data if needed
}

LoginInfo* LoginInfo::deserialize(RakNet::BitStream* stream)
{
    auto info = new LoginInfo();

    info->username = Utils::readWString(stream, 33);
    info->password = Utils::readWString(stream, 41);

    stream->Read(info->languageID);
    stream->Read(info->platformType);

    info->clientMemoryInfo = Utils::readWString(stream, 256);
    info->clientGraphicsInfo = Utils::readWString(stream, 128);

    stream->Read(info->processorCores);
    stream->Read(info->processorType);
    stream->Read(info->processorLevel);
    stream->Read(info->processorRevision);

    stream->Read(info->unknown1);

    stream->Read(info->osMajorVersion);
    stream->Read(info->osMinorVersion);
    stream->Read(info->osBuildNumber);
    stream->Read(info->platformID);

    return info;
}
}
}
}
