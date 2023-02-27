from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


class Topic(models.Model):
    class Meta:
        verbose_name = "话题"
        verbose_name_plural = "话题"

    def __str__(self):
        return self.content

    TYPE_CHOICES = [
        ('S', '单选'),
        ('M', '多选')
    ]

    starter = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    content = models.CharField(
        verbose_name="话题内容",
        max_length=200,
    )

    type = models.CharField(
        verbose_name="选项类型",
        choices=TYPE_CHOICES,
        default='S',
        max_length=10,
    )

    anonymous = models.BooleanField(
        verbose_name="是否记名",
    )

    pub_date = models.DateTimeField(
        verbose_name="发布时间",
    )

    begin_date = models.DateTimeField(
        verbose_name="开始时间",
    )

    end_date = models.DateTimeField(
        verbose_name="结束时间",
    )

    participant_num = models.IntegerField(
        verbose_name="总参与人数",
        default=0,
    )


class Choices(models.Model):
    class Meta:
        verbose_name = "选项"
        verbose_name_plural = "选项"

    def __str__(self):
        return self.description

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE
    )

    description = models.CharField(
        verbose_name="选项描述",
        max_length=100,
    )

    votes = models.IntegerField(
        verbose_name="选择人数",
        default=0,
    )
