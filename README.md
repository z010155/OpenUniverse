![logo.png](.github/logo.png)

# OpenUniverse

An open-source LEGO Universe server.

## Requirements

- **PostgreSQL** for the database
- **Redis** for the session cache
- **Python 3.6** to run the actual program

## Running

### Installing the dependencies

#### PostgreSQL

##### Windows users

Use one of the [installers for windows](https://www.postgresql.org/download/windows/).

##### Linux users

Use your package manager to install PostgreSQL.

On Debian/Ubuntu for example:

```sh
$ sudo apt install postgresql
```

##### MacOS users

Install the [Homebrew package manager](https://brew.sh) and run the following in a terminal:

```sh
$ brew install postgresql
```

#### Redis

##### Windows

On Windows 10 you can use the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) to run Redis (see the linux example on how to install), or you can install [Redis for Windows](https://github.com/MicrosoftArchive/redis/releases/tag/win-3.2.100)

##### Linux/Windows Subsystem for Linux

Again, use your package manager to install Redis

For example:

```sh
$ sudo apt install redis-server
```

##### MacOS

```sh
$ brew install redis
```

#### Python 3.6

##### Windows

Use the [Python installer for windows](https://python.org).

##### Linux

Same here, use your package manager.

Example:

```sh
$ sudo apt install python3 python3-pip
# might be python3.6 and python3.6-pip
```

##### MacOS

```sh
$ brew install python3
```

#### PyPi packages

```sh
$ pip3 install -Ur requirements.txt
# you might need a C/C++ compiler installed to build some dependencies
```

### Creating the database

#### Windows

```cmd
C:\Users\User> "C:\Program Files\PostgreSQL\10\bin\createdb.exe" -Upostgres openlu
# use the password you set
```

#### *nix

```sh
$ createdb openlu
```

### Starting Redis

#### Windows

Redis for Windows should automatically start a Redis daemon, you probably won't have to do anything.

#### *nix/Windows Subsystem for Linux

```sh
$ redis-server
```

### Running it

```sh
$ python main.py
# might be py, python3 or python3.6 on your system, check output with the '-V' flag
```

## Questions

If you have any questions, just send me a message on Discord. (noud02#0080)

## Related projects

- [PyLUS](https://github.com/Knightoffaith/PyLUS)
- [WLUS](https://github.com/wesleyd1124/WLUS)

## Contributing

Contributions are always welcome!

## License

OpenUniverse is licensed under the MIT license.

## Disclaimer

The LEGO Group has not endorsed or authorized the operation of this game and is not liable for any safety issues in relation to its operation.
