import os
import sys

def get_config_path(file_name):
    # Get the directory of the current script
    commands_dir = os.path.dirname(sys.argv[0])
    
    # Construct the path to config.json
    config_path = os.path.join(commands_dir, "..", "OmegaBOT", file_name)
    
    # Verify if the file exists
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"The configuration file '{os.path.basename(config_path)}' does not exist."
        )
    
    return config_path

def guild_id():

    import discord
    import json

    with open("config.json") as file:
        guild_id = discord.Object(id=json.load(file)["guild_id"])

    return guild_id