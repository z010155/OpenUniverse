#include "Database.h"

namespace OpenUniverse {
namespace Core {
Database::Database(std::string connStr)
{
    conn = new pqxx::connection(connStr);
    w = new pqxx::work(*conn);
}

Database::~Database()
{
}

void Database::createAccount(std::string username, std::string password)
{
    std::mt19937 rng;
    rng.seed(std::random_device()());
    std::uniform_int_distribution<std::mt19937::result_type> generator(1000000000000000000u, 9999999999999999999u);

    uint64_t id = generator(rng);

    char hashed[crypto_pwhash_argon2i_STRBYTES];

    if (crypto_pwhash_argon2i_str(hashed, password.c_str(), password.length(), crypto_pwhash_argon2i_OPSLIMIT_SENSITIVE, crypto_pwhash_argon2i_MEMLIMIT_SENSITIVE))
        throw std::runtime_error("Out of memory");

    w->exec("INSERT INTO accounts VALUES (" + w->quote(id) + "," + w->quote(username) + "," + w->quote(hashed) + ")");
}

DB::Account* Database::authenticate(std::string username, std::string password)
{
    auto account = getAccount(username);

    if (!account || crypto_pwhash_argon2i_str_verify(account->password.c_str(), password.c_str(), password.length()))
        return NULL;

    return account;
}

DB::Account* Database::getAccount(std::string username)
{
    auto account = new DB::Account();

    auto res = w->exec("SELECT * FROM accounts WHERE username = " + w->quote(username));

    if (res.size()) {
        auto user = res[0];

        account->id = user[0].as<uint64_t>();
        account->username = user[1].as<std::string>();
        account->password = user[2].as<std::string>();

        if (res.size() > 3)
            account->character = user[3].as<uint64_t>();
    } else
        return NULL;

    return account;
}
}
}
