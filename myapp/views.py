from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, View):
    """ ログイン後のメインページ """
    def get(self, request, *args, **kwargs):
        return render(request, "myapp/index.html")
