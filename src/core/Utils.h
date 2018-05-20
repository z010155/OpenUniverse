#ifndef __LU_UTILS_H__
#define __LU_UTILS_H__

#include <string>
#include <locale>
#include <codecvt>

#include "raknet/BitStream.h"

namespace OpenUniverse {
namespace Core {
class Utils {
public:
    virtual ~Utils();

    static std::string wstringToString(std::wstring);
    static std::wstring stringToWString(std::string);

    static std::wstring readWString(RakNet::BitStream*, unsigned int);
    static std::string readString(RakNet::BitStream*, unsigned int);

    static void writeWString(RakNet::BitStream*, std::wstring, unsigned int);
    static void writeString(RakNet::BitStream*, std::string, unsigned int);
};
}
}

#endif
