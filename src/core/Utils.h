#ifndef __LU_UTILS_H__
#define __LU_UTILS_H__

#include <string>
#include <locale>
#include <codecvt>
#include <algorithm>
#include <iterator>
#include <sstream>

#include "raknet/BitStream.h"

namespace OpenUniverse {
namespace Core {
class Utils {
public:
    virtual ~Utils();

    static std::string wstringToString(std::wstring);
    static std::wstring stringToWString(std::string);

    static std::string toLatin1(std::string);
    static std::wstring toLatin1(std::wstring);
    static std::string toUTF8(std::string);
    static std::wstring toUTF8(std::wstring);

    static std::wstring readWString(RakNet::BitStream*, uint32_t);
    static std::string readString(RakNet::BitStream*, uint32_t);

    static void writeWString(RakNet::BitStream*, std::wstring, unsigned int);
    static void writeString(RakNet::BitStream*, std::string, unsigned int);
};
}
}

#endif
