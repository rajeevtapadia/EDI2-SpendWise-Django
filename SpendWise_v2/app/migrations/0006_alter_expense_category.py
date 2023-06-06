# Generated by Django 4.2 on 2023-06-06 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_expense_balence_profile_balence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(choices=[('Food & Drinks', 'Food & Drinks'), ('Shopping', 'Shopping'), ('Transport', 'Transport'), ('Travel', 'Travel'), ('Entertainment', 'Entertainment'), ('Communication', 'Communication'), ('Meds', 'Meds'), ('Stationary', 'Stationary'), ('Personal', 'Personal'), ('Education', 'Education'), ('Other', 'Other')], max_length=15),
        ),
    ]
