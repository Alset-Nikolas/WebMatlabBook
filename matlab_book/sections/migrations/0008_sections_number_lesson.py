# Generated by Django 4.1.7 on 2023-03-01 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0007_alter_sectiontasks_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='sections',
            name='number_lesson',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
