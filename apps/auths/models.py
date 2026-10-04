from django.db import models

from typing import Any

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from django.core.exceptions import ValidationError

from django.db.models import (
    EmailField,
    CharField,
    BooleanField,
)


class UserManager(BaseUserManager):

    def __obtain_user_instance(
        self,
        email: str,
        password: str,
        **kwargs: dict[str, Any],
    ) -> 'User':
        """Get user instance."""
        if not email:
            raise ValidationError(
                message="Email field is required", code="email_empty"
            )
        # if not full_name:
        #     raise ValidationError(
        #         message="Full name name is required.", code="full_name_empty"
        #     )

        new_user: 'User' = self.model(
            email=self.normalize_email(email),
            password=password,
            **kwargs,
        )
        return new_user

    def create_user(
            self,
            email: str,
            password: str | None = None,
            **kwargs: dict[str, Any],
    ) -> 'User':
        
        new_user: 'User' = self.__obtain_user_instance(
            email=email,
            password=password,
            **kwargs,
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user

    def create_superuser(
                self,
                email: str,
                password: str | None = None,
                **kwargs: dict[str, Any],
        ) -> 'User':
            
            new_user: 'User' = self.__obtain_user_instance(
                email=email,
                password=password,
                is_stuff=True,
                is_superuser=True,
                **kwargs,
            )
            new_user.set_password(password)
            new_user.save(using=self._db)
            return new_user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=150, unique=True, db_index=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
         return super().__str__()