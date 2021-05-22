class Template:

    def __init__(self, *valid_types):
        self.valid_types = valid_types

        assert all(
            isinstance(cur, (type, Template))
            for cur in valid_types
        )

    def check(self, data):

        for valid_type in self.valid_types:
            if isinstance(valid_type, Template):
                try:
                    valid_type.check(data)
                    return
                except:
                    continue

            if isinstance(data, valid_type):
                return

        assert False


class TemplateList(Template):

    def __init__(self, *valid_types):
        super().__init__(list, tuple)
        self.element_template = Template(*valid_types)

    def check(self, data):
        super().check(data)
        for element in data:
            self.element_template.check(element)


class TemplateDict(Template):

    def __init__(self, **template):
        super().__init__(dict)

        self.template = template

        assert all(
            isinstance(value, Template)
            for value in template.values()
        )

    def check(self, data):
        super().check(data)

        assert all(
            key in data
            for key in self.template
        )

        for key in self.template:
            self.template[key].check(data[key])
