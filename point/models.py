from django.db import models

# Create your models here.

class History(models.Model):
    id = models.IntegerField(primary_key=True)
    area = models.ForeignKey(to='area.Area', on_delete=models.CASCADE)
    user = models.ForeignKey(to='accounts.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    gain = models.IntegerField()
    total = models.IntegerField()
    reason = models.CharField(max_length=100, default="")