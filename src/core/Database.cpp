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
    delete w;
    delete conn;
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

        if (user.size() > 3)
            account->character = user[3].as<uint64_t>();
    } else
        return NULL;

    return account;
}

DB::Account* Database::getAccount(uint64_t id)
{
    auto account = new DB::Account();
    auto res = w->exec("SELECT * FROM accounts WHERE id = " + w->quote(id));

    if (res.size()) {
        auto user = res[0];

        account->id = user[0].as<uint64_t>();
        account->username = user[1].as<std::string>();
        account->password = user[2].as<std::string>();

        if (user.size() > 3)
            account->character = user[3].as<uint64_t>();
    } else
        return NULL;

    return account;
}

std::vector<DB::Character*> Database::getCharacters(std::string username)
{
    std::vector<DB::Character*> characters;
    auto account = getAccount(username);

    if (!account)
        return characters;

    auto res = w->exec("SELECT * FROM characters WHERE account = " + w->quote(account->id));

    for (auto row : res) {
        auto character = new DB::Character();

        character->id = row[0].as<int64_t>();
        character->name = row[1].as<std::string>();
        character->account = account;
        character->zone = row[3].as<uint16_t>();
        character->maxArmor = row[4].as<unsigned int>();
        character->armor = row[5].as<unsigned int>();
        character->maxHealth = row[6].as<unsigned int>();
        character->health = row[7].as<unsigned int>();
        character->maxImagination = row[9].as<unsigned int>();
        character->imagination = row[8].as<unsigned int>();
        character->isImmune = row[10].as<bool>();
        character->currency = row[11].as<unsigned int>();
        character->isFreeToPlay = row[12].as<bool>();
        character->gmLevel = row[13].as<unsigned int>();
        character->luScore = row[14].as<unsigned int>();
        character->playtime = row[15].as<uint64_t>();
        // character->emotes = row[16].as<std::vector<unsigned int>>();
        // character->visitedWorlds = row[17].as<std::vector<uint16_t>>();
        // character->items = row[18].as<std::vector<uint32_t>>();
        character->level = row[19].as<unsigned int>();

        character->eyebrowStyle = row[20].as<uint32_t>();
        character->eyeStyle = row[21].as<uint32_t>();
        character->hairColor = row[22].as<uint32_t>();
        character->hairStyle = row[23].as<uint32_t>();
        character->pantsColor = row[24].as<uint32_t>();
        character->mouthStyle = row[25].as<uint32_t>();
        character->shirtColor = row[26].as<uint32_t>();
        character->shirtStyle = row[27].as<uint32_t>();
        character->lh = row[28].as<uint32_t>();
        character->rh = row[29].as<uint32_t>();

        characters.push_back(character);
    }

    return characters;
}

DB::Character* Database::getCharacter(int64_t id)
{
    auto res = w->exec("SELECT * FROM characters WHERE id = " + w->quote(id));

    if (!res.size())
        return NULL;

    auto row = res[0];

    auto character = new DB::Character();
    auto account = getAccount(row[2].as<uint64_t>());

    character->id = row[0].as<int64_t>();
    character->name = row[1].as<std::string>();
    character->account = account;
    character->zone = row[3].as<uint16_t>();
    character->maxArmor = row[4].as<unsigned int>();
    character->armor = row[5].as<unsigned int>();
    character->maxHealth = row[6].as<unsigned int>();
    character->health = row[7].as<unsigned int>();
    character->maxImagination = row[8].as<unsigned int>();
    character->imagination = row[9].as<unsigned int>();
    character->isImmune = row[10].as<bool>();
    character->currency = row[11].as<unsigned int>();
    character->isFreeToPlay = row[12].as<bool>();
    character->gmLevel = row[13].as<unsigned int>();
    character->luScore = row[14].as<unsigned int>();
    character->playtime = row[15].as<uint64_t>();
    // character->emotes = row[16].as<unsigned int>();
    // character->visitedWorlds = row[17].as<std::vector<uint16_t>>();
    // character->items = row[18].as<std::vector<uint32_t>>();
    character->level = row[19].as<unsigned int>();

    character->eyebrowStyle = row[20].as<uint32_t>();
    character->eyeStyle = row[21].as<uint32_t>();
    character->hairColor = row[22].as<uint32_t>();
    character->hairStyle = row[23].as<uint32_t>();
    character->pantsColor = row[24].as<uint32_t>();
    character->mouthStyle = row[25].as<uint32_t>();
    character->shirtColor = row[26].as<uint32_t>();
    character->shirtStyle = row[27].as<uint32_t>();
    character->lh = row[28].as<uint32_t>();
    character->rh = row[29].as<uint32_t>();

    return character;
}
}
}
