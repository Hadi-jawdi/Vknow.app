from django import forms

from .models import SATQuestion


class StartTestForm(forms.Form):
    section = forms.ChoiceField(choices=SATQuestion.Section.choices, label="Section")
    num_questions = forms.ChoiceField(
        choices=[("10", "10 questions"), ("20", "20 questions"), ("27", "27 questions (full R&W module)")],
        initial="10",
        label="Length",
    )
    domain = forms.ChoiceField(required=False, label="Focus on a specific domain (optional)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        domains = (
            SATQuestion.objects.values_list("domain", flat=True)
            .distinct()
            .order_by("domain")
        )
        self.fields["domain"].choices = [("", "All domains")] + [(d, d) for d in domains if d]
