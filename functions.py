import discord
import sqlite3
from SirenBot import *
from typing import Literal
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
    Gets general_logs from config.env
    rtype: int
    """
    general_logs_str = os.getenv('GENERAL_LOGS')
    try:
        general_logs_id = int(general_logs_str)
    except:
        general_logs_id = 0
    return general_logs_id

def get_critical_logs():
    """
    Gets critical_logs from config.env
    rtype: int
    """
    critical_logs_str = os.getenv('CRITICAL_LOGS')
    try:
        critical_logs_id = int(critical_logs_str)
    except:
        critical_logs_id = 0
    return critical_logs_id


def get_mega_alert_logs():
    """
    Gets mega_alert_logs from config.env
    rtype: int
    """
    mega_alert_logs_str = os.getenv('MEGA_ALERT_LOGS')
    try:
        mega_alert_logs_id = int(mega_alert_logs_str)
    except:
        mega_alert_logs_id = 0
    return mega_alert_logs_id

def get_bot_owner():
    """
    Gets bot_owner from config.env
    rtype: int
    """
    bot_owner_str = os.getenv('BOT_OWNER')
    try:
        bot_owner_id = int(bot_owner_str)
    except:
        bot_owner_id = 0
    return bot_owner_id


"""JSON"""
def load_json(filename):
    """
    Loads a json file, wow
    """
    with open(filename, encoding='utf-8') as infile:
        return json.load(infile)

def update_webhook_tokens_json(name:Literal['mega_alerts', 'critical', 'general'], webhook_token_url):
    """
    Changes a token in webhook_tokens.json
    rtype: bool
    """

    try: 
        with open('SF-SirenBot/webhook_tokens.json', encoding='utf-8') as infile:
            obj = json.load(infile)

        obj[str(name)] = str(webhook_token_url)
        
        with open('SF-SirenBot/webhook_tokens.json', 'w') as outfile:
            json.dump(obj, outfile, ensure_ascii=True, indent=4)
        return True
    except Exception as e:
        print(e)
        return False

async def send_webhook_embed(name:Literal['mega_alerts', 'critical', 'general'], embed_obj):
    """
    Sends an embed through a webhook of choice.
    rtype: bool
    """
    try: 
        with open('SF-SirenBot/webhook_tokens.json', encoding='utf-8') as infile:
            f = json.load(infile)

        webhook_url = None
        if name == 'mega_alerts':
            webhook_url = f['mega_alerts']
        if name == 'critical':
            webhook_url = f['critical']
        if name == 'general':
            webhook_url = f['general']

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=webhook_url, session=session)
            await webhook.send(embed=embed_obj)
            await session.close()

        return True
            
    except Exception as e:
        print(e)
        return False
    
    
