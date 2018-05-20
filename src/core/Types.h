#ifndef __LU_TYPES_H__
#define __LU_TYPES_H__

namespace OpenUniverse {
namespace Core {
enum ConnectionType {
    GENERAL = 0,
    AUTH = 1,
    CLIENT = 4,
    SERVER = 5,
};

enum AuthPacket {
    LOGIN_INFO = 0,
};

enum ClientPacket {
    USER_SESSION_INFO = 0x01,
    MINIFIGURE_LIST_REQUEST = 0x02,
    MINIFIGURE_CREATE_REQUEST = 0x03,
    JOIN_WORLD = 0x04,
    CLIENT_GAME_MESSAGE = 0x05,
    MINIFIGURE_DELETE_REQUEST = 0x06,
    MINIFIGURE_RENAME_REQUEST = 0x07,
    CHAT_MESSAGE = 0x0e,
    CLIENTSIDE_LOAD_COMPLETE = 0x13,
    ROUTED_PACKET = 0x15,
    POSITION_UPDATE = 0x16,
    MAIL = 0x17,
    WHITELIST_REQUEST = 0x19,
    MODEL_PREVIEW_REQUEST = 0x1b,
    HANDLE_FUNNESS = 0x1e,
    REQUEST_FREE_TRIAL_REFRESH = 0x20,
    UGC_DOWNLOAD_FAILED = 0x78,
};
}
}

#endif
