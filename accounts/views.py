from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from . import models
from . import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class Login(LoginView):
    form_class = forms.LoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy('test_login')
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(Login, self).dispatch(*args, **kwargs)

class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = "registration/profile.html"
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)
    #success_url = reverse_lazy('top')


from django.contrib import messages
class RoomAddView(LoginRequiredMixin, generic.FormView):
    template_name = "registration/room_add.html"    
    form_class = forms.RoomAddForm
    success_url = reverse_lazy('chat_test')  # リダイレクト先URL

    def form_valid(self, form):
        event = form.save(commit=False)
        event.save()
        form.save_m2m()
        messages.add_message(self.request, messages.SUCCESS, '登録しました！')  # メッセージ出力
        return super().form_valid(form)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(RoomAddView, self).dispatch(*args, **kwargs)


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
        context["room_names"] =  data

        return context

class UserChangeView(LoginRequiredMixin, generic.FormView):
    template_name = 'registration/profile_edit.html'
    form_class = forms.UserChangeForm
    success_url = reverse_lazy('profile')
    #success_url = reverse_lazy('accounts:profile')だとエラー...なんで?
    
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
            'header' : self.request.user.header,
        })
        return kwargs


#test
class TestView(generic.FormView):
    template_name = "test.html"
    form_class = forms.TestForm
    success_url = reverse_lazy('top')
    def form_valid(self, form):
        return super().form_valid(form)


#本番用500errorを詳細に書く
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseServerError
@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)



import django_filters
from rest_framework import viewsets, filters
from rest_framework import generics
from .models import Chat,Room
from .serializer import ChatSerializer,RoomSerializer

# class ChatViewSet(generics.RetrieveAPIView):
#     queryset = Chat.objects.all()
#     serializer_class = ChatSerializer
    # lookup_field = 'room'

class ChatViewSet(generics.ListAPIView):
    serializer_class = ChatSerializer

    #api_chat/かapi_chat/strかで場合分け
    def get_queryset(self):
        if len(self.kwargs) == 0:
            return Chat.objects.all()
        else:
            category = self.kwargs['room']
            return Chat.objects.filter(room=category)

class RoomViewSet(generics.ListAPIView):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    def get_queryset(self):
        user_id = self.kwargs['meta']
        return Room.objects.filter(meta=user_id)

class GreetView(generic.FormView):
    template_name = 'ajax_test.html'  # テンプレート名(htmlファイル名)
    form_class = forms.GreetForm
    success_url = reverse_lazy('ajax_test')
