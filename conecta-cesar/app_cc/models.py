from django.db import models

# Create your models here.

class Login(models.Model): 
    email=models.CharField(max_length=100, null=False)
    password=models.CharField(max_length=100, null=False)
    date_added=models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    problem=models.CharField(max_length=200, null=False)
    details = models.TextField()
    created_date = models.DateTimeField("Created on")

def __str__(self):
    return self.email, self.password, self.date_added

class Entry(models.Model):
    topic=models.ForeignKey(Question, on_delete=models.CASCADE)
    text=models.TextField()
    def __str__(self):
        return self.text
    class Meta:
        verbose_name_plural='Entries'
