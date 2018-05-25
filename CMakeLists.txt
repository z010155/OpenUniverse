cmake_minimum_required(VERSION 2.6)

project(OpenUniverse CXX)

include_directories("include")
add_subdirectory("include/raknet")

set(OPENUNIVERSE_SOURCES
    src/main.cpp

    src/core/LUPacket.cpp
    src/core/Server.cpp
    src/core/Utils.cpp
    src/core/Logger.cpp
    src/core/Database.cpp
    src/core/SessionManager.cpp
    src/core/packets/PacketHeader.cpp
    src/core/packets/Handshake.cpp

    src/auth/AuthServer.cpp
    src/auth/packets/LoginInfo.cpp

    src/world/WorldServer.cpp
    src/world/packets/MinifigureList.cpp
    src/world/packets/MinifigureCreate.cpp
)

set(LIBS
    RakNet
    pqxx
    pq
    sodium
    pthread
    yaml-cpp
)

add_executable(${PROJECT_NAME} ${OPENUNIVERSE_SOURCES})

target_link_libraries(${PROJECT_NAME} ${LIBS} m)
