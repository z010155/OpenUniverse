#include "SessionManager.h"

namespace OpenUniverse {
namespace Core {
SessionManager::SessionManager()
{
    sessions = std::map<SystemAddress, DB::Account*>();
}

SessionManager::~SessionManager()
{
}

void SessionManager::addSession(SystemAddress address, DB::Account* account)
{
    sessions[address] = account;
}

DB::Account* SessionManager::getSession(SystemAddress address)
{
    if (sessions.find(address) == sessions.end())
        return NULL;

    return sessions[address];
}
}
}
