cmake_minimum_required(VERSION 2.6)

project(OpenUniverse CXX)

include_directories("include/raknet")
add_subdirectory("include/raknet")

set(OPENUNIVERSE_SOURCES
    src/main.cpp

    src/core/LUPacket.cpp
    src/core/Server.cpp
    src/core/Utils.cpp
    src/core/packets/PacketHeader.cpp
    src/core/packets/Handshake.cpp

    src/auth/AuthServer.cpp
    src/auth/packets/LoginInfo.cpp
)

set(LIBS
    RakNet
    pthread
)

add_executable(${PROJECT_NAME} ${OPENUNIVERSE_SOURCES})

target_link_libraries(${PROJECT_NAME} ${LIBS} m)
