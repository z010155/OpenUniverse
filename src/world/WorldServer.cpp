#include "WorldServer.h"

namespace OpenUniverse {
namespace World {
WorldServer::WorldServer(Database* database)
{
    port = cfg["world"].as<YAML::Node>()["port"].as<int>();
    logger = new Logger("WORLD");
    db = database;
}

WorldServer::~WorldServer()
{
    delete logger;
}

void WorldServer::handlePacket(RakNet::BitStream* stream, Packet* p)
{
    auto header = Core::Packets::PacketHeader::deserialize(stream);

    switch (header->rakID) {
    case ID_USER_PACKET_ENUM:
        switch (header->remoteConnectionType) {
        case ConnectionType::GENERAL:
            if (header->packetID == 0) {
                logger->info("Handshake packet received...");
                makeHandshake(stream, p, 4);
            }
            break;
        }
        case ConnectionType::CLIENT:
            switch (header->packetID) {
            case ClientPacket::MINIFIGURE_LIST_REQUEST:
                logger->info("Minifigure list request packet received");
                handleCharList(stream, p);
                break;
            }
            break;
        break;
    }

    delete header;
}

void WorldServer::handleCharList(RakNet::BitStream* stream, Packet* p)
{
    auto packet = new World::Packets::MinifigureList();

    std::vector<World::Packets::Minifigure*> characters;

    packet->selectedIndex = 0;
    packet->characters = characters;

    send(packet, p->systemAddress, false);
}

void WorldServer::serverStarted()
{
    logger->info("Server started");
}

void WorldServer::serverStartFailed()
{
    logger->error("Server failed to start");
}
}
}
