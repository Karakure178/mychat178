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

def room(request, pk):
    return render(request, 'registration/room.html', {
        'room': pk
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