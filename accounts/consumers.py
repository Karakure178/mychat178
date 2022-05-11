import json
#from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
#from asgiref.sync import async_to_sync  # async_to_sync() : 非同期関数を同期的に実行する際に使用する。
import datetime
from accounts.models import Chat
from users.models import User
from channels.db import database_sync_to_async

# ChatConsumerクラス: WebSocketからの受け取ったものを処理するクラス
class ChatConsumer( AsyncWebsocketConsumer ):
    # コンストラクタ
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.strGroupName = ''
        self.strUserName = ''
        self.strRoomName = "" #追加

    # WebSocket接続時の処理
    async def connect( self ):
        # WebSocket接続を受け入れます。
        # ・connect()でaccept()を呼び出さないと、接続は拒否されて閉じられます。
        # 　たとえば、要求しているユーザーが要求されたアクションを実行する権限を持っていないために、接続を拒否したい場合があります。
        # 　接続を受け入れる場合は、connect()の最後のアクションとしてaccept()を呼び出します。
        await self.accept()

    # WebSocket切断時の処理
    async def disconnect( self, close_code ):
        # チャットからの離脱
        await self.leave_chat()

    # WebSocketからのデータ受信時の処理
    # （ブラウザ側のJavaScript関数のsocketChat.send()の結果、WebSocketを介してデータがChatConsumerに送信され、本関数で受信処理します）
    async def receive( self, text_data ):
        # 受信データをJSONデータに復元
        text_data_json = json.loads( text_data )

        # チャットへの参加時の処理
        if( 'join' == text_data_json.get( 'data_type' ) ):
            # ユーザー名をクラスメンバー変数に設定
            self.strUserName = text_data_json['username']
            # ルーム名の取得
            self.strRoomName = text_data_json['roomname']#追加
            
            # チャットへの参加
            await self.join_chat( self.strRoomName )

        # チャットからの離脱時の処理
        elif( 'leave' == text_data_json.get( 'data_type' ) ):
            # チャットからの離脱
            await self.leave_chat()

        # メッセージ受信時の処理
        else:
            # メッセージの取り出し
            strMessage = text_data_json['message']
            # グループ内の全コンシューマーにメッセージ拡散送信（受信関数を'type'で指定）
            data = {
                'type': 'chat_message', # 受信処理関数名
                'message': strMessage, # メッセージ
                'username': self.strUserName, # ユーザー名
                "roomname": self.strRoomName,#追加
                'datetime': datetime.datetime.now().strftime( '%Y/%m/%d %H:%M:%S' ), # 現在時刻
                "icon": await self._icon_send(self.strUserName),
            }

            #メッセージの送信＆DB保存
            await self.channel_layer.group_send( self.strGroupName, data )
            await self._save_message(self.strUserName,self.strRoomName,strMessage)        

    # 拡散メッセージ受信時の処理
    # （self.channel_layer.group_send()の結果、グループ内の全コンシューマーにメッセージ拡散され、各コンシューマーは本関数で受信処理します）
    async def chat_message( self, data ):
        data_json = {
            'message': data['message'],
            'username': data['username'],
            'datetime': data['datetime'],
            'roomname': data['roomname'],
            'icon': data['icon'],
        }
        # WebSocketにメッセージを送信します。
        # （送信されたメッセージは、ブラウザ側のJavaScript関数のsocketChat.onmessage()で受信処理されます）
        # JSONデータをテキストデータにエンコードして送ります。
        await self.send( text_data=json.dumps( data_json ) )

    # チャットへの参加
    async def join_chat( self, strRoomName ):
        # グループに参加
        #self.strGroupName = 'chat_%s' % strRoomName
        self.strGroupName = 'chat_' + strRoomName
        print(self.strGroupName)
        await self.channel_layer.group_add( self.strGroupName, self.channel_name )


    # チャットからの離脱
    async def leave_chat( self ):
        if( '' == self.strGroupName ):
            return

        # グループから離脱
        await self.channel_layer.group_discard( self.strGroupName, self.channel_name )

        # ルーム名を空に
        self.strGroupName = ''

    #chatのDBに保存
    @database_sync_to_async
    def _save_message(self, your_user, room_name, strMessage):
        icon_url = User.objects.filter(username__iexact=your_user)
        Chat.objects.create(name=your_user,room=decode_roomname(room_name),text=strMessage, icon=icon_url[0])

    #icon.urlをmessagejsonに返す
    @database_sync_to_async
    def _icon_send(self,user_name):
        user_k = User.objects.filter(username__iexact=user_name)
        return user_k[0].icon.url

#送られるルーム名がASCIIなため元に戻す関数
def decode_roomname(room_name):
    # print(room_name)
    decode = room_name.split('.')
    roomDecode = ""
    for i in decode:
        roomDecode = roomDecode + chr(int(i))
    #chr(int)でascii文字列に変換
    return roomDecode


# class NotiConsumer( AsyncWebsocketConsumer ):
#     # コンストラクタ
#     def __init__( self, *args, **kwargs ):
#         super().__init__( *args, **kwargs )
#         self.strGroupName = ''
#         self.strUserName = ''
#         self.strRoomName = "" #追加

#     # WebSocket接続時の処理
#     async def connect( self ):
#         await self.accept()

#     async def disconnect( self, close_code ):
#         # チャットからの離脱
#         await self.leave_chat()

#     async def receive( self, text_data ):
#         # 受信データをJSONデータに復元
#         text_data_json = json.loads( text_data )

#         # チャットへの参加時の処理
#         if( 'noti' == text_data_json.get( 'data_type' ) ):
#             self.strUserName = text_data_json['username']
#             self.strRoomName = text_data_json['roomname']
#             await self.join_chat( self.strRoomName )

#         # チャットからの離脱時の処理
#         elif( 'leave' == text_data_json.get( 'data_type' ) ):
#             await self.leave_chat()

#     # 通知機能への参加
#     async def join_chat( self, strRoomName ):
#         # グループに参加
#         #self.strGroupName = 'chat_%s' % strRoomName
#         self.strGroupName = 'chat_' + strRoomName
#         print(self.strGroupName)
#         await self.channel_layer.group_add( self.strGroupName, self.channel_name )