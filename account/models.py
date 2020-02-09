from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# from django.contrib import auth

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField(blank=True, null=True,)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'profile for {self.user.username}'


class Contact(models.Model):
    user_from = models.ForeignKey(
        'auth.user', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(
        'auth.user', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


# add a field dynamically to the user model without directly modifying it(monkey patch)
User.add_to_class('following', models.ManyToManyField(
    'self', through=Contact, related_name='followers', symmetrical=False))
