#include "AuthServer.h"

namespace OpenUniverse {
namespace Auth {
AuthServer::AuthServer(Database* database) : Server()
{
    db = database;
    port = 1001;
    logger = new Logger("AUTH");
}

AuthServer::~AuthServer()
{
    delete logger;
}

void AuthServer::handlePacket(RakNet::BitStream* stream, Packet* p)
{
    auto header = Core::Packets::PacketHeader::deserialize(stream);

    switch (header->rakID) {
    case ID_USER_PACKET_ENUM:
        switch (header->remoteConnectionType) {
        case ConnectionType::GENERAL:
            if (header->packetID == 0) {
                logger->info("Handshake packet received...");
                makeHandshake(stream, p, 1);
            }
            break;
        case ConnectionType::AUTH:
            if (header->packetID == 0) {
                logger->info("Login info packet received...");
                handleLoginPacket(stream, p);
            }
            break;
        }
        break;
    }

    delete header;
}

void AuthServer::handleLoginPacket(RakNet::BitStream* stream, Packet* p)
{
    auto info = Auth::Packets::LoginInfo::deserialize(stream);
    auto packet = new Auth::Packets::LoginInfo();

    auto user = Utils::wstringToString(info->username);
    auto password = Utils::wstringToString(info->password);

    auto account = db->authenticate(user, password);

    packet->loginStatus = account ? 0x01 : 0x06;

    // FIXME: add a config
    packet->userToken = L"test";
    packet->serverInstanceIP = "127.0.0.1";
    packet->chatInstanceIP = "127.0.0.1";
    packet->serverInstancePort = 2001;
    packet->chatInstancePort = 2002;

    RakNet::BitStream bs;

    packet->serialize(&bs);

    uint8_t rakID;
    uint16_t networkType;
    uint32_t packetID;
    uint8_t pad;
    
    bs.Read(rakID);
    bs.Read(networkType);
    bs.Read(packetID);
    bs.Read(pad);

    uint8_t loginStatus;

    bs.Read(loginStatus);

    auto tlap = Utils::readString(&bs, 33);

    for (int i = 0; i < 7; i++)
        Utils::readString(&bs, 33);

    uint16_t major;
    uint16_t current;
    uint16_t minor;

    bs.Read(major);
    bs.Read(current);
    bs.Read(minor);

    auto key = Utils::wstringToString(Utils::readWString(&bs, 33));
    auto charIP = Utils::readString(&bs, 33);
    auto chatIP = Utils::readString(&bs, 33);
    
    uint16_t charPort;
    uint16_t chatPort;

    bs.Read(charPort);
    bs.Read(chatPort);

    auto ip = Utils::readString(&bs, 33);
    auto guid = Utils::readString(&bs, 37);

    logger->info(std::to_string(loginStatus));
    logger->info(tlap);
    logger->info(std::to_string(major) + "." + std::to_string(current) + "." + std::to_string(minor));
    logger->info(key);
    logger->info(charIP);
    logger->info(chatIP);
    logger->info(std::to_string(charPort));
    logger->info(std::to_string(chatPort));
    logger->info(ip);
    logger->info(guid);


    send(packet, p->systemAddress, false);

    delete info;
}

void AuthServer::serverStarted()
{
    logger->info("Server started");
}

void AuthServer::serverStartFailed()
{
    logger->error("Server failed to start");
}
}
}
