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

# Ensures that ALL information is pulled until requests.get() returns an error, signifying the end of the GroupMe message stream
while True:
    ret_dict = None
    #If we don't have a set last_id, we haven't started pulling messages yet, and so the request URL will not contain a last_id
    if last_id == "":
        ret = requests.get('https://api.groupme.com/v3/groups/' + group_id + '/messages?token=' + access_token)
        ret_dict = json.loads(ret.content.decode('utf-8'))
    else: #Otherwise, we pull messages that occured before the id of the last message we pulled
        ret = requests.get('https://api.groupme.com/v3/groups/' + group_id + '/messages?token=' + access_token + '&before_id=' + last_id + '&limit=100')
        try:
            ret_dict = json.loads(ret.content.decode('utf-8'))
        except Exception as err:
            print(str(err))
            break

    print(str(ret_dict))
    # For each message we get
    for message in ret_dict['response']['messages']:
        # Grab the sender's name, id, and how many likes they got
        sender_name = message['name']
        sender_id = message['user_id']
        likes_to_add = len(message['favorited_by'])
        does_sender_exist = False
        # Check to see if we've added this sender to the people_list
        for person in people_list:
            # If so, update their information and add likes
            if person['id'] == sender_id:
                does_sender_exist = True
                person['name'] = sender_name
                person['likes_received'] += likes_to_add
                person['posts_made'] += 1
                break
        # If not, add them to the dictionary
        if not does_sender_exist:
            people_list.append({'id':sender_id,
                                'name':sender_name,
                                'likes_sent':0,
                                'posts_made':1,
                                'likes_received':likes_to_add})
        # For each person that liked the current message
        does_liker_exist = False
        for id in message['favorited_by']:
            # Check if they've been added to the people_list, and add to their 'likes_sent' count if so
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
        # Update last_id
        last_id = message['id']
        msg_count += 1
        num_likes_tot += likes_to_add

        print(str(last_id))
        
        # If the message has attachments, pull the URL and add it, along with sender name and accompanying text to url_list
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

                
# Printing results:
print("MSG COUNT: " + str(msg_count))
print("NUM LIKES TOTAL: " + str(num_likes_tot))
print("LIST: " + str(people_list))
print("SORTED BY MOST POSTS: ")

# print people sorted by number of posts made
posts = sorted(people_list, key=lambda k:k['posts_made'])
for person in posts:
    print(str(person))

# Print people sorted by likes sent
print("SORTED BY WHO SENT THE MOST LIKES: ")
sent_likes = sorted(people_list, key=lambda k:k['likes_sent'])
for person in sent_likes:
    print(str(person))

# Print people sorted by likes received
print("SORTED BY WHO GOT THE MOST LIKES: ")
received_likes = sorted(people_list, key=lambda k:k['likes_received'])
for person in received_likes:
    print(str(person))

# Print urls of pictures sent to the chat
print("URLS:")
for line in url_list:
    print(line)

# Finally, write the URLS of the picuters sent to the chat to a text file
curDir = os.path.dirname(os.path.realpath('__file__'))

# REPLACE ****** with the filename you want to write to
with os.fdopen(os.open(curDir + "/******.txt", os.O_WRONLY), "w", encoding='utf-8') as file_write:
    file_write.write("\n".join(url_list))


