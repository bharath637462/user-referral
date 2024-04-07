import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, is_staff=False, is_superuser=False, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    referral_code = models.CharField(max_length=36, null=True, blank=True)
    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True)
    is_staff = models.BooleanField(_('Staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    active = models.BooleanField(_('Active'), default=True)
    groups = models.ManyToManyField(Group, related_name='groups')

    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return f'{self.name}[{self.email}]'

    def has_perm(self, perms):
        if self.active and self.is_superuser:
            return True

        return False

    def has_module_perms(self, app_label):

        if self.active and self.is_superuser:
            return True

        return False

    class Meta:
        db_table = 'user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')