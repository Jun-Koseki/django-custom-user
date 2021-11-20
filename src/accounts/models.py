from django.db import models
from django.utils.timezone import localtime
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from datetime import timedelta


def get_password_limit():
    try:
        limit = int(getattr(settings, "PASSWORD_EXPIRY"))
    except ValueError:
        raise Exception(
            "PASSWORD_EXPIRY" " needs to be an integer"
        )
    return limit


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=150)
    email = models.EmailField(_('email'), unique=True)
    bio = models.TextField(_('bio'), blank=True)
    website = models.URLField(_('website'), blank=True)
    last_modified_pw = models.DateTimeField(_('パスワード更新日時'), default=localtime())

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.original_password = self.password

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

        if self.__password_has_been_changed():
            UserPasswordHistory.remember_password(self)
            self.last_modified_pw = localtime()
            super(User, self).save(*args, **kwargs)

        return self

    def password_has_been_expired(self):
        password_period = localtime() - self.last_modified_pw
        if password_period > timedelta(seconds=get_password_limit()):
            return True
        else:
            return False

    def __password_has_been_changed(self):
        return self.original_password != self.password


class UserPasswordHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=150)
    use_from = models.DateTimeField(blank=True)

    @classmethod
    def remember_password(cls, user):
        cls(user=user, password=user.password, use_from=localtime()).save()
