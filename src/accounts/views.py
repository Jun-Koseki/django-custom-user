from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, View
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .mixins import PasswordChangeRequiredMixin
import logging

logger = logging.getLogger(__name__)


class SignUpView(SuccessMessageMixin, CreateView):

    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    success_message = "Registered your account successfully!"

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)
        logger.info("User ID: {} has been registered.".format(new_user.id))
        return valid

    def get_success_url(self):
        return reverse('myapp:index')


class ProfileView(LoginRequiredMixin, PasswordChangeRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        initial_value = dict(username=request.user.username, email=request.user.email, bio=request.user.bio,
                             website=request.user.website)
        form = CustomUserChangeForm(request.GET or None, initial=initial_value)
        context = {"form": form}
        return render(request, "registration/profile.html", context=context)

    def post(self, request, *args, **kwargs):
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, "Profile updated successfully.")
            return redirect(reverse('myapp:index'))
        else:
            messages.error(request, form.errors)
            return redirect(reverse('accounts:profile'))


class ChangePasswordView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user)
        context = {"form": form}
        return render(request, "registration/password_change_form.html", context)

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated.")
            return redirect(reverse('myapp:index'))
        else:
            messages.error(request, form.errors)
            return redirect(reverse('accounts:change_password'))
