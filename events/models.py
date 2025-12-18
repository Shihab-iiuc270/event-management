from django.db import models

class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateField()     
    time = models.TimeField()        
    location = models.CharField(max_length=255)
    category = models.ForeignKey("Category", on_delete=models.CASCADE,default=1)
    assign_to = models.ManyToManyField(Participant, related_name='events')

    def __str__(self):
        return self.name
    
  

class Category(models.Model):
    name = models.CharField(max_length=200,unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name