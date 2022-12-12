from django.db import models

# Create your models here.

class Chat(models.Model): # new
    text = models.TextField() 
    
    def __str__(self):
        return self.text