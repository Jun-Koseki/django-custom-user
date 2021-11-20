from django.shortcuts import render, redirect, reverse, resolve_url
import logging


logger = logging.getLogger(__name__)


class PasswordChangeRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.password_has_been_expired():
            path = "{}?next={}".format(reverse("accounts:change_password"), request.path)
            return redirect(path)
        else:
            logger.warning(request.path)
        return super().dispatch(request, *args, **kwargs)

