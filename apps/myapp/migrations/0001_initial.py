# Generated by Django 5.1.3 on 2024-11-07 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GL_AC_NO', models.BigIntegerField()),
                ('GL_AC_DESC', models.CharField(max_length=255)),
                ('Net_DR_CR', models.FloatField()),
                ('Converted_PnL', models.FloatField()),
                ('GL_RP_DT_PRE_TL', models.FloatField()),
                ('GL_RP_DT_CUR_TL', models.FloatField()),
                ('GL_RP_DIFF', models.FloatField()),
                ('FOX_CON_TL', models.FloatField()),
                ('DIFF', models.FloatField()),
                ('Comments', models.TextField()),
                ('UPSTREAM_REPORT_DATE', models.DateTimeField()),
                ('VERSION_ID', models.CharField(max_length=50)),
                ('LOAD_TIME_STAMP', models.DateTimeField()),
            ],
        ),
    ]
