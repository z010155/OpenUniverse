#ifndef __LU_LOGGER_H__
#define __LU_LOGGER_H__

#include <string>
#include <iostream>
#include <thread>

namespace OpenUniverse {
namespace Core {
class Logger {
private:
    std::string name;

    std::string getTime();

public:
    Logger(std::string);
    virtual ~Logger();

    void info(std::string);
    void error(std::string);
    void warn(std::string);
};
}
}

#endif
