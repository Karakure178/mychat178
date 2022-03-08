import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync  # async_to_sync() : 非同期関数を同期的に実行する際に使用する。
from channels.db import database_sync_to_async
from .models import Chat
#from django.contrib.auth.models import User
from users.models import User
import time

@database_sync_to_async
def kansu():
    print("テスト")
    #self.room_nameくん、urlを選択した値に変更できないため（やり方がわからん）、有効化できない。

# ChatConsumerクラス: WebSocketからの受け取ったものを処理するクラス
#多分同期処理、sync_to_asyncは非同期の場合の定義なため同期処理だと動かない
class ChatConsumer( WebsocketConsumer ):
    # WebSocket接続時の処理
    room_name=""
    def connect( self ):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # グループに参加
        self.strGroupName = 'accounts'
        async_to_sync( self.channel_layer.group_add )( self.strGroupName, self.channel_name )

        # WebSocket接続を受け入れます。
        # ・connect()でaccept()を呼び出さないと、接続は拒否されて閉じられます。
        # 　たとえば、要求しているユーザーが要求されたアクションを実行する権限を持っていないために、接続を拒否したい場合があります。
        # 　接続を受け入れる場合は、connect()の最後のアクションとしてaccept()を呼び出します。
        self.accept()

    # WebSocket切断時の処理
    def disconnect( self, close_code ):
        # グループから離脱
        async_to_sync( self.channel_layer.group_discard )( self.strGroupName, self.channel_name )

    # WebSocketからのデータ受信時の処理
    # （ブラウザ側のJavaScript関数のsocketChat.send()の結果、WebSocketを介してデータがChatConsumerに送信され、本関数で受信処理します）
    def receive( self, text_data ):
        # 受信データをJSONデータに復元
        text_data_json = json.loads( text_data )

        # メッセージの取り出し
        strMessage = text_data_json['message']
        your_user = text_data_json["user"]
        # グループ内の全コンシューマーにメッセージ拡散送信（受信関数を'type'で指定）
        data = {
            'type': 'chat_message', # 受信処理関数名
            'message': strMessage, # メッセージ
            "user": your_user,
        }
        async_to_sync( self.channel_layer.group_send )( self.strGroupName, data )
        #Chat.objects.create(room=self.room_name, text=strMessage, name=User.objects.filter(username=your_user))
        
        self._save_message(your_user,self.room_name,strMessage)        
        #Chat.objects.create(name=your_user, room=self.room_name, text=strMessage, )

    # 拡散メッセージ受信時の処理
    # （self.channel_layer.group_send()の結果、グループ内の全コンシューマーにメッセージ拡散され、各コンシューマーは本関数で受信処理します）
    def chat_message( self, data ):
        data_json = {
            'message': data['message'],
            'user': data['user'],
        }

        # WebSocketにメッセージを送信します。
        # （送信されたメッセージは、ブラウザ側のJavaScript関数のsocketChat.onmessage()で受信処理されます）
        # JSONデータをテキストデータにエンコードして送ります。
        self.send( text_data=json.dumps( data_json ) )
    
    def _save_message(self, your_user, room_name, strMessage):
        #Chat.objects.create(name=your_user,room=room_name,text=strMessage,)
        Chat.objects.create(name=your_user,room=room_name,text=strMessage, )
        print("動くぞい!")



#room_test用
class RoomTestConsumer( WebsocketConsumer ):
    # WebSocket接続時の処理
    room_name=""
    def connect( self ):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # グループに参加
        self.strGroupName = 'accounts'
        async_to_sync( self.channel_layer.group_add )( self.strGroupName, self.channel_name )

        # WebSocket接続を受け入れます。
        # ・connect()でaccept()を呼び出さないと、接続は拒否されて閉じられます。
        # 　たとえば、要求しているユーザーが要求されたアクションを実行する権限を持っていないために、接続を拒否したい場合があります。
        # 　接続を受け入れる場合は、connect()の最後のアクションとしてaccept()を呼び出します。
        self.accept()

    # WebSocket切断時の処理
    def disconnect( self, close_code ):
        # グループから離脱
        async_to_sync( self.channel_layer.group_discard )( self.strGroupName, self.channel_name )

    # WebSocketからのデータ受信時の処理
    # （ブラウザ側のJavaScript関数のsocketChat.send()の結果、WebSocketを介してデータがChatConsumerに送信され、本関数で受信処理します）
    def receive( self, text_data ):
        # 受信データをJSONデータに復元
        text_data_json = json.loads( text_data )

        # メッセージの取り出し
        strMessage = text_data_json['message']
        your_user = text_data_json["user"]
        # グループ内の全コンシューマーにメッセージ拡散送信（受信関数を'type'で指定）
        data = {
            'type': 'chat_message', # 受信処理関数名
            'message': strMessage, # メッセージ
            "user": your_user,
        }
        async_to_sync( self.channel_layer.group_send )( self.strGroupName, data )
        #Chat.objects.create(room=self.room_name, text=strMessage, name=User.objects.filter(username=your_user))
        
        self._save_message(your_user,self.room_name,strMessage)        
        #Chat.objects.create(name=your_user, room=self.room_name, text=strMessage, )

    # 拡散メッセージ受信時の処理
    # （self.channel_layer.group_send()の結果、グループ内の全コンシューマーにメッセージ拡散され、各コンシューマーは本関数で受信処理します）
    def chat_message( self, data ):
        data_json = {
            'message': data['message'],
            'user': data['user'],
        }

        # WebSocketにメッセージを送信します。
        # （送信されたメッセージは、ブラウザ側のJavaScript関数のsocketChat.onmessage()で受信処理されます）
        # JSONデータをテキストデータにエンコードして送ります。
        self.send( text_data=json.dumps( data_json ) )
    
    def _save_message(self, your_user, room_name, strMessage):
        #Chat.objects.create(name=your_user,room=room_name,text=strMessage,)
        Chat.objects.create(name=your_user,room=room_name,text=strMessage, )
        print("動くぞい!")