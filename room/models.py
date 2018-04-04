from django.db import models
#from account.models import User
from django.contrib.auth.models import User
#User = get_user_model()
from django.utils import timezone



# Create your models here.
class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=True)
    name = models.CharField(max_length=256)
    wins = models.PositiveIntegerField()
    loss = models.PositiveIntegerField()
    draw = models.PositiveIntegerField()
    games_played = models.PositiveIntegerField()


    class Meta:
        ordering = ["-wins"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Match(models.Model):
    p1_name = models.ForeignKey(Player, on_delete=models.CASCADE ,related_name='p1')
    p2_name = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='p2')
    p1_score = models.PositiveIntegerField()
    p2_score = models.PositiveIntegerField()
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_owner', null=True)

    class Meta:
        ordering = ["-date"]

    def save(self, *args, **kwargs):
        self.date = timezone.now()
        super().save(*args, **kwargs)
