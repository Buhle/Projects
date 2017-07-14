# Projects
Chat server

**payload must be a json**

## Payload for saving chats calling webservice

payload = {'username':'buhle', 'message':'Hey there','messageto':'24680'}}

**Responese**
u'chat saved'

**Status code**
200 OK

## Payload for update chats calling webservice

payload = {'username':'12345', 'message':'Hey there', 'id':'5','messageto':'24680'}

**Response**
u'message updated'

**Status code** 
200 OK

## Payload for view chats calling webservice

payload = {'user1':'12345', 'user2':'24680'}

**Response**

u"[(1, datetime.datetime(2017, 7, 10, 14, 36, 48), '12345', 'Hi', '24680'), (2, datetime.datetime(2017, 7, 10, 14, 43, 3), '24680', 'Hi', '12345'), (3, datetime.datetime(2017, 7, 10, 14, 45, 59), '12345', 'How are you?', '24680'), (4, datetime.datetime(2017, 7, 10, 14, 47, 9), '24680', 'good and you?', '12345'), (5, datetime.datetime(2017, 7, 10, 14, 51, 57), '12345', 'Hi', '24680')]"

**Status code** 
200 OK
