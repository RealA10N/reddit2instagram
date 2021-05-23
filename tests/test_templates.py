import math
import pytest
from reddit2instagram.templates import Template, TemplateCheckError


class ExampleObject: pass
class ExampleTwo(ExampleObject): pass
class AnotherObject: pass


class TestTemplateChecks:

    @pytest.mark.parametrize('template_type, data', [
        (str, 'string'),
        (int, 123),
        (float, 21.02),
        (list, [1, 'string!', 12.34, ExampleObject, AnotherObject()]),
        (set, set()),
        (ExampleObject, ExampleObject()),
        (ExampleObject, ExampleTwo()),
    ])
    def test_basic_template_check(self, template_type, data):
        """ Multiple scenarios where the basic template check shouldn't fail """
        Template(template_type).check(data)

    @pytest.mark.parametrize('template_type, data', [
        (str, 123),
        (int, 'not a number'),
        (float, 123),
        (list, 'str'),
        (list, ('not', 'a', 'list!',)),
        (tuple, range(10)),
        (ExampleObject, AnotherObject()),
        (ExampleTwo, ExampleObject()),
    ])
    def test_basic_template_check_fail(self, template_type, data):
        """ Multiple scenarios where the basic template check should fail """
        with pytest.raises(TemplateCheckError):
            Template(template_type).check(data)

    @pytest.mark.parametrize('template_type', [str, int, float, list, dict, set])
    def test_basic_template_type_fail(self, template_type):
        """ When a template recives an object class (and not an instance),
        it should raise an template check error. """
        with pytest.raises(TemplateCheckError):
            Template(template_type).check(template_type)

    @pytest.mark.parametrize('valid_types, data_collection', [
        pytest.param(
            (int, float, complex),
            (1, math.inf, math.pi, math.sqrt(2), complex(1, 2), complex(1, 0)),
            id='numbers',
        ),
        pytest.param(
            (list, tuple, set),
            ([1, 2, 3], (1, 2, 3), {1, 2, 3},
             ['hello', 123, list], tuple()),
            id='collections',
        )
    ])
    def test_basic_template_multiple_accepted_values(self, valid_types, data_collection):
        template = Template(*valid_types)
        for data in data_collection:
            template.check(data)
