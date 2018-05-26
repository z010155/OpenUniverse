cmake_minimum_required(VERSION 2.8)

project(OpenUniverse CXX)

include(ExternalProject)

externalproject_add(libpqxx
                    SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include/libpqxx
                    CONFIGURE_COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/include/libpqxx/configure --prefix=<INSTALL_DIR> --disable-documentation
                    BUILD_COMMAND ${MAKE}
)

externalproject_get_property(libpqxx install_dir)
set(pqxx_dir ${install_dir})
unset(install_dir)

include_directories("include" "include/yaml-cpp/include" "include/libpqxx/include" "${pqxx_dir}/include")

add_subdirectory("include/raknet")
add_subdirectory("include/yaml-cpp")

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
    yaml-cpp
    ${pqxx_dir}/lib/libpqxx.a
    pq
    sodium
    pthread
)

add_executable(${PROJECT_NAME} ${OPENUNIVERSE_SOURCES})

target_link_libraries(${PROJECT_NAME} ${LIBS} m)
