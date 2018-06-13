from django import forms


# Create your forms here.
class NewAssignmentForm(forms.Form):
    assignment_name = forms.CharField(label='Assignment name', max_length=100)
    assignment_description = forms.CharField(label='Assignment Description', widget=forms.Textarea)


class NewSubmissionForm(forms.Form):
    student_name = forms.CharField(label='Student name', max_length=100)
    data_location = forms.CharField(label='Data location', max_length=260)
