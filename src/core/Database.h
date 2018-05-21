#ifndef __LU_DATABASE_H__
#define __LU_DATABASE_H__

#include <sodium/crypto_pwhash_argon2i.h>
#include <pqxx/pqxx>

#include <string>
#include <exception>
#include <random>

#include "db/Account.h"

namespace OpenUniverse {
namespace Core {
class Database {
private:
    pqxx::connection* conn;
    pqxx::work* w;

public:
    Database(std::string);

    virtual ~Database();

    void createAccount(std::string, std::string);

    DB::Account* authenticate(std::string, std::string);
    DB::Account* getAccount(std::string);
};
}
}

#endif
