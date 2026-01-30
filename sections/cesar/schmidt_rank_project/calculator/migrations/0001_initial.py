# Generated manually for schmidt_rank_project

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calculation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_vector', models.TextField(help_text='JSON array of state vector components')),
                ('dimension_a', models.IntegerField(help_text='Dimension of subsystem A')),
                ('dimension_b', models.IntegerField(help_text='Dimension of subsystem B')),
                ('state_name', models.CharField(blank=True, help_text="Optional name for the state (e.g., 'Bell State')", max_length=200)),
                ('schmidt_rank', models.IntegerField(help_text='Schmidt rank of the state')),
                ('schmidt_coefficients', models.TextField(help_text='JSON array of Schmidt coefficients')),
                ('is_entangled', models.BooleanField(help_text='Whether the state is entangled')),
                ('entropy', models.FloatField(help_text='Von Neumann entropy')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, help_text='Optional notes about the calculation')),
            ],
            options={
                'verbose_name': 'Calculation',
                'verbose_name_plural': 'Calculations',
                'ordering': ['-created_at'],
            },
        ),
    ]
