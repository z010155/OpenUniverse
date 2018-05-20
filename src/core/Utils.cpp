#include "Utils.h"

namespace OpenUniverse {
namespace Core {
Utils::~Utils()
{
}

std::string Utils::wstringToString(std::wstring wstr)
{
    std::wstring_convert<std::codecvt_utf8<wchar_t>, wchar_t> converter;

    return converter.to_bytes(wstr);
}

std::wstring Utils::stringToWString(std::string str)
{
    std::wstring_convert<std::codecvt_utf8<wchar_t>, wchar_t> converter;

    return converter.from_bytes(str);
}

std::wstring Utils::readWString(RakNet::BitStream* stream, unsigned int size = 33)
{
    std::wstring str = L"";

    for (unsigned int i = 0; i < size; i++) {
        wchar_t character;

        stream->Read(character);

        if (!character)
            break;

        str += character;
    }

    return str;
}

std::string Utils::readString(RakNet::BitStream* stream, unsigned int size = 33)
{
    std::string str = "";

    for (unsigned int i = 0; i < size; i++) {
        char character;

        stream->Read(character);

        if (!character)
            break;

        str += character;
    }

    return str;
}

void Utils::writeWString(RakNet::BitStream* stream, std::wstring str, unsigned int size = 33)
{
    for (unsigned int i = 0; i < size - 1; i++) {
        if (i < str.size())
            stream->Write(str.at(i));
        else
            stream->Write((unsigned short)0);
    }

    stream->Write((unsigned short)0);
}

void Utils::writeString(RakNet::BitStream* stream, std::string str, unsigned int size = 33)
{
    for (unsigned int i = 0; i < size; i++) {
        if (i < size)
            stream->Write(str.at(i));
        else
            stream->Write((unsigned char)0);
    }

    stream->Write((unsigned char)0);
}
}
}
