from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


class Profile(models.Model):
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
        ('U', '未知')
    ]

    Exp = models.IntegerField(
        verbose_name='经验值',
    )

    Intro = models.TextField(
        verbose_name='个人简介',
        max_length='400'
    )

    Gender = models.CharField(
        verbose_name='性别',
        max_length=10,
        choices=GENDER_CHOICES,
        default='U'
    )

    Avatar = models.ImageField(
        upload_to='avatar/',
        verbose_name='头像',
        default='/media/avatar/Star for Van-500.png',
    )

    Balance = models.DecimalField(
        max_digits=65,
        decimal_places=2,
        verbose_name='余额'
    )


class History(models.Model):
    class Meta:
        verbose_name = '历史记录',
        verbose_name_plural = '历史记录'

    run_date = models.DateField(
        default=datetime.today,
        verbose_name='运行日期'
    )

    file_history = models.FileField(
        verbose_name='运行结果'
    )

    runner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    pass
