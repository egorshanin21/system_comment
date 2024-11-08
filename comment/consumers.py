import json
from channels.generic.websocket import AsyncWebsocketConsumer


class CommentConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time comments in a chat-like system.

    This consumer allows users to connect to a 'comments' room and participate in a real-time
    comment exchange. It listens for incoming comment data and broadcasts it to all clients in
    the room using Django Channels' channel layer. It also supports handling of WebSocket
    connections and disconnections.

    Methods:
        - connect: Establishes a WebSocket connection and adds the current channel to the comment room group.
        - disconnect: Handles the WebSocket disconnection, removing the channel from the group.
        - receive: Receives a comment message, decodes the data, and sends it to the comment room group.
        - chat_message: Sends a general message to the WebSocket.
        - new_comment: Sends a newly received comment to all connected WebSocket clients.
    """

    async def connect(self):
        """
        Handles establishing the WebSocket connection. When a user connects,
        they are added to the 'comment' room group so that they can receive
        real-time updates about new comments. The WebSocket is then accepted.

        This method is called automatically when a connection is established.
        """
        self.room_name = 'comments'
        self.room_group_name = f'comment_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        Handles the WebSocket disconnection. When a user disconnects, their channel
        is removed from the 'comment' room group to stop receiving new messages.

        :param close_code: The closing code for the connection, provided by the WebSocket.
        """
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Handles receiving a message from the WebSocket. This method processes incoming
        comment data in JSON format, decodes it, and then sends the comment data
        to the comment room group to be broadcasted to all connected users.

        :param text_data: The received message in JSON format, containing comment details
                          such as username, email, comment text, and timestamp.
        """

        text_data_json = json.loads(text_data)

        comment_data = {
            'username': text_data_json['username'],
            'email': text_data_json['email'],
            'text': text_data_json['message'],
            'created_at': text_data_json['created_at'],
            'id': text_data_json['id']
        }

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'new_comment',
                'comment_data': comment_data
            }
        )

    async def chat_message(self, event):
        """
        Sends a chat message to the WebSocket. This method is used for transmitting
        general messages, such as notifications or system messages.

        :param event: An event containing the message to be sent.
        """
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def new_comment(self, event):
        """
        Sends a new comment to the WebSocket. When a new comment is received from
        the `receive` method, it is broadcasted to all connected clients in real-time.

        :param event: The event containing the new comment's data, including
                      username, email, message text, and timestamp.
        """
        comment_data = event['comment_data']

        await self.send(text_data=json.dumps({
            'type': 'new_comment',
            'comment_data': comment_data
        }))
