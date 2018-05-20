#include "Server.h"

namespace OpenUniverse {
namespace Core {
void Server::start()
{
    server = RakNetworkFactory::GetRakPeerInterface();

    server->SetIncomingPassword("3.25 ND1", 8);

    SocketDescriptor sockDescriptor(port, 0);

    if (server->Startup(8, 30, &sockDescriptor, 1)) {
        serverStarted();
        active = true;
    } else {
        serverStartFailed();
        active = false;
    }

    server->SetMaximumIncomingConnections(8);

    Packet* p;

    while (active) {
        p = server->Receive();

        if (!p)
            continue;

        RakNet::BitStream* stream = new RakNet::BitStream(p->data, p->length, false);

        handlePacket(stream, p);

        server->DeallocatePacket(p);

        RakSleep(30);
    }

    RakNetworkFactory::DestroyRakPeerInterface(server);
}

void Server::stop()
{
    active = false;
}

void Server::send(LUPacket* p, SystemAddress address, bool broadcast = false)
{
    auto stream = new RakNet::BitStream();

    p->serialize(stream);

    server->Send(stream, PacketPriority::SYSTEM_PRIORITY, PacketReliability::RELIABLE_ORDERED, 1, address, broadcast);
}

void Server::makeHandshake(RakNet::BitStream* stream, Packet* p, int remoteConnectionType = 4)
{
    auto handshake = Packets::Handshake::deserialize(stream);
    auto packet = new Packets::Handshake();

    packet->gameVersion = handshake->gameVersion;
    packet->remoteConnectionType = remoteConnectionType;
    packet->pid = getpid();

    send(packet, p->systemAddress);
}
}
}
