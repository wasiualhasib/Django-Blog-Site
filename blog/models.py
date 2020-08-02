from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify




# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextUploadingField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    post_published=models.BooleanField(default=False)
    post_published_date=models.DateTimeField(blank=True,null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def post_content(self):
        self.content = ' '.join(self.content.split()[:35]) + ' ....'
        return self.content


    def publish(self):
        self.post_published =True
        self.post_published_date= timezone.now()
        self.save()

    def unPublish(self):
        self.post_published =False
        self.post_published_date=None
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    # class Meta:
    #     ordering = ['-date_posted']
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_absolute_slug(self):
        return reverse('post-detail', kwargs={'slug': slugify(self.title)})

    def update_post(self):
        return reverse('post-update', kwargs={'pk': self.pk})

    def delete_post(self):
        return reverse('post-delete', kwargs={'pk': self.pk})



class Comments(models.Model):
    post = models.ForeignKey(Post, related_name='comments',on_delete=models.CASCADE, null=True)
    author=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    comments = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text