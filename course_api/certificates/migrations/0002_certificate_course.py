# Generated by Django 4.2.3 on 2023-07-14 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_initial'),
        ('certificates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='courses.course'),
            preserve_default=False,
        ),
    ]
