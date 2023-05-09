from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime


# Create your models here.

# create a user profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # follows = models.ManyToManyField('self',
    # related_name='followed_by',
    # symmetrical=False,
    # blank=True)
    def __str__(self):
        return self.user.username


# create profile when new user signs up
def create_profile(sender, instance, created, **kwargs):
    # print(sender, instance, created)
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
        ("food", "Food & Drinks"),
        ("shopping", "Shopping"),
        ("transport", "Transport"),
        ("travel", "Travel"),
        ("entertainment", "Entertainment"),
        ("comm", "Communication"),
        ("meds", "Meds"),
        ("stationary", "Stationary"),
        ("personal", "Personal"),
        ("edun", "Education"),
        ("other", "Other"),
    ]
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=30, blank=True)
    amount = models.IntegerField(blank=False)
    date = models.DateField(default=datetime.now)
    payment_mode = models.CharField(choices=PAYMENT_MODE_CHOICES, blank=False, max_length=6)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=15)

    def sum(self, category):
        sum = 0
        print(self.objects.filter(category=category))
        for expense in self.objects.filter(category=category):
            sum += expense.amount
        return sum


    def __str__(self):
        return self.description

    # find out what meta does:??
    class Meta:
        pass
