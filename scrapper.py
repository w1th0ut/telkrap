from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv
import sys

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

with client:
    client.loop.run_until_complete(main())
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('[*] Enter verification code: '))


chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

print('\n[*] From Which Group Yow Want To Scrap A Members?\n')
i=0
for g in groups:
    print(str(i) + ' - ' + g.title)
    i+=1

g_index = input("\n[*] Enter a Number: ")
target_group=groups[int(g_index)]

print('[*] Fetching Members..')

all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)

print('[*] Saving and overwriting In file..')
with open(bot + "/Scrapped Users/scrapped.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])
print('[*] Members scraped successfully..\n')