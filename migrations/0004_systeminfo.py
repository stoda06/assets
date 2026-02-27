from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_delete_systeminfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('processor', models.CharField(max_length=255)),
                ('serial_number', models.CharField(max_length=255, unique=True)),
                ('memory', models.CharField(max_length=50)),
                ('disk_size', models.CharField(max_length=50)),
                ('Username', models.CharField(blank=True, default='', max_length=255)),
                ('Location_name', models.CharField(blank=True, default='', max_length=255)),
                ('system_name', models.CharField(blank=True, default='', max_length=255)),
                ('asset_id', models.CharField(blank=True, default='', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'app_label': 'assets',
            },
        ),
    ]
