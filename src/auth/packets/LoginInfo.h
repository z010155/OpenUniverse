#ifndef __LU_LOGININFO_H__
#define __LU_LOGININFO_H__

#include <string>

#include "../../core/LUPacket.h"
#include "../../core/Types.h"
#include "../../core/Utils.h"

using namespace OpenUniverse::Core;

namespace OpenUniverse {
namespace Auth {
namespace Packets {
class LoginInfo : public LUPacket {
public:
    // Client
    std::wstring username;
    std::wstring password;
    uint16_t languageID;
    unsigned char platformType;
    std::wstring clientMemoryInfo;
    std::wstring clientGraphicsInfo;
    uint32_t processorCores;
    uint32_t processorType;
    uint16_t processorLevel;
    uint16_t processorRevision;
    uint32_t unknown1;
    uint32_t osMajorVersion;
    uint32_t osMinorVersion;
    uint32_t osBuildNumber;
    uint32_t platformID;

    // Server
    unsigned char loginStatus;
    uint16_t clientVersionMajor = 1;
    uint16_t clientVersionCurrent = 10;
    uint16_t clientVersionMinor = 64;
    std::wstring userToken;
    std::string serverInstanceIP;
    std::string chatInstanceIP;
    uint16_t serverInstancePort;
    uint16_t chatInstancePort;
    std::string ip = "127.0.0.1";
    std::string locale = "US";
    bool firstLoginAfterSubscribing = false;
    bool freeToPlay = false;
    std::wstring errorMessage = L"";
    uint32_t stampCount = 0;

    LoginInfo();

    virtual ~LoginInfo();

    void serialize(RakNet::BitStream*);

    static LoginInfo* deserialize(RakNet::BitStream*);
};
}
}
}

#endif
