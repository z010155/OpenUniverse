#ifndef __LU_LOGININFO_H__
#define __LU_LOGININFO_H__

#include <string>

#include "../../core/LUPacket.h"
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
    unsigned short languageID;
    unsigned char platformType;
    std::wstring clientMemoryInfo;
    std::wstring clientGraphicsInfo;
    unsigned long processorCores;
    unsigned long processorType;
    unsigned short processorLevel;
    unsigned short processorRevision;
    unsigned long unknown1;
    unsigned long osMajorVersion;
    unsigned long osMinorVersion;
    unsigned long osBuildNumber;
    unsigned long platformID;

    // Server
    unsigned char loginStatus;
    unsigned short clientVersionMajor = 1;
    unsigned short clientVersionCurrent = 10;
    unsigned short clientVersionMinor = 64;
    std::wstring userToken;
    std::string serverInstanceIP;
    std::string chatInstanceIP;
    unsigned short serverInstancePort;
    unsigned short chatInstancePort;
    std::string ip = "127.0.0.1";
    std::string locale = "US";
    bool firstLoginAfterSubscribing = false;
    bool freeToPlay = false;
    std::wstring errorMessage = L"";
    unsigned long stampCount = 0;

    LoginInfo();

    virtual ~LoginInfo();

    void serialize(RakNet::BitStream*);

    static LoginInfo* deserialize(RakNet::BitStream*);
};
}
}
}

#endif
