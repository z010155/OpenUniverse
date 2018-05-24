#ifndef __LU_DB_CHARACTER_H__
#define __LU_DB_CHARACTER_H__

#include <string>
#include <vector>

#include "Account.h"

namespace OpenUniverse {
namespace Core {
namespace DB {
struct Character {
public:
    int64_t id;
    std::string name;
    Account* account;
    uint16_t zone;

    unsigned int maxArmor;
    unsigned int armor;
    unsigned int maxHealth;
    unsigned int health;
    unsigned int imagination;
    unsigned int maxImagination;
    bool isImmune;
    unsigned int currency;
    bool isFreeToPlay;
    unsigned int gmLevel;
    unsigned int luScore;
    uint64_t playtime;
    unsigned int level;
    std::vector<unsigned int> emotes;
    std::vector<uint16_t> visitedWorlds;
    std::vector<uint32_t> items;

    uint32_t eyebrowStyle;
    uint32_t eyeStyle;
    uint32_t hairColor;
    uint32_t hairStyle;
    uint32_t pantsColor;
    uint32_t mouthStyle;
    uint32_t shirtColor;
    uint32_t shirtStyle;
    uint32_t lh;
    uint32_t rh;
};
}
}
}

#endif
