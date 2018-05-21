#include "Logger.h"

namespace OpenUniverse {
namespace Core {
Logger::Logger(std::string str) : name(str)
{
}

Logger::~Logger()
{
}

// FIXME: add colors to these
void Logger::info(std::string str)
{
    auto log = "[" + name + "] (INF) " + str;

    std::cout << "<" << std::this_thread::get_id() << "> " << log << std::endl;
}

void Logger::warn(std::string str)
{
    auto log = "[" + name + "] (WRN) " + str;

    std::cout << "<" << std::this_thread::get_id() << "> " << log << std::endl;
}

void Logger::error(std::string str)
{
    auto log = "[" + name + "] (ERR) " + str;

    std::cout << "<" << std::this_thread::get_id() << "> " << log << std::endl;
}
}
}
