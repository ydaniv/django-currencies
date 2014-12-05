from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _


class RoundingRuleValidator(RegexValidator):

    regex = r'^(\d+\.?|\d*\.\d+)([eE]-?\d+)?\|' \
            r'(ROUND_DOWN|ROUND_HALF_UP|ROUND_HALF_EVEN|ROUND_CEILING|ROUND_FLOOR|ROUND_UP|ROUND_HALF_DOWN|ROUND_05UP)$'
    message = _('Enter a valid decimal rounding exponent and flag (e.g: `1.|ROUND_HALF_UP`).')
