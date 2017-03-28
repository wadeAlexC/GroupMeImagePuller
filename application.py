import requests, json, os

# REPLACE these with the bot id and access token you get from the groupme API registration
# REPLACE the group_id with the id of the group you add your bot to
bot_id = "#####"
access_token = "#####"
group_id = "#####"

last_id = ""
count = 0
url_list = []

msg_count = 0
num_likes_tot = 0
people_list = []

while True:
    ret_dict = None
    if last_id == "":
        ret = requests.get('https://api.groupme.com/v3/groups/' + group_id + '/messages?token=' + access_token)
        ret_dict = json.loads(ret.content.decode('utf-8'))
    else:
        ret = requests.get('https://api.groupme.com/v3/groups/' + group_id + '/messages?token=' + access_token + '&before_id=' + last_id + '&limit=100')
        try:
            ret_dict = json.loads(ret.content.decode('utf-8'))
        except Exception as err:
            print(str(err))
            break

    print(str(ret_dict))
    for message in ret_dict['response']['messages']:
        sender_name = message['name']
        sender_id = message['user_id']
        likes_to_add = len(message['favorited_by'])
        does_sender_exist = False
        for person in people_list:
            if person['id'] == sender_id:
                does_sender_exist = True
                person['name'] = sender_name
                person['likes_received'] += likes_to_add
                person['posts_made'] += 1
                break

        if not does_sender_exist:
            people_list.append({'id':sender_id,
                                'name':sender_name,
                                'likes_sent':0,
                                'posts_made':1,
                                'likes_received':likes_to_add})

        does_liker_exist = False
        for id in message['favorited_by']:
            for person in people_list:
                if person['id'] == id:
                    does_liker_exist = True
                    person['likes_sent'] += 1
                    break

            if does_liker_exist == False:
                people_list.append({'id':sender_id,
                                    'name':'unknown',
                                    'likes_sent':1,
                                    'posts_made':0,
                                    'likes_received':0})

        last_id = message['id']
        msg_count += 1
        num_likes_tot += likes_to_add

        print(str(last_id))
        attach = message['attachments']
        if len(attach) > 0:

            if 'url' in attach[0]:
                count += 1
                print(str(message['name']))
                print(str(message['text']))
                url_list.append("Sender: " + str(message['name']))
                url_list.append("Text: " + str(message['text']))
                url_list.append("Pic: " + str(attach[0]['url']))
                print("URL: " + str(attach[0]['url']))

print("MSG COUNT: " + str(msg_count))
print("NUM LIKES TOTAL: " + str(num_likes_tot))
print("LIST: " + str(people_list))
print("SORTED BY MOST POSTS: ")
posts = sorted(people_list, key=lambda k:k['posts_made'])
for person in posts:
    print(str(person))

print("SORTED BY WHO SENT THE MOST LIKES: ")
sent_likes = sorted(people_list, key=lambda k:k['likes_sent'])
for person in sent_likes:
    print(str(person))

print("SORTED BY WHO GOT THE MOST LIKES: ")
received_likes = sorted(people_list, key=lambda k:k['likes_received'])
for person in received_likes:
    print(str(person))

print("URLS:")
for line in url_list:
    print(line)

curDir = os.path.dirname(os.path.realpath('__file__'))

# REPLACE ****** with the filename you want to write to
with os.fdopen(os.open(curDir + "/******.txt", os.O_WRONLY), "w", encoding='utf-8') as file_write:
    file_write.write("\n".join(url_list))


