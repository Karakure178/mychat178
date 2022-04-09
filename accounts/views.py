from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy,reverse
from django.views import generic
from . import models
from . import forms

class Login(LoginView):
    form_class = forms.LoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy('profile')

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

class SignUpdoneView(generic.TemplateView):
    template_name = "registration/signup_done.html"

# def chat_test( request ):
#     return render( request, 'chat/chat_test.html' )

class ChatTestView(LoginRequiredMixin, generic.TemplateView):
    template_name =  'chat/chat_test.html'








# from django.shortcuts import render

# # Create your views here.

# def chat( request ):
#     return render( request, 'chat/chat.html' )

# def chat_test( request ):
#     return render( request, 'chat/chat_test.html' )



# from django.views import generic
# from django.contrib import messages
# from django.contrib.auth.mixins import LoginRequiredMixin
# from . import models
# from . import forms

# class HomeView(generic.FormView):
#     posted_data = {"text": "",
#                "select_part": []}
#     template_name = "home.html"
#     # form_class = forms.ExampleForm
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["user"] =  models.User.objects.all().order_by("id")[0]
#         context["followers"] = models.User.objects.all().order_by("id")[0].followers.all()
#         context["followees"] = models.User.objects.all().order_by("id")[0].followees.all()

#         # print(context["user"].followers)
#         # print(type(context["user"].followers.all()))
#         # print(context["user"])
#         return context
#     def form_valid(self, form):
#         self.posted_data["text"] = form.data.get("follower")
#         return super().form_valid(form)


# class TestView(generic.FormView):
#     template_name = 'home2.html'
#     form_class = forms.ExampleForm
#     success_url = '/admin'  # リダイレクト先URL
#     def form_valid(self, form):
#         form.save()  # 保存処理など
#         messages.add_message(self.request, messages.SUCCESS, '登録しました！')
#         return super().form_valid(form)


# class UserChangeView(LoginRequiredMixin, generic.FormView):
#     template_name = 'change.html'
#     form_class = forms.UserChangeForm
#     # success_url = reverse_lazy('accounts:profile')
    
#     def form_valid(self, form):
#         #formのupdateメソッドにログインユーザーを渡して更新
#         form.update(user=self.request.user)
#         return super().form_valid(form)

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         # 更新前のユーザー情報をkwargsとして渡す
#         kwargs.update({
#             'email' : self.request.user.email,
#             'first_name' : self.request.user.first_name,
#             'last_name' : self.request.user.last_name,
#         })
#         return kwargs