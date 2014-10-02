from django.db import models
from django.utils.translation import gettext_lazy as _
from . import utils


class Currency(models.Model):

    OPENEXCHANGERATES = 'openexchangerates'

    #TODO: perhaps refactor this to be generated from a settings config
    SOURCE_CHOICES = (
        (OPENEXCHANGERATES, _('OpenExchangeRates')),)

    code = models.CharField(_('code'), max_length=3)
    name = models.CharField(_('name'), max_length=35)
    symbol = models.CharField(_('symbol'), max_length=4, blank=True)
    factor = models.DecimalField(_('factor'), max_digits=30, decimal_places=10,
        help_text=_('Specifies the difference of the currency to base one.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('The currency will be available.'))
    is_base = models.BooleanField(_('base'), default=False,
        help_text=_('Make this the base currency against which rates are calculated.'))
    is_default = models.BooleanField(_('default'), default=False,
        help_text=_('Make this the default user currency.'))
    source = models.CharField(_('Rates source'), max_length=50,
        choices=SOURCE_CHOICES,
        default=OPENEXCHANGERATES,
        help_text=_('Specifies the source service to use updating rates.'))
    rate_interval = models.PositiveIntegerField(_('Rates update interval'), default=3600,
        help_text=_('intervals at which this currency is updated from its source. Defaults to 1 hour.'))

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
        if self.is_default:
            Currency.objects.filter(is_default=True).update(is_default=False)
        super(Currency, self).save(**kwargs)

    def to_base(self, price):
        return utils.price_to_base(price, self)

    @classmethod
    def price_to_base(cls, price, code):
        return cls.objects.get(code__exact=code).to_base(price)