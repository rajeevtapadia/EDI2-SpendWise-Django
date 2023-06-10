from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime


# Create your models here.

# create a user profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balence = models.IntegerField(blank=False, default=0)
    def __str__(self):
        return self.user.username


# create profile when new user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=User)


# expense model
class Expense(models.Model):
    # actual value: human readable name
    PAYMENT_MODE_CHOICES = [
        ("UPI", "UPI"),
        ("Cash", "Cash"),
        ("DCard", "Debit Card"),
        ("CCard", "Credit Card"),
    ]
    CATEGORY_CHOICES = [
        ("Food & Drinks", "Food & Drinks"),
        ("Shopping", "Shopping"),
        ("Transport", "Transport"),
        ("Travel", "Travel"),
        ("Entertainment", "Entertainment"),
        ("Communication", "Communication"),
        ("Meds", "Meds"),
        ("Stationary", "Stationary"),
        ("Personal", "Personal"),
        ("Education", "Education"),
        ("Other", "Other"),
    ]
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=30, blank=True)
    amount = models.IntegerField(blank=False)
    date = models.DateField(default=datetime.now)
    payment_mode = models.CharField(choices=PAYMENT_MODE_CHOICES, blank=False, max_length=6)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=15)

    def sum(self, category, user):
        sum = 0
        if category == 'all':
            for expense in self.objects.filter(profile=user):
                sum += expense.amount
        else:
            for expense in self.objects.filter(profile=user, category=category):
                sum += expense.amount
        return sum


    def __str__(self):
        return self.description

    # find out what meta does:??
    class Meta:
        pass
