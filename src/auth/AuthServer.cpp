#include "AuthServer.h"

namespace OpenUniverse {
namespace Auth {
AuthServer::AuthServer() : Server()
{
    port = 1001;
}

AuthServer::~AuthServer()
{
}

void AuthServer::handlePacket(RakNet::BitStream* stream, Packet* p)
{
    auto header = Core::Packets::PacketHeader::deserialize(stream);

    switch (header->rakID) {
    case ID_USER_PACKET_ENUM:
        switch (header->remoteConnectionType) {
        case ConnectionType::GENERAL:
            if (header->packetID == 0)
                makeHandshake(stream, p, 1);
            break;
        case ConnectionType::AUTH:
            if (header->packetID == 0)
                handleLoginPacket(stream, p);
            break;
        }
        break;
    }
}

void AuthServer::handleLoginPacket(RakNet::BitStream* stream, Packet* p)
{
    auto info = Auth::Packets::LoginInfo::deserialize(stream);

    std::cout << "[AUTH] User: " << Utils::wstringToString(info->username) << " Pass: " << Utils::wstringToString(info->password);
}

void AuthServer::serverStarted()
{
    std::cout << "[AUTH] Server started" << std::endl;
}

void AuthServer::serverStartFailed()
{
    std::cout << "[AUTH] !! Server failed to start !!" << std::endl;
}
}
}
