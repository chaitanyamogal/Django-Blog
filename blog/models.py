from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title= models.CharField(max_length=255)
    # content = models.TextField()
    # content = RichTextField()
    content = RichTextUploadingField(config_name='default')
    author = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    timeStamp = models.DateTimeField(blank=True)

    def __str__(self):
        return "Title : " + self.title 

class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(default=now)
