""" Special templates that are based on the basic templates, and are used to
build the workflow template. """

from .basic import (
    Template,
    TemplateList,
    TemplateDict,
)


class TemplateRedditCredentials(TemplateDict):

    def __init__(self):
        super().__init__(
            id=Template(str),
            secret=Template(str),
        )


class TemplateInstagramCredentials(TemplateDict):

    def __init__(self):
        super().__init__(
            username=Template(str),
            password=Template(str),
        )


class TemplateJob(TemplateDict):
    def __init__(self):
        super().__init__(
            name=Template(str),
            subreddits=TemplateList(str),
        )


class TemplateWorkflow(TemplateDict):
    def __init__(self):
        super().__init__(
            credentials=TemplateDict(
                reddit=TemplateRedditCredentials(),
                instagram=TemplateInstagramCredentials(),
            ),
            jobs=TemplateList(
                TemplateJob(),
            )
        )
