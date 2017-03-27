import requests, json, os

# REPLACE these with the bot id and access token you get from the groupme API registration
# REPLACE the group_id with the id of the group you add your bot to
bot_id = "#####"
access_token = "#####"
group_id = "#####"

last_id = ""
count = 0
url_list = []

# REPLACE ### with the number of images you want to pull
while count < ###:
    ret_dict = None
    if last_id == "":
        ret = requests.get('https://api.groupme.com/v3/groups/' + group_id + '/messages?token=' + access_token)
        ret_dict = json.loads(ret.content.decode('utf-8'))
    else:
        ret = requests.get('https://api.groupme.com/v3/groups/' + group_id + '/messages?token=' + access_token + '&before_id=' + last_id + '&limit=100')
        ret_dict = json.loads(ret.content.decode('utf-8'))

    for message in ret_dict['response']['messages']:
        last_id = message['id']
        attach = message['attachments']
        if len(attach) > 0:
            
            if 'url' in attach[0]:
                count += 1
                url_list.append("Sender: " + str(message['name']))
                url_list.append("Text: " + str(message['text']))
                url_list.append("Pic: " + str(attach[0]['url']))


curDir = os.path.dirname(os.path.realpath('__file__'))

# REPLACE ****** with the filename you want to write to
with os.fdopen(os.open(curDir + "/******.txt", os.O_WRONLY), "w", encoding='utf-8') as file_write:
    file_write.write("\n".join(url_list))


