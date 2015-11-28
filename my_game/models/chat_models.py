# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime


class Chat(models.Model):
    class Meta:
        db_table = 'chat'

    user = models.CharField(max_length=32)
    user_id = models.IntegerField(db_index=True, default=1)
    text = models.CharField(max_length=64)
    time = models.DateTimeField(default=datetime.now, blank=True)


class ChatPrivate(models.Model):
    class Meta:
        db_table = 'chat_private'

    user_id = models.IntegerField(default=1)
    user = models.CharField(max_length=20)
    recipient = models.IntegerField()
    recipient_name = models.CharField(max_length=20)
    text = models.CharField(max_length=64)


class UserChatOnline(models.Model):
    class Meta:
        db_table = 'user_chat_online'

    user_id = models.IntegerField(db_index=True)
    user = models.CharField(max_length=20)
    last_time_update = models.DateTimeField()
