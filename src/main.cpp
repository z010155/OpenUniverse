#include <iostream>
#include <thread>
#include <vector>
#include <string>

#include "auth/AuthServer.h"
#include "core/Database.h"

using Server = OpenUniverse::Core::Server;
using AuthServer = OpenUniverse::Auth::AuthServer;
using Database = OpenUniverse::Core::Database;

int main()
{
    Database* db = new Database("dbname=openuniverse user=root password=root");

    std::vector<Server*> servers;
    std::vector<std::thread*> threads;

    servers.push_back(new AuthServer(db));

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
        std::cout << "> ";
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
