import typing
import pytest

import os

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

from reddit2instagram.templates.path import (
    TemplatePath,
    TemplateCheckPathNotFoundError,
)


def validate(template, data):
    return template.validate(
        HeadContainer(data),
        RaiseOnError(),
    )


@pytest.mark.parametrize('color, expected', [
    pytest.param(color, expected, id=str(color))
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
def test_template_color(color, expected: Exception):

    if expected is None:
        validate(TemplateColor(), color)

    else:
        with pytest.raises(expected):
            validate(TemplateColor(), color)


@pytest.mark.parametrize('path, expected', [
    pytest.param(path, expected, id=str(path))
    for path, expected in (
        (__file__, None),
        (os.path.dirname(__file__), None),
        ('.', None),
        ('./notAfolDer/', TemplateCheckPathNotFoundError),
        ('notAfilE.txt', TemplateCheckPathNotFoundError),
    )
])
def test_template_path(path: str, expected: Exception):

    if expected is None:
        validate(TemplatePath(), path)

    else:
        with pytest.raises(expected):
            validate(TemplatePath(), path)
