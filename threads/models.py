from django.conf import settings
from django.db import models
from django.urls import reverse


class Thread(models.Model): # model for our threads feature 
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    
    class Meta:
        ordering = ['-id']  # reverses the order TODO add the upvote functionality

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("thread_detail", kwargs={"pk": self.pk})
    
    
class Comment(models.Model):  # the model for our comments section
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    comment = models.CharField(max_length=140)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse("thread_detail", kwargs={"pk": self.pk})