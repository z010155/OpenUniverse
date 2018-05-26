#include "Database.h"

namespace OpenUniverse {
namespace Core {
Database::Database(std::string connStr)
{
    conn = new pqxx::connection(connStr);

    conn->prepare("create_account", "INSERT INTO accounts VALUES ($1, $2, $3)");
    conn->prepare("create_character", "INSERT INTO characters (id, name, unnaproved_name, account, shirt_color, shirt_style, pants_color, hair_style, hair_color, lh, rh, eyebrow_style, eye_style, mouth_style) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)");
    conn->prepare("get_accounts_name", "SELECT * FROM accounts WHERE username = $1");
    conn->prepare("get_accounts_id", "SELECT * FROM accounts WHERE id = $1");
    conn->prepare("get_characters_account", "SELECT * FROM characters WHERE account = $1");
    conn->prepare("get_characters_id", "SELECT * FROM characters WHERE id = $1");
}

Database::~Database()
{
    delete conn;
}

void Database::createAccount(std::string username, std::string password)
{
    std::mt19937 rng;
    rng.seed(std::random_device()());
    std::uniform_int_distribution<std::mt19937::result_type> generator(1000000000000000000u, 9223372036854775807u);

    uint64_t id = generator(rng);

    char hashed[crypto_pwhash_STRBYTES];

    if (crypto_pwhash_str(hashed, password.c_str(), password.length(), crypto_pwhash_OPSLIMIT_SENSITIVE, crypto_pwhash_MEMLIMIT_SENSITIVE))
        throw std::runtime_error("Out of memory");

    pqxx::transaction<> t(*conn);

    t.exec_prepared("create_account", id, username, hashed);
    t.commit();
}

void Database::createCharacter(DB::Account* account, std::string name, uint32_t predef1, uint32_t predef2,
                               uint32_t predef3, uint32_t shirtColor, uint32_t shirtStyle, uint32_t pantsColor,
                               uint32_t hairStyle, uint32_t hairColor, uint32_t lh, uint32_t rh, uint32_t eyebrowStyle,
                               uint32_t eyeStyle, uint32_t mouthStyle)
{
    std::mt19937 rng;
    rng.seed(std::random_device()());
    std::uniform_int_distribution<std::mt19937::result_type> generator(1000000000000000000u, 9223372036854775807u);
    pqxx::transaction<> t(*conn);

    std::ifstream firstStream;
    std::ifstream middleStream;
    std::ifstream lastStream;

    firstStream.open("assets/names/minifigname_first.txt");
    middleStream.open("assets/names/minifigname_middle.txt");
    lastStream.open("assets/names/minifigname_last.txt");

    std::string first;
    std::string middle;
    std::string last;

    firstStream >> first;
    middleStream >> middle;
    lastStream >> last;

    auto firstParts = Utils::split(first, "\n");
    auto middleParts = Utils::split(middle, "\n");
    auto lastParts = Utils::split(last, "\n");

    auto predefName = firstParts[predef1] + middleParts[predef2] + lastParts[predef3];

    t.exec_prepared("create_character", generator(rng), predefName, name, account->id, shirtColor, shirtStyle, pantsColor, hairStyle, hairColor, lh, rh, eyebrowStyle, eyeStyle, mouthStyle);
    t.commit();
}

DB::Account* Database::authenticate(std::string username, std::string password)
{
    auto account = getAccount(username);

    if (!account || crypto_pwhash_str_verify(account->password.c_str(), password.c_str(), password.length()))
        return NULL;

    return account;
}

DB::Account* Database::getAccount(std::string username)
{
    pqxx::transaction<> t(*conn);

    auto account = new DB::Account();
    auto res = t.exec_prepared("get_accounts_name", username);

    if (res.size()) {
        auto user = res[0];

        account->id = user[0].as<uint64_t>();
        account->username = user[1].as<std::string>();
        account->password = user[2].as<std::string>();

        if (!user[3].is_null())
            account->character = user[3].as<uint64_t>();
    } else
        return NULL;

    return account;
}

DB::Account* Database::getAccount(uint64_t id)
{
    pqxx::transaction<> t(*conn);

    auto account = new DB::Account();
    auto res = t.exec_prepared("get_accounts_id", id);

    if (res.size()) {
        auto user = res[0];

        account->id = user[0].as<uint64_t>();
        account->username = user[1].as<std::string>();
        account->password = user[2].as<std::string>();

        if (!user[3].is_null())
            account->character = user[3].as<uint64_t>();
    } else
        return NULL;

    return account;
}

std::vector<DB::Character*> Database::getCharacters(std::string username)
{
    pqxx::transaction<> t(*conn);
    std::vector<DB::Character*> characters;
    auto account = getAccount(username);

    if (!account)
        return characters;

    auto res = t.exec_prepared("get_characters_account", account->id);

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
        auto emotes = row[16].as_array();
        auto visitedWorlds = row[17].as_array();
        auto items = row[18].as_array();
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

        character->emotes = std::vector<unsigned int>();
        character->visitedWorlds = std::vector<uint16_t>();
        character->items = std::vector<uint32_t>();

        std::pair<pqxx::array_parser::juncture, std::string> emote = emotes.get_next();

        while (emote.first != pqxx::array_parser::juncture::done) {
            char* base;
            unsigned int id = strtol(emote.second.c_str(), &base, 0);

            character->emotes.push_back(id);

            emote = emotes.get_next();
        }

        std::pair<pqxx::array_parser::juncture, std::string> world = visitedWorlds.get_next();

        while (world.first != pqxx::array_parser::juncture::done) {
            char* base;
            uint16_t id = strtol(world.second.c_str(), &base, 0);

            character->visitedWorlds.push_back(id);

            world = visitedWorlds.get_next();
        }

        std::pair<pqxx::array_parser::juncture, std::string> item = items.get_next();

        while (item.first != pqxx::array_parser::juncture::done) {
            char* base;
            uint32_t id = strtol(item.second.c_str(), &base, 0);

            character->items.push_back(id);

            item = items.get_next();
        }

        characters.push_back(character);
    }

    return characters;
}

DB::Character* Database::getCharacter(int64_t id)
{
    pqxx::transaction<> t(*conn);
    auto res = t.exec_prepared("get_accounts_id", id);

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
    auto emotes = row[16].as_array();
    auto visitedWorlds = row[17].as_array();
    auto items = row[18].as_array();
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

    character->emotes = std::vector<unsigned int>();
    character->visitedWorlds = std::vector<uint16_t>();
    character->items = std::vector<uint32_t>();

    std::pair<pqxx::array_parser::juncture, std::string> emote = emotes.get_next();

    while (emote.first != pqxx::array_parser::juncture::done) {
        char* base;
        unsigned int id = strtol(emote.second.c_str(), &base, 0);

        character->emotes.push_back(id);

        emote = emotes.get_next();
    }

    std::pair<pqxx::array_parser::juncture, std::string> world = visitedWorlds.get_next();

    while (world.first != pqxx::array_parser::juncture::done) {
        char* base;
        uint16_t id = strtol(world.second.c_str(), &base, 0);

        character->visitedWorlds.push_back(id);

        world = visitedWorlds.get_next();
    }

    std::pair<pqxx::array_parser::juncture, std::string> item = items.get_next();

    while (item.first != pqxx::array_parser::juncture::done) {
        char* base;
        uint32_t id = strtol(item.second.c_str(), &base, 0);

        character->items.push_back(id);

        item = items.get_next();
    }

    return character;
}
}
}
