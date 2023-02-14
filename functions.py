import discord
import sqlite3
from SirenBot import *
from dotenv import load_dotenv

load_dotenv('SF-SirenBot/config.env') 

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
def get_admin_role():
    """
    Gets the admin_role from sirenDB.db
    rtype: int
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT admin_role FROM guild_config;")
    try:
        admin_role = cursor.fetchone()[0]
    except Exception as e:
        admin_role = None
        print(e)
    return admin_role

def get_mod_role():
    """
    Gets the mod_role from sirenDB.db
    rtype: int
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT mod_role FROM guild_config;")
    try:
        mod_role = cursor.fetchone()[0]
    except Exception as e:
        mod_role = None
        print(e)
    return mod_role

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

"""config.env FUNCTIONS"""
def get_general_logs():
    """
    gets general_logs from config.env
    rtype: int
    """
    general_logs_str = os.getenv('GENERAL_LOGS')
    try:
        general_logs_id = int(general_logs_id)
    except:
        general_logs_id = 0
    return general_logs_id

def get_critical_logs():
    """
    gets critical_logs from config.env
    rtype: int
    """
    critical_logs_str = os.getenv('CRITICAL_LOGS')
    try:
        critical_logs_id = int(critical_logs_id)
    except:
        critical_logs_id = 0
    return critical_logs_id

def get_mega_alert_logs():
    """
    gets mega_alert_logs from config.env
    rtype: int
    """
    mega_alert_logs_str = os.getenv('MEGA_ALERT_LOGS')
    try:
        mega_alert_logs_id = int(mega_alert_logs_id)
    except:
        mega_alert_logs_id = 0
    return mega_alert_logs_id


    