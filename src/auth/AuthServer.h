#ifndef __LU_AUTHSERVER_H__
#define __LU_AUTHSERVER_H__

#include "raknet/MessageIdentifiers.h"

#include "../core/Server.h"
#include "../core/Types.h"
#include "../core/Logger.h"
#include "../core/Database.h"
#include "../core/db/Account.h"
#include "../core/packets/PacketHeader.h"
#include "../core/packets/Handshake.h"

#include "packets/LoginInfo.h"

using namespace OpenUniverse::Core;

namespace OpenUniverse {
namespace Auth {
class AuthServer : public Server {
private:
    Logger* logger;
    Database* db;

    void handlePacket(RakNet::BitStream*, Packet*);
    void serverStarted();
    void serverStartFailed();

    void handleLoginPacket(RakNet::BitStream*, Packet*);

public:
    AuthServer(Database*);

    virtual ~AuthServer();
};
}
}

#endif
