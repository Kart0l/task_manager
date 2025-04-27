from django.utils.translation import gettext_lazy as _

# Role choices for user profiles
ROLE_CHOICES = [
    ("developer", _("Developer")),
    ("designer", _("Designer")),
    ("pm", _("Project Manager")),
    ("qa", _("QA Manager")),
    ("devops", _("DevOps")),
    ("user", _("User")),
]

# Task status choices
STATUS_CHOICES = [
    ("todo", _("To Do")),
    ("in_progress", _("In Progress")),
    ("done", _("Done")),
]

# Task priority choices
PRIORITY_CHOICES = [
    ("low", _("Low")),
    ("medium", _("Medium")),
    ("high", _("High")),
]

# Task type choices
TASK_TYPE_CHOICES = [
    ("bug", _("Bug")),
    ("new_feature", _("New Feature")),
    ("refactoring", _("Refactoring")),
    ("qa", _("QA")),
    ("breaking_change", _("Breaking Change")),
]

# Task type colors
TASK_TYPE_COLORS = {
    "bug": "#FF0000",  # red
    "new_feature": "#00FF00",  # green
    "refactoring": "#FFFF00",  # yellow
    "qa": "#0000FF",  # blue
    "breaking_change": "#FF00FF",  # magenta
} 