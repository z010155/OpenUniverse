#ifndef __LU_WORLDSERVER_H__
#define __LU_WORLDSERVER_H__

#include "raknet/MessageIdentifiers.h"

#include "../core/Server.h"
#include "../core/Database.h"
#include "../core/Logger.h"
#include "../core/SessionManager.h"
#include "../core/packets/PacketHeader.h"
#include "packets/MinifigureList.h"
#include "packets/MinifigureCreate.h"

using namespace OpenUniverse::Core;

namespace OpenUniverse {
namespace World {
class WorldServer : public Server {
private:
    SessionManager* sessions;
    Database* db;
    Logger* logger;

    void handlePacket(RakNet::BitStream*, Packet*);
    void serverStarted();
    void serverStartFailed();

    void handleCharList(RakNet::BitStream*, Packet*);
    void handleCharCreate(RakNet::BitStream*, Packet*);

public:
    WorldServer(SessionManager*, Database*);

    ~WorldServer();
};
}
}

#endif
