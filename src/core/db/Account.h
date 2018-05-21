#ifndef __LU_DB_USER_H__
#define __LU_DB_USER_H__

#include <string>

namespace OpenUniverse {
namespace Core {
namespace DB {
struct Account {
public:
    uint64_t id;
    std::string username;
    std::string password;
    uint16_t zone;
    uint64_t character;
};
}
}
}

#endif
