from django.db import models

class Games(models.Model):
    game_name = models.CharField(max_length=200)
    game_file_link = models.CharField(max_length=200)
    file_location = models.CharField(max_length=200)
    game_year = models.IntegerField()
    cover = models.CharField(max_length=200)
    rma_file = models.FileField(upload_to='rmaFolder/', blank=True)
    def __str__(self):
        return self.game_name