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
            case ClientPacket::MINIFIGURE_CREATE_REQUEST:
                logger->info("Minifigure create request packet received");
                handleCharCreate(stream, p);
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

void WorldServer::handleCharCreate(RakNet::BitStream* stream, Packet* p)
{
    auto request = World::Packets::MinifigureCreate::deserialize(stream);

    std::ifstream firstStream;
    std::ifstream middleStream;
    std::ifstream lastStream;
    
    firstStream.open("assets/names/minifigname_first.txt");
    middleStream.open("assets/names/minifigname_middle.txt");
    lastStream.open("assets/names/minifigname_last.txt");

    std::string first;
    std::string middle;
    std::string last;

    firstStream >> first;
    middleStream >> middle;
    lastStream >> last;

    auto firstParts = Utils::split(first, "\n");
    auto middleParts = Utils::split(middle, "\n");
    auto lastParts = Utils::split(last, "\n");
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
