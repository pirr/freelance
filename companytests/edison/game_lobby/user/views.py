from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import View
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout
from django.shortcuts import redirect

from .models import UserStatus
from .forms import RFPAuthForm


class RegisterFormView(FormView):

    form_class = UserCreationForm
    success_url = '/user/login/'
    template_name = 'register.html'

    def form_valid(self, form):
        form.save()

        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):

    form_class = RFPAuthForm
    template_name = 'login.html'
    success_url = '/hole/'

    def form_valid(self, form):
        self.user = form.get_user()

        try:
            UserStatus.objects.filter(player=self.user.id).delete()

        except:
            print('user had not online')

        login(self.request, self.user)

        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):

    def get(self, request):
        logout(request)

        return redirect('/user/login/')
