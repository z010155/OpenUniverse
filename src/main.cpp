#include <iostream>
#include <thread>
#include <vector>
#include <string>

#include <yaml-cpp/yaml.h>

#include "auth/AuthServer.h"
#include "world/WorldServer.h"
#include "core/Database.h"

using Server = OpenUniverse::Core::Server;
using AuthServer = OpenUniverse::Auth::AuthServer;
using WorldServer = OpenUniverse::World::WorldServer;
using Database = OpenUniverse::Core::Database;

int main()
{
    auto cfg = YAML::LoadFile("config.yml");
    auto dbConf = cfg["db"].as<YAML::Node>();

    auto database = dbConf["database"].as<std::string>();
    auto user = dbConf["user"].as<std::string>();
    auto password = dbConf["password"].as<std::string>();

    auto db = new Database("dbname=" + database + " user=" + user + " password=" + password);

    std::vector<Server*> servers;
    std::vector<std::thread*> threads;

    servers.push_back(new AuthServer(db));
    servers.push_back(new WorldServer(db));

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
