from django.db import models

# Create your models here.

class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class ChatMessage(models.Model):
    sender = models.ForeignKey(RoomMember, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=500)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.name} ({self.room_name}): {self.message}"