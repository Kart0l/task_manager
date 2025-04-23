from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.template.loader import render_to_string
from .standart_value import STATUS_CHOICES, PRIORITY_CHOICES, TASK_TYPE_CHOICES

class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.Textarea, forms.DateTimeInput, forms.DateInput)):
                field.widget.attrs.update({"class": "form-control"})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({"class": "form-select"})

class TaskFilterMixin:
    STATUS_CHOICES = [("", _("All statuses"))] + STATUS_CHOICES
    PRIORITY_CHOICES = [("", _("All Prioritizes"))] + PRIORITY_CHOICES
    TASK_TYPE_CHOICES = [("", _("All types"))] + TASK_TYPE_CHOICES

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label=_("Status"))
    assignee = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        empty_label=_("All performers"),
        label=_("Performer")
    )
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False, label=_("Priority"))
    task_type = forms.ChoiceField(choices=TASK_TYPE_CHOICES, required=False, label=_("Task Type"))
    date_from = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False,
        label=_("Date from")
    )
    date_to = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False,
        label=_("Date to")
    )
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": _("Search by name or description")}),
        label=_("Search")
    )

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get("date_from")
        date_to = cleaned_data.get("date_to")
        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError(_("The start date cannot be later than the end date."))
        return cleaned_data

class AjaxFormMixin:
    action_type = None

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            action = self.action_type or "updated"
            return JsonResponse({
                "success": True,
                "message": f"{_('Task success')} {_(action)}"
            })
        return response

    def form_invalid(self, form):
        if self.request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "success": False,
                "errors": form.errors
            }, status=400)
        return super().form_invalid(form)

class AjaxActionMixin:
    def success_response(self, message):
        return JsonResponse({
            "success": True,
            "message": str(message)
        })

    def error_response(self, error, status=400):
        return JsonResponse({
            "success": False,
            "error": str(error)
        }, status=status)

class AjaxListMixin:
    ajax_template_name = None
    ajax_extra_data = {}

    def get(self, request, *args, **kwargs):
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            if not self.ajax_template_name:
                raise ValueError("Specify the ajax_template_name in the view")
            objects = self.get_queryset()
            context = self.get_context_data(objects=objects)
            html = render_to_string(self.ajax_template_name, context, request)
            response_data = {'html': html}
            response_data.update(self.ajax_extra_data)
            return JsonResponse(response_data)
        return super().get(request, *args, **kwargs)