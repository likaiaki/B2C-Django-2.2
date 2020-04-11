from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserManager(BaseUserManager):
    # use_in_migrations = True
    def create(self, **extra_fields):
        print(extra_fields["mobile"])
        if extra_fields.get("mobile", None) is None:
            raise ValueError("请填入手机号码！")
        user = self.model(
            **extra_fields
        )
        user.set_password(extra_fields.get("password"))
        user.save()
        return user


class User(AbstractUser):
    GENDER_CHOICES = (
        (0, "男"),
        (1, "女")
    )
    username = models.CharField(max_length=150, null=True, unique=False, verbose_name="用户名子")
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    avatar_url = models.CharField(max_length=256, null= True, verbose_name="头像路径")
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    USERNAME_FIELD = "mobile"
    objects = UserManager()

    class Meta:
        db_table = "tb_user"  # 指明数据库的名称
        verbose_name = "用户"  # 在addmin显示额名称
        verbose_name_plural = "verbose_name"  # 显示复数名称


class Blog(models.Model):
    title = models.CharField(max_length=256, null=False, verbose_name="新闻标题")
    content =models.TextField(null=False, verbose_name="新闻内容")
    status = models.SmallIntegerField(default=0, verbose_name="新闻状态")  # 当前博客状态 如果为0代表审核通过，1代表审核中，-1代表审核不通过p
    user = models.ForeignKey(User, to_field="mobile", on_delete=models.PROTECT, verbose_name="用户id")
    clicks = models.IntegerField(default=0, verbose_name="浏览量")

    class Meta:
        db_table = "tb_blog"  # 指明数据库的名称
        verbose_name = "博客"  # 在addmin显示额名称
        verbose_name_plural = "verbose_name"  # 显示复数名称


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null= True, verbose_name="博客id")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null= True, verbose_name="用户id")
    create_time = models.DateTimeField(verbose_name="评论时间")
    content = models.CharField(max_length=500, verbose_name="评论内容")
    parent = models.ForeignKey('Comment', on_delete=models.PROTECT, null=True, verbose_name="父评论id")

    class Meta:
        db_table = "tb_comment"
        verbose_name = "微博评论"  # 在admin显示额名称
        verbose_name_plural = "verbose_name"  #c显示复数名称

