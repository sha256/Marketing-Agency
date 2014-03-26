from django.http import Http404
from apps.auth.forms.adduser import PasswordResetForm
from apps.auth.models import User
from core.views import SmartView
from datetime import datetime

__author__ = 'sha256'


class PasswordResetView(SmartView):

    def get_common_data(self, request):
        data = {}
        form = PasswordResetForm()
        if len(self.code) < 5:
            raise Http404()

        try:
            user = User.objects.get(password_reset=self.code)
        except:
            raise Http404()
        else:
            if user.password_reset_expire < datetime.now():
                data['expire'] = True
            else:
                form = PasswordResetForm(request.POST or None, instance=user)
                if form.is_valid():
                    form.save()
                    user.password_reset = ""
                    user.save()
                    data['success'] = True

        data['form'] = form
        return data

    def get(self, request, code, *args, **kwargs):
        self.code = code
        return self.render(request, "auth/password_reset.html", {})

    def post(self, request, code, *args, **kwargs):
        self.code = code
        return self.render(request, "auth/password_reset.html", {})




