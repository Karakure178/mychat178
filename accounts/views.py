from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.views import generic
from . import models
from . import forms

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
class Login(LoginView):
    form_class = forms.LoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy('profile')
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(Login, self).dispatch(*args, **kwargs)

class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = "registration/profile.html"
    #success_url = reverse_lazy('top')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["room"] =  models.Room.objects.all().order_by("id")
        return context
    def get_success_url(self):
        # reverse("room",kwargs={'pk': self.object.pk})
        return reverse("room",kwargs={'pk': self.objects.get(self.object.pk)})
        #思いついた、pk : self.objects.get(self.object.pk)で行けるのでは？
        #ここ選択された時valueを与えたいのにわからない。pkじゃなくて


from django.contrib import messages
class RoomAddView(LoginRequiredMixin, generic.FormView):
    template_name = "registration/room_add.html"    
    form_class = forms.RoomAddForm
    success_url = reverse_lazy('profile')  # リダイレクト先URL

    def form_valid(self, form):
        event = form.save(commit=False)
        event.save()
        form.save_m2m()
        messages.add_message(self.request, messages.SUCCESS, '登録しました！')  # メッセージ出力
        return super().form_valid(form)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(RoomAddView, self).dispatch(*args, **kwargs)




def room(request, pk):
    return render(request, 'registration/room.html', {
        'room': pk
    })

#room_test.htmlテスト
def room_test(request, pk):
    room_names = models.Room.objects.all().order_by('id')
    return render(request, 'registration/room_test.html', {
        'room': pk,"room_names":room_names
    })

class Logout(LogoutView):
    template_name = "registration/logout.html"

class TopView(generic.TemplateView):
    template_name = "registration/top.html"


class SignUpView(generic.CreateView):
    form_class = forms.SignUpForm
    #form_class = UserCreationForm #カスタムuserを使う場合はエラー
    success_url = reverse_lazy('signup_done')
    template_name = 'registration/signup.html'
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SignUpView, self).dispatch(*args, **kwargs)


class SignUpdoneView(generic.TemplateView):
    template_name = "registration/signup_done.html"

class ChatTestView(LoginRequiredMixin, generic.TemplateView):
    template_name =  'chat/chat_test.html'
    # form_class = forms.ChatAddForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #自分が登録されてるルームのみ表示
        who = models.User.objects.filter(id=self.request.user.id)
        data = models.Room.objects.filter(meta__in=who)
        
        #アクセスしてるusernameでchatを検索しヒットしたオブジェクトをdata_chatsに突っ込む
        #request_username = models.User.objects.get(id=self.request.user.id)
        request_chats = models.Chat.objects.all()#models.Chat.objects.filter(name=request_username)
        context["room_names"] =  data

        #data_chatsをそれぞれのルームへ分割arrayしたい、今持ってるルーム数知りたい
        room_data = self._rooms_get(data)
        rooms_chats =  self._rooms_chat_get(room_data,request_chats)
        """
        rooms_chat[ルーム数][ [ユーザ名],[text],[時間],[アイコン] ]
        """
        context["rooms"] = room_data #所属するルーム達
        context["room_chats"] = rooms_chats #所属するルームとチャット内容

        return context

    #ユーザーが所属するルームのみ取得
    def _rooms_get(self,data):
        rooms = list()
        for i in data:
            if i.room not in rooms:
                print(i.room)
                rooms.append(i.room)
        return rooms

    #ユーザーが所属するルームののchatlist(ユーザ名,ルーム名,チャット内容)を返却
    def _rooms_chat_get(self,room_data,chat_data):
        chats = [[] for i in range(len(room_data))]
        for i in chat_data:
            room_index = room_data.index(i.room)#ただのlistに変換
            chats[room_index].append([i.name,i.text,i.time.strftime('%Y/%m/%d %H:%M:%S'),])
        return chats

class UserChangeView(LoginRequiredMixin, generic.FormView):
    template_name = 'registration/profile_edit.html'
    form_class = forms.UserChangeForm
    success_url = reverse_lazy('accounts:profile')
    
    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'email' : self.request.user.email,
            'first_name' : self.request.user.first_name,
            'last_name' : self.request.user.last_name,
        })
        return kwargs


#本番用500errorを詳細に書く
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseServerError
@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)