from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, UserChannelsTooMuchError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import random

bot = sys.argv[1]

list_account = open(bot + "/account.txt", "r")
account_list = list_account.read()
content_list = account_list.split(",")
list_account.close()

api_id =  content_list[0]
api_hash = content_list[1]
phone = content_list[2]

client = TelegramClient(phone, api_id, api_hash)
async def main():
    return

FLOOD_ERROR_TIME = 1800 #30 minutes

with client:
    client.loop.run_until_complete(main())
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('40779'))

users = []
with open(bot + "/Scrapped Users/scrapped.csv", "r", encoding="UTF-8") as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print('\n[*] Choose a group to add members:\n')
i = 0
for group in groups:
    print(str(i) + ' - ' + group.title)
    i += 1

g_index = input("\n[*] Enter a Number: ")
target_group = groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

n = 0

for user in users:
    n += 1
    if n % 80 == 0:
        time.sleep(60)
    try:
        print("Adding {}".format(user['id']))
        if user['username'] == "":
            continue
        user_to_add = client.get_input_entity(user['username'])
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        time.sleep(random.randrange(60, 90))
    except PeerFloodError:
        print("[*] Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        print("Waiting {} seconds".format(FLOOD_ERROR_TIME))
        time.sleep(FLOOD_ERROR_TIME)
    except UserPrivacyRestrictedError:
        print("[*] The user's privacy settings do not allow you to do this. Skipping.")
        time.sleep(20)
    except UserChannelsTooMuchError:
        print("User already joined a lot of group. Skipping.")
        time.sleep(20)
    except:
        traceback.print_exc()
        print("[*] Unexpected Error")
        continue

print("[*] Already add all user to selected group.")