import discord
import sqlite3
from SirenBot import *

"""OTHER"""
def get_guild_id():
    """
    Gets guild_id from sirenDB.db
    rtype: int
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT guild_id FROM guild_config;")
    guild_id = cursor.fetchone()[0]
    return guild_id

"""ROLES"""
def get_team_role():
    """
    Gets the team_role from sirenDB.db
    rtype: int
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT team_role FROM guild_config;")
    try:
        team_role = cursor.fetchone()[0]
    except Exception as e:
        team_role = None
        print(e)
    return team_role

def get_verified_role():
    """
    Gets the verified_role from sirenDB.db
    rtype: int
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT verified_role FROM guild_config;")
    try:
        verified_role = cursor.fetchone()[0]
    except Exception as e:
        verified_role = None
        print(e)
    return verified_role

"""CHANNELS"""
def get_gen_chat():
    """
    Gets the general_channel from sirenDB.db
    rtype: int
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT general_channel FROM guild_config;")
    try:
        general_channel = cursor.fetchone()[0]
    except Exception as e:
        general_channel = None
        print(e)
    return general_channel

def get_log_channel():
    """
    Gets the log_channel from sirenDB.db
    rtype: int
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT log_channel FROM guild_config;")
    try:
        log_channel = cursor.fetchone()[0]
    except Exception as e:
        log_channel = None
        print(e)
    return log_channel
