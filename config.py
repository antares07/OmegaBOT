from configparser import ConfigParser

# Import token from ini file
def token():
    config = ConfigParser()
    config.read('token.ini')
    token = config["discord"]["token"]
    return token