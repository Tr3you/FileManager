from django.db import models

class User(models.Model):
    email = models.EmailField()
    password = models.CharField()

    def __str__(self):
        return self.email

class File(models.Model):
    name = models.CharField(max_length=200)
    size = models.IntegerField()
    type = models.CharField(max_length=200)
    last_modified = models.DateField()
    date_deleted = models.DateField(null=True)
    date_updated = models.DateField()
    download_url = models.TextField()
    is_favorite = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name + " | " + self.type

