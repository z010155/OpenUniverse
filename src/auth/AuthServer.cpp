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

    // FIXME: use a less resource heavy algorithm for hashing/checking passwords
    auto account = db->authenticate(user, password);

    if (!account)
        db->createAccount(user, password);

    packet->loginStatus = 0x01; // account ? 0x01 : 0x06;

    auto worldConf = cfg["world"].as<YAML::Node>();

    // FIXME: add a config
    packet->userToken = L"test";
    packet->serverInstanceIP = worldConf["host"].as<std::string>();
    packet->chatInstanceIP = "127.0.0.1";
    packet->serverInstancePort = worldConf["port"].as<int>();
    packet->chatInstancePort = 2002;
 
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
