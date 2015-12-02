# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import currencies.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=3, verbose_name='code')),
                ('name', models.CharField(max_length=35, verbose_name='name')),
                ('symbol', models.CharField(max_length=4, verbose_name='symbol', blank=True)),
                ('factor', models.DecimalField(help_text='Specifies the difference of the currency to base one.', verbose_name='factor', max_digits=30, decimal_places=10)),
                ('is_active', models.BooleanField(default=True, help_text='The currency will be available.', verbose_name='active')),
                ('is_base', models.BooleanField(default=False, help_text='Make this the base currency against which rates are calculated.', verbose_name='base')),
                ('rounding', models.CharField(default=b'.01|ROUND_HALF_UP', help_text='Rounding rules for this currency. An exponent and a flag joined by |. E.g: ".01|ROUND_UP"', max_length=30, verbose_name='rounding rules', validators=[currencies.validators.RoundingRuleValidator])),
                ('source', models.CharField(default=b'openexchangerates', help_text='Specifies the source service to use updating rates.', max_length=50, verbose_name='Rates source', choices=[(b'openexchangerates', 'OpenExchangeRates')])),
                ('rate_interval', models.PositiveIntegerField(default=3600, help_text='interval, in seconds, at which this currency is updated from its source. Defaults to 1 hour.', verbose_name='Rates update interval')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'currency',
                'verbose_name_plural': 'currencies',
            },
        ),
    ]
