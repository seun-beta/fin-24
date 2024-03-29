import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class NumberValidator:
    def validate(self, password, user=None):
        if not re.findall(r"\d", password):
            raise ValidationError(
                _("The password must contain at least 1 digit, 0-9."),
                code="password_no_number",
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 digit, 0-9.")


class UppercaseValidator:
    def validate(self, password, user=None):
        if not re.findall("[A-Z]", password):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter, A-Z."),
                code="password_no_upper",
            )

    def get_help_text(self):
        return _("Your password must contain at least 1 uppercase letter, A-Z.")


class SymbolValidator:
    def validate(self, password, user=None):
        if not re.findall("[()[\\]{}|\\`~!@#$%^&*_\\-+=;:'\",<>./?]", password):
            raise ValidationError(
                _(
                    "The password must contain at least 1 special character: "
                    + "()[]{}|\\`~!@#$%^&*_-+=;:'\",<>./?"
                ),
                code="password_no_symbol",
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 special character: "
            + "()[]{}|\\`~!@#$%^&*_-+=;:'\",<>./?"
        )
