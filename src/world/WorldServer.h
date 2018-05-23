#ifndef __LU_WORLDSERVER_H__
#define __LU_WORLDSERVER_H__

#include "raknet/MessageIdentifiers.h"

#include "../core/Server.h"
#include "../core/Database.h"
#include "../core/Logger.h"
#include "../core/packets/PacketHeader.h"
#include "packets/MinifigureList.h"

using namespace OpenUniverse::Core;

namespace OpenUniverse {
namespace World {
class WorldServer : public Server {
private:
    Database* db;
    Logger* logger;

    void handlePacket(RakNet::BitStream*, Packet*);
    void serverStarted();
    void serverStartFailed();

    void handleCharList(RakNet::BitStream*, Packet*);

public:
    WorldServer(Database*);

    ~WorldServer();
};
}
}

#endif
