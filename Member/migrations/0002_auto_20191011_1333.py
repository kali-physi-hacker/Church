# Generated by Django 2.2.6 on 2019-10-11 13:33

import Member.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shepherd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('age', models.PositiveIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='fathers_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='guardians_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='mothers_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='new_believer_school',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='pays_tithe',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='member',
            name='picture',
            field=models.ImageField(height_field=360, null=True, upload_to=Member.models.upload_image_path, width_field=360),
        ),
        migrations.AddField(
            model_name='member',
            name='working',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='member',
            name='ministry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Member.Ministry'),
        ),
        migrations.AlterField(
            model_name='member',
            name='telephone',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='shepherd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Member.Shepherd'),
        ),
    ]
