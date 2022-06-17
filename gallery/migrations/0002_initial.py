# Generated by Django 3.2.5 on 2022-06-17 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gallery', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryvideo',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_video', to='accounts.account'),
        ),
        migrations.AddField(
            model_name='galleryimg',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_img', to='accounts.account'),
        ),
    ]
