import datetime
from enum import Enum


class YoutrackPriorities(Enum):
    HOTFIXES = ['ShowStopper', 'Blocker', 'Critical']
    FEATURES = ['Normal', 'Minor']


class Issue:
    def __init__(self, fields, complete=False):
        self.id = fields['project']['shortName'] + "-" + str(fields['numberInProject'])
        self.summary = fields['summary']
        self.branch = self.id + "-" + self.summary.replace(" ", "-")

        if complete:
            self.context = Context(fields)
            self.assignees = Assignees(fields)

        for field in filter(filter_header, fields['fields']):
            setattr(self,
                    field['projectCustomField']['field']['name'].lower(),
                    field['value']['name'])

        self.type = 'hotfix' if self.priority in YoutrackPriorities.HOTFIXES.value else 'feature'

    def __str__(self):
        return str({"id": self.id, "summary": self.summary, "state": self.state, "priority": self.priority})


class Context:
    def __init__(self, fields):
        self.created = datetime.datetime.fromtimestamp(
            fields['created'] / 1000).strftime("%B %d, %Y")
        self.reporter = fields['reporter']['name']
        self.description = fields['description']

    def __str__(self):
        return str({"created": self.created, "reporter": self.reporter, "description": self.description})


class Assignees:
    def __init__(self, fields):
        self.listedAssignees = {}

        for field in filter(filter_assignees, fields['fields']):
            if field['value']:
                self.listedAssignees[field['projectCustomField']
                                     ['field']['name']] = field['value']['name']

    def __str__(self):
        return str(self.listedAssignees)


def filter_header(field):
    return field['projectCustomField']['field']['name'] in ["State", "Priority"]


def filter_assignees(field):
    values = ["Responsable", "Revisor", "Diseñador(a)", "Code reviewer", "Jefe de proyecto"]
    return field['projectCustomField']['field']['name'] in values
