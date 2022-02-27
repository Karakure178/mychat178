from django.urls import path
from . import consumers
#urls.pyに当たる処理

websocket_urlpatterns = [
    path( 'ws/accounts/<str:room_name>', consumers.ChatConsumer.as_asgi() ),
    #本来はコメントアウトが正しい。ただしstrをviewで選択された値にしたいがそれがわからんため有効化出来ぬ
    #path( 'ws/accounts/', consumers.ChatConsumer.as_asgi() ),
]