# Generated by Django 4.1.7 on 2023-03-01 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0006_alter_sectiontasks_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sectiontasks',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='sections.sections'),
        ),
    ]
