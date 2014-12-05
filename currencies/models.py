from decimal import ROUND_HALF_UP, Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from . import validators


class Currency(models.Model):

    OPENEXCHANGERATES = 'openexchangerates'

    #TODO: perhaps refactor this to be generated from a settings config
    SOURCE_CHOICES = (
        (OPENEXCHANGERATES, _('OpenExchangeRates')),)

    code = models.CharField(_('code'), max_length=3, unique=True)
    name = models.CharField(_('name'), max_length=35)
    symbol = models.CharField(_('symbol'), max_length=4, blank=True)
    factor = models.DecimalField(_('factor'), max_digits=30, decimal_places=10,
        help_text=_('Specifies the difference of the currency to base one.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('The currency will be available.'))
    is_base = models.BooleanField(_('base'), default=False,
        help_text=_('Make this the base currency against which rates are calculated.'))
    rounding = models.CharField(_('rounding rules'), max_length=30,
        default=".01|%s" % ROUND_HALF_UP,
        validators=[validators.RoundingRuleValidator],
        help_text=_('Rounding rules for this currency. An exponent and a flag joined by |. E.g: ".01|ROUND_UP"'))
    source = models.CharField(_('Rates source'), max_length=50,
        choices=SOURCE_CHOICES,
        default=OPENEXCHANGERATES,
        help_text=_('Specifies the source service to use updating rates.'))
    rate_interval = models.PositiveIntegerField(_('Rates update interval'), default=3600,
        help_text=_('interval, in seconds, at which this currency is updated from its source. Defaults to 1 hour.'))

    class Meta:
        ordering = ('name', )
        verbose_name = _('currency')
        verbose_name_plural = _('currencies')

    def __unicode__(self):
        return self.code

    def save(self, **kwargs):
        # Make sure the base and default currencies are unique
        if self.is_base:
            Currency.objects.filter(is_base=True).update(is_base=False)
        super(Currency, self).save(**kwargs)

    def round(self, value):
        rules = self.rounding.split('|')
        return Decimal(value).quantize(Decimal(rules[0]), rounding=rules[1])

    def to_base(self, price):
        from . import utils
        return utils.price_to_base(price, self)

    @classmethod
    def price_to_base(cls, price, code):
        return cls.objects.get(code__exact=code).to_base(price)