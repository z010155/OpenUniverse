#include "Utils.h"

namespace OpenUniverse {
namespace Core {
Utils::~Utils()
{
}

// https://stackoverflow.com/questions/15333259/c-stdwstring-to-stdstring-quick-and-dirty-conversion-for-use-as-key-in
std::string Utils::wstringToString(std::wstring wstr)
{   
    return std::string((const char*) &wstr[0], sizeof(wchar_t) / sizeof(char) * wstr.size());
}

std::wstring Utils::stringToWString(std::string str)
{
    return std::wstring((const wchar_t*) &str[0], sizeof(char)  / sizeof(wchar_t) * str.size());
}

// https://stackoverflow.com/questions/23689733/convert-string-from-utf-8-to-iso-8859-1
std::wstring Utils::toLatin1(std::wstring wstr)
{
    std::wstring out;
    std::transform(wstr.cbegin(), wstr.cend(), std::back_inserter(out), [](const wchar_t c)
    {
        return c <= 255 ? c : '?';
    });

    return out;
}

std::string Utils::toLatin1(std::string str)
{
    std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;

    auto wide = converter.from_bytes(str);

    std::string out;
    out.reserve(wide.length());

    std::transform(wide.cbegin(), wide.cend(), std::back_inserter(out), [](const wchar_t c)
    {
        return c <= 255 ? c : '?';
    });

    return out;
}

// https://stackoverflow.com/questions/5586214/how-to-convert-char-from-iso-8859-1-to-utf-8-in-c-multiplatformly#5586678
std::wstring Utils::toUTF8(std::wstring wstr)
{
    std::wstring out;

    for (uint8_t c : wstr) {
        if (c < 0x80)
            out += c;
        else {
            out += 0xc0 | (c & 0xc0) >> 6;
            out += 0x80 | (c & 0x3f);
        }
    }

    return out;
}

std::string Utils::toUTF8(std::string str)
{
    std::string out;

    for (uint8_t c : str) {
        if (c < 0x80)
            out += c;
        else {
            out += 0xc0 | (c & 0xc0) >> 6;
            out += 0x80 | (c & 0x3f);
        }
    }

    return out;
}

std::wstring Utils::readWString(RakNet::BitStream* stream, uint32_t size = 33)
{
    std::wstring wstr;
    
    wstr.reserve(size);

    // auto end = false;

    for (uint32_t i = 0; i < size; i++) {
        char character;

        stream->Read(character);

        if (character == 0)
            continue;
            // end = true;

        // if (!end)
        wstr += character;
    }

    return wstr;
}

std::string Utils::readString(RakNet::BitStream* stream, uint32_t size = 33)
{
    std::string str;

    str.reserve(size);

    // auto end = false;

    for (uint32_t i = 0; i < size; i++) {
        char character;

        stream->Read(character);

        if (character == 0)
            continue;
            // end = true;

        // if (!end)
        str += character;
    }

    return str;
}

void Utils::writeWString(RakNet::BitStream* stream, std::wstring str, unsigned int size = 33)
{
    for (unsigned int i = 0; i < size; i++)
        stream->Write(i < str.length() ? (char)str[i] : (char)0);
}

void Utils::writeString(RakNet::BitStream* stream, std::string str, unsigned int size = 33)
{
    for (unsigned int i = 0; i < size; i++)
        stream->Write(i < str.length() ? (char)str[i] : (char)0);
}
}
}
