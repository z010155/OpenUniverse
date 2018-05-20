#ifndef __LU_SERIALIZABLE_H__
#define __LU_SERIALIZABLE_H__

#include "raknet/BitStream.h"

namespace OpenUniverse {
namespace Core {
class Serializable {
public:
    virtual ~Serializable() {}

    virtual void serialize(RakNet::BitStream*) = 0;

    static Serializable* deserialize(RakNet::BitStream*);
};
}
}

#endif
