# Generated by Django 4.1.7 on 2023-03-02 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_alter_sectiontasks_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sectiontasks',
            name='path_script',
            field=models.FileField(blank=True, null=True, upload_to='staticfiles/tasks/matlab_scripts/'),
        ),
        migrations.AlterField(
            model_name='sectiontasks',
            name='path_test',
            field=models.FileField(blank=True, null=True, upload_to='staticfiles/tasks/tests/'),
        ),
    ]
