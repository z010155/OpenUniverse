#ifndef __LU_SERVER_H__
#define __LU_SERVER_H__

#ifdef _WIN32
#include <process.h>
#define getpid _getpid
#else
#include <unistd.h>
#endif

#include "raknet/BitStream.h"
#include "raknet/RakSleep.h"
#include "raknet/RakNetworkFactory.h"
#include "raknet/RakPeerInterface.h"

#include "LUPacket.h"
#include "packets/Handshake.h"

namespace OpenUniverse {
namespace Core {
class Server {
protected:
    int port;
    bool active = false;

    RakPeerInterface* server;

    void makeHandshake(RakNet::BitStream*, Packet*, int);

    virtual void handlePacket(RakNet::BitStream*, Packet*) = 0;
    virtual void serverStarted() = 0;
    virtual void serverStartFailed() = 0;

public:
    virtual ~Server() {}

    void start();
    void stop();
    void send(LUPacket*, SystemAddress, bool);
};
}
}

#endif
