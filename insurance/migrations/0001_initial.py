import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InsurancePrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('sex', models.CharField(max_length=10)),
                ('bmi', models.FloatField(verbose_name='BMI')),
                ('children', models.IntegerField(default=0)),
                ('smoker', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3)),
                ('region', models.CharField(choices=[('northeast', 'Northeast'), ('northwest', 'Northwest'), ('southeast', 'Southeast'), ('southwest', 'Southwest')], max_length=20)),
                ('predicted_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insurance_predictions', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
