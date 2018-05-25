#ifndef __LU_SESSIONMANAGER_H__
#define __LU_SESSIONMANAGER_H__

#include <map>

#include "raknet/RakNetTypes.h"

#include "db/Account.h"

namespace OpenUniverse {
namespace Core {
class SessionManager {
private:
    std::map<SystemAddress, DB::Account*> sessions;

public:
    SessionManager();

    virtual ~SessionManager();

    void addSession(SystemAddress, DB::Account*);
    DB::Account* getSession(SystemAddress);
};
}
}

#endif
