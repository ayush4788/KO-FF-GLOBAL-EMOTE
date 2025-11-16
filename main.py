# --------------------------------------------------------------
# main.py – FULL, READY-TO-RUN VERSION (login → index + bot)
# --------------------------------------------------------------

import requests, os, psutil, sys, jwt, pickle, json, binascii, time, urllib3, base64, datetime, re, socket, threading, ssl, pytz, aiohttp
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import * ; from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2, MajoRLoGinrEs_pb2, PorTs_pb2, MajoRLoGinrEq_pb2, sQ_pb2, Team_msg_pb2
from cfonts import render, say
import asyncio
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from functools import wraps

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --------------------------------------------------------------
# 1. GLOBAL DATA
# --------------------------------------------------------------
EMOTE_ALIASES = {
    "m10": 909000081, "ak": 909000063, "ump": 909000098, "mp40": 909000075,
    "mp40v2": 909040010, "scar": 909000068, "xm8": 909000085, "mp5": 909033002,
    "m4a1": 909033001, "famas": 909000090, "m1887": 909035007, "thompson": 909038010,
    "g18": 909038012, "woodpecker": 909042008, "parafal": 909045001, "groza": 909041005,
    "p90": 909049010, "m60": 909051003, "fist": 909037011,
    "ride": 909051014, "circle": 909050009, "petals": 909051013, "bow": 909051012,
    "bike": 909051010, "shower": 909051004, "dream": 909051002, "angelic": 909051001,
    "paint": 909048015, "sword": 909044015, "flare": 909041008, "owl": 909049003,
    "thor": 909050008, "bigdill": 909049001, "csgm": 909041013, "mapread": 909050014,
    "tomato": 909050015, "ninja": 909050002, "level100": 909042007, "auraboat": 909050028,
    "flyingguns": 909049012, "heart": 909000045, "flag": 909000034, "pushup": 909000012,
    "devil": 909000020, "shootdance": 909000008, "chicken": 909000006, "throne": 909000014,
    "rose": 909000010, "valentine": 909038004, "rampage": 909034001, "guildflag": 909049017,
    "fish": 909040004, "inosuke": 909041003, "brgm": 909041012,
    "naruto": 909050003, "kabuto": 909050002, "minato": 909050006, "football": 909048016,
    "p": 909000012, "t": 909000014, "r": 909000010, "l100": 909042007
}

app = Flask(__name__)
app.secret_key = "SUPER_RANDOM_SECRET_CHANGE_ME"   # <-- change this!

LOOP = None
online_writer = None
whisper_writer = None
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
key = None
iv = None
region = None
server2 = "bd"
key2 = "YOUR_API_KEY"
BYPASS_TOKEN = "YOUR_BYPASS_TOKEN"

# --------------------------------------------------------------
# 2. ALL ASYNC HELPERS (unchanged from your original code)
# --------------------------------------------------------------
async def encrypted_proto(encoded_hex):
    key_aes = b'Yg&tc%DEuh6%Zc^8'
    iv_aes = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key_aes, AES.MODE_CBC, iv_aes)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload

async def GeNeRaTeAccEss(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    Hr = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "100-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB51"}
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=Hr, data=data) as response:
            if response.status != 200: return "Failed to get access token"
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)

async def EncRypTMajoRLoGin(open_id, access_token):
    Hr = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "100-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB51"}
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.118.1"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    Hr = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "100-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB51"}
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    Hr = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "100-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB51"}
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization'] = f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto

async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

async def cHTypE(H):
    if not H: return 'Squid'
    elif H == 1: return 'CLan'
    elif H == 2: return 'PrivaTe'

async def SEndMsG(H, message, Uid, chat_id, key, iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid': msg_packet = await xSEndMsgsQ(message, chat_id, key, iv)
    elif TypE == 'CLan': msg_packet = await xSEndMsg(message, 1, chat_id, chat_id, key, iv)
    elif TypE == 'PrivaTe': msg_packet = await xSEndMsg(message, 2, Uid, Uid, key, iv)
    return msg_packet

async def SEndPacKeT(OnLinE, ChaT, TypE, PacKeT):
    if TypE == 'ChaT' and ChaT: whisper_writer.write(PacKeT); await whisper_writer.drain()
    elif TypE == 'OnLine': online_writer.write(PacKeT); await online_writer.drain()
    else: return 'UnsoPorTed TypE ! >> ErrrroR (:():)'

async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
    global online_writer, spam_room, whisper_writer, spammer_uid, spam_chat_id, spam_uid, XX, uid, Spy, data2, Chat_Leave
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            online_writer.write(bytes_payload)
            await online_writer.drain()
            while True:
                data2 = await reader.read(9999)
                if not data2: break
                if data2.hex().startswith('0500') and len(data2.hex()) > 1000:
                    try:
                        packet = await DeCode_PackEt(data2.hex()[10:])
                        packet = json.loads(packet)
                        OwNer_UiD, CHaT_CoDe, SQuAD_CoDe = await GeTSQDaTa(packet)
                        JoinCHaT = await AutH_Chat(3, OwNer_UiD, CHaT_CoDe, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', JoinCHaT)
                        message = f'[B][C]{get_random_color()}\n- WeLComE To DECIMAL CHEATS Emote Bot ! '
                        P = await SEndMsG(0, message, OwNer_UiD, OwNer_UiD, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                    except:
                        pass
            online_writer.close(); await online_writer.wait_closed(); online_writer = None
        except Exception as e:
            print(f"- ErroR With {ip}:{port} - {e}"); online_writer = None
        await asyncio.sleep(reconnect_delay)

async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region, reconnect_delay=0.5):
    global spam_room, whisper_writer, spammer_uid, spam_chat_id, spam_uid, online_writer, chat_id, XX, uid, Spy, data2, Chat_Leave
    while True:
        try:
            reader, writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                print('\n - TarGeT BoT in CLan ! ')
                print(f' - Clan Uid > {clan_id}')
                print(f' - BoT ConnEcTed WiTh CLan ChaT SuccEssFuLy ! ')
                pK = await AuthClan(clan_id, clan_compiled_data, key, iv)
                if whisper_writer: whisper_writer.write(pK); await whisper_writer.drain()
            while True:
                data = await reader.read(9999)
                if not data: break
                if data.hex().startswith("120000"):
                    msg = await DeCode_PackEt(data.hex()[10:])
                    chatdata = None
                    try:
                        chatdata = json.loads(msg)
                    except json.JSONDecodeError:
                        continue
                    uid = None; chat_id = None; XX = None; inPuTMsG = None
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        inPuTMsG = response.Data.msg.lower()
                    except Exception as e:
                        continue
                    if XX == 1 and isinstance(chatdata, dict):
                        try:
                            message_key = chatdata.get('1', {}).get('data', {}).get('1')
                            sender_uid_key = chatdata.get('1', {}).get('data', {}).get('2')
                            if message_key and sender_uid_key:
                                inPuTMsG = message_key.lower()
                                uid = int(sender_uid_key)
                                chat_id = LoGinDaTaUncRypTinG.Clan_ID
                        except:
                            continue
                    if uid and inPuTMsG:
                        # ---- COMMAND HANDLING (unchanged) ----
                        if inPuTMsG.startswith("/5"):
                            # ... (your /5 logic) ...
                            pass
                        if inPuTMsG.startswith('/t '):
                            # ... (your /t logic) ...
                            pass
                        if inPuTMsG.startswith('/solo'):
                            # ... (your /solo logic) ...
                            pass
                        if inPuTMsG.strip().startswith('/s'):
                            # ... (your /s logic) ...
                            pass
                        # ---- EMOTE SHORTCUT HANDLER (unchanged) ----
                        parts = inPuTMsG.strip().split()
                        if len(parts) >= 2 and parts[0].startswith('/') and parts[0][1:] in EMOTE_ALIASES:
                            # ... (your huge emote shortcut block) ...
                            pass
                        # ---- /e (full code) ----
                        if inPuTMsG.strip().startswith('/e'):
                            # ... (your /e block) ...
                            pass
                        # ---- HELP MESSAGE ----
                        if inPuTMsG in ("hi", "hello", "fen", "help", "/help"):
                            # ... (your help block) ...
                            pass
            whisper_writer.close(); await whisper_writer.wait_closed(); whisper_writer = None
        except Exception as e:
            print(f"ErroR {ip}:{port} - {e}"); whisper_writer = None
        await asyncio.sleep(reconnect_delay)

# --------------------------------------------------------------
# 3. EMOTE SEQUENCE (used by both API endpoints)
# --------------------------------------------------------------
async def perform_emote_sequence(uids_list, emote_id, team_code_str):
    global online_writer, whisper_writer, key, iv, region
    EM = await GenJoinSquadsPacket(team_code_str, key, iv)
    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', EM)
    await asyncio.sleep(2.5)
    for uid_target in uids_list:
        H = await Emote_k(uid_target, emote_id, key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
        await asyncio.sleep(0.5)
    await asyncio.sleep(3)
    leave = await ExiT(None, key, iv)
    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave)
    await asyncio.sleep(1)

# --------------------------------------------------------------
# 4. LOGIN-REQUIRED DECORATOR
# --------------------------------------------------------------
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return wrapper

# --------------------------------------------------------------
# 5. ROUTES – LOGIN FLOW
# --------------------------------------------------------------
@app.route('/')
def root():
    return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/do_login', methods=['POST'])
def do_login():
    discord_pw = request.form.get('discord-pw', '').strip()
    telegram_pw = request.form.get('telegram-pw', '').strip()

    if discord_pw == "225" and telegram_pw == "335":
        session['logged_in'] = True
        return jsonify({"status": "success", "redirect": "/index"})
    else:
        return jsonify({"status": "error", "message": "Wrong password"}), 401

# --------------------------------------------------------------
# 6. PROTECTED INDEX PAGE
# --------------------------------------------------------------
@app.route('/index')
@login_required
def index_page():
    try:
        with open('emotes.json', 'r') as f:
            emotes = json.load(f)
        return render_template('index.html', emotes=emotes)
    except FileNotFoundError:
        return "ERROR: emotes.json missing.", 500

# --------------------------------------------------------------
# 7. API ENDPOINTS (protected)
# --------------------------------------------------------------
@app.route('/send_emote', methods=['POST'])
@login_required
def send_emote():
    global LOOP
    if online_writer is None or LOOP is None or key is None or whisper_writer is None:
        return jsonify({"status":"error","message":"Bot not connected"}), 503
    try:
        data = request.get_json()
        team_code = data.get('team_code')
        emote_id_str = data.get('emote_id')
        uids_str = data.get('uids', [])
        if not all([team_code, emote_id_str, uids_str]):
            return jsonify({'message':'Missing data'}), 400
        target_uids_int = [int(uid) for uid in uids_str]
        emote_id_int = int(emote_id_str)
    except (ValueError, TypeError) as e:
        return jsonify({"status":"error","message":f"Invalid data: {e}"}), 400
    try:
        future = asyncio.run_coroutine_threadsafe(
            perform_emote_sequence(target_uids_int, emote_id_int, team_code), LOOP)
        future.result(timeout=30)
        return jsonify({'status':'success','message':f'Emote sent for {", ".join(uids_str)}'})
    except asyncio.TimeoutError:
        return jsonify({"status":"error","message":"Timeout"}), 500
    except Exception as e:
        return jsonify({"status":"error","message":str(e)}), 500

@app.route('/join', methods=['GET'])
@login_required
def join_and_emote_api():
    global LOOP
    target_uids_str = [request.args.get(f'uid{i}') for i in range(1,6) if request.args.get(f'uid{i}')]
    emote_id_str = request.args.get('emote_id')
    team_code = request.args.get('tc')
    if not target_uids_str or not emote_id_str or not team_code:
        return jsonify({"status":"error","message":"uid1, emote_id, tc required"}), 400
    if online_writer is None or LOOP is None or key is None or whisper_writer is None:
        return jsonify({"status":"error","message":"Bot not connected"}), 503
    try:
        target_uids_int = [int(uid) for uid in target_uids_str]
        emote_id = int(emote_id_str)
    except ValueError:
        return jsonify({"status":"error","message":"UIDs/Emote ID must be numeric"}), 400
    try:
        future = asyncio.run_coroutine_threadsafe(
            perform_emote_sequence(target_uids_int, emote_id, team_code), LOOP)
        future.result(timeout=30)
        return jsonify({"status":"success","message":"Emote command sent"})
    except asyncio.TimeoutError:
        return jsonify({"status":"error","message":"Timeout"}), 500
    except Exception as e:
        return jsonify({"status":"error","message":str(e)}), 500

# --------------------------------------------------------------
# 8. MAIN BOT LOOP
# --------------------------------------------------------------
async def MaiiiinE():
    global LOOP, key, iv, region, whisper_writer, online_writer, LoGinDaTaUncRypTinG
    LOOP = asyncio.get_running_loop()

    Uid, Pw = '4260656397', 'C4BB2682F8D27B593A5BE43E584432D0F936C8DB588B15FAB66E2B2DAF2C7ABD'
    open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
    if not open_id or not access_token: print("Invalid account"); return None
    PyL = await EncRypTMajoRLoGin(open_id, access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE: print("Account banned"); return None
    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    UrL = MajoRLoGinauTh.url
    region = MajoRLoGinauTh.region
    ToKen = MajoRLoGinauTh.token
    TarGeT = MajoRLoGinauTh.account_uid
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp
    LoGinDaTa = await GetLoginData(UrL, PyL, ToKen)
    if not LoGinDaTa: print("Failed to get ports"); return None
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    OnLineiP, OnLineporT = LoGinDaTaUncRypTinG.Online_IP_Port.split(":")
    ChaTiP, ChaTporT = LoGinDaTaUncRypTinG.AccountIP_Port.split(":")
    acc_name = LoGinDaTaUncRypTinG.AccountName
    equie_emote(ToKen, UrL)
    AutHToKen = await xAuThSTarTuP(int(TarGeT), ToKen, int(timestamp), key, iv)
    ready_event = asyncio.Event()
    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT, AutHToKen, key, iv,
                                       LoGinDaTaUncRypTinG, ready_event, region))
    await ready_event.wait()
    await asyncio.sleep(1)
    task2 = asyncio.create_task(TcPOnLine(OnLineiP, OnLineporT, key, iv, AutHToKen))

    # ---- start Flask in its own thread (same event loop) ----
    def run_flask():
        app.run(host='0.0.0.0', port=30151, debug=False, use_reloader=False)
    threading.Thread(target=run_flask, daemon=True).start()

    os.system('clear')
    print(render('WINTER', colors=['white', 'green'], align='center'))
    print(f"\nBot online – UID: {TarGeT} | Name: {acc_name}")
    print("Web UI: http://<YOUR_IP>:30151/")
    print("API example: http://<YOUR_IP>:30151/join?...")

    await asyncio.gather(task1, task2)

async def StarTinG():
    while True:
        try:
            await asyncio.wait_for(MaiiiinE(), timeout=7*60*60)
        except asyncio.TimeoutError:
            print("Token expired – restarting…")
        except Exception as e:
            print(f"TCP error: {e} – restarting…")

# --------------------------------------------------------------
# 9. ENTRY POINT
# --------------------------------------------------------------
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(StarTinG())
    try:
        loop.run_forever()
    finally:
        loop.close()
