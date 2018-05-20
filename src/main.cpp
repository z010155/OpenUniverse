#include <iostream>
#include <thread>
#include <vector>
#include <string>

#include "auth/AuthServer.h"

using Server = OpenUniverse::Core::Server;
using AuthServer = OpenUniverse::Auth::AuthServer;

int main()
{
    std::vector<Server*> servers;
    std::vector<std::thread*> threads;

    servers.push_back(new AuthServer());

    for (auto server : servers) {
        auto serverThread = new std::thread([server]()
        {
            server->start();
        });

        serverThread->detach();

        threads.push_back(serverThread);
    }

    auto quit = false;

    while (!quit) {
        std::string input;
        std::cin >> input;

        // FIXME: add a command framework

        if (input == "quit") {
            for (auto server : servers) {
                server->stop();
            }

            quit = true;
        }
    }

    return 0;
}
