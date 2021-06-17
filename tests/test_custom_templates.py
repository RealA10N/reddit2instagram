import pytest

from validit.utils import DefaultValue
from validit.containers import HeadContainer
from validit.errors.managers import TemplateCheckRaiseOnError as RaiseOnError
from validit.errors import (
    TemplateCheckInvalidDataError as InvalidDataError,
    TemplateCheckMissingDataError as MissingDataError,
)

from reddit2instagram.templates.color import (
    TemplateColor,
    TemplateCheckColorError,
)


@pytest.mark.parametrize('color, expected', [
    pytest.param(
        color,
        expected,
        id=str(color),
    )
    for color, expected in (
        ('#ffffff', None),
        ('red', None),
        ('hotpink', None),
        ('rgb(123, 234, 0)', None),
        ('rgb(255, 255, 304)', None),
        (None, InvalidDataError),
        (123, InvalidDataError),
        ((12, 23, 45), InvalidDataError),
        (0xffffff, InvalidDataError),
        (DefaultValue, MissingDataError),
        ('ffffff', TemplateCheckColorError),
        ('abcd', TemplateCheckColorError),
    )
])
def test_template_color(color, expected):

    def validate():
        TemplateColor().validate(
            HeadContainer(color),
            RaiseOnError(),
        )

    if expected is None:
        validate()

    else:
        with pytest.raises(expected):
            validate()
