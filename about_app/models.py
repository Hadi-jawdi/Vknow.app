from django.db import models



class AboutUs(models.Model):
    text = models.TextField(null=True, blank=True)



    def __str__(self):
        return self.text[:20]