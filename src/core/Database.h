#ifndef __LU_DATABASE_H__
#define __LU_DATABASE_H__

#include <sodium/crypto_pwhash.h>
#include <pqxx/pqxx>

#include <string>
#include <exception>
#include <random>
#include <vector>
#include <fstream>

#include "Utils.h"
#include "db/Account.h"
#include "db/Character.h"

namespace OpenUniverse {
namespace Core {
class Database {
private:
    pqxx::connection* conn;

public:
    Database(std::string);

    ~Database();

    void createAccount(std::string, std::string);
    void createCharacter(DB::Account*, std::string, uint32_t, uint32_t, uint32_t, uint32_t, uint32_t, uint32_t,
                         uint32_t, uint32_t, uint32_t, uint32_t, uint32_t, uint32_t, uint32_t);

    DB::Account* authenticate(std::string, std::string);
    DB::Account* getAccount(std::string);
    DB::Account* getAccount(uint64_t);

    std::vector<DB::Character*> getCharacters(std::string);
    DB::Character* getCharacter(int64_t);
};
}
}

#endif
