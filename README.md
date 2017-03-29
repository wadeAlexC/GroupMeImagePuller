# GroupMeImagePuller
Short, simple, bot to pull images from a GroupMe chat and write their urls to a text file

Link to the GroupMe API to register your bot: https://dev.groupme.com/bots/new
To use this program, register a new bot account, pick the group you want it to be in, name it, and pick an avatar URL. Leave the callback URL field blank- this bot does not receive POST requests. Once your bot is registered, you can visit https://dev.groupme.com/bots and click on the bot you just created to get the Bot Id, Group Id, and Access Token, which you will need to copy into the marked spots in application.py

UPDATE:

Added functions-
Now functions as a GroupMe metrics bot:
1. Counts how many messages have been sent to the group in total
2. Counts the number of likes in the group in total
3. Displays lists of people in the group sorted by:
a. Most posts made
b. Most likes given
c. Most likes received

Finally, still takes the urls of each image sent to the group and writes them to a text file, but now includes text containing the sender name and whatever text was included with the sent image.
