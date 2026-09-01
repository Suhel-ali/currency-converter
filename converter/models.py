from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="profile_images/",
        default="profile_images/2.jpg"
    )

    def __str__(self):
        return self.user.username


class Conversion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    from_currency = models.CharField(max_length=10)
    to_currency = models.CharField(max_length=10)

    amount = models.DecimalField(max_digits=15, decimal_places=2)
    rate = models.DecimalField(max_digits=15, decimal_places=6)
    converted_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    conversion_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_currency} → {self.to_currency}"


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    from_currency = models.CharField(max_length=10)
    to_currency = models.CharField(max_length=10)

    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_currency} → {self.to_currency}"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    message = models.TextField()
    submitted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username




class Feedback(models.Model):

     user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

     comment = models.TextField()

     submitted_date = models.DateTimeField(
        auto_now_add=True ,null=True)
     def __str__(self):
        return self.user.username