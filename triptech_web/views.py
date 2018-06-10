from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.utils import timezone
from django.urls import reverse
from django.views import generic

from .models import Filenames, Data, Assignments, Submissions
from .forms import NewAssignmentForm, NewSubmissionForm

from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Select
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components, file_html


# Create your views here.
class FileView(generic.ListView):
    template_name = 'triptech_web/files.html'
    context_object_name = 'filename_list'

    def get_queryset(self):
        """
        Returns the files currently in the system
        """
        return Filenames.objects.all()


class AssignmentView(generic.ListView):
    template_name = 'triptech_web/assignment_list.html'
    context_object_name = 'assignment_list'

    def get_queryset(self):
        """
        Returns the assignments currently available from the database
        :return:
        """
        return Assignments.objects.all()


class SubmissionView(generic.ListView):
    template_name = 'triptech_web/submission_list.html'
    context_object_name = 'submission_list'

    def get_queryset(self):
        """
        Returns the submissions currently available from the database
        :return:
        """
        pk = self.kwargs['pk']
        return Submissions.objects.filter(assignment_id=pk)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['assignment'] = Assignments.objects.filter(pk=self.kwargs['pk'])[0].title
        return context


def assignment_details(request, pk):

    if request.method == 'POST':
        a = Assignments.objects.get(pk=pk)
        a.delete()
        return HttpResponseRedirect(reverse('triptech_web:assignments'))

    assignment = Assignments.objects.get(pk=pk)

    context = {
        'title': assignment.title,
        'date_created': assignment.date_created,
        'text': assignment.text,
        'pk': pk
    }

    return render(request, 'triptech_web/assignment_view.html', context)


def new_assignment(request):

    if request.method == 'POST':
        form = NewAssignmentForm(request.POST)
        if form.is_valid():
            a = Assignments(title=form.cleaned_data['assignment_name'], date_created=timezone.now(),
                            text=form.cleaned_data['assignment_description'], metadata1='', metadata2='')
            a.save()
            return HttpResponseRedirect(reverse('triptech_web:assignments'))
    else:
        form = NewAssignmentForm()

    return render(request, 'triptech_web/assignment_new.html', {'form': form})


def edit_assignment(request, pk):

    if request.method == 'POST':
        form = NewAssignmentForm(request.POST)
        if form.is_valid():
            a = Assignments.objects.get(pk=pk)
            a.title = form.cleaned_data['assignment_name']
            a.text = form.cleaned_data['assignment_description']
            a.save()
            return HttpResponseRedirect(reverse('triptech_web:view_assignment', kwargs={'pk': pk}))
    else:
        assignment = Assignments.objects.get(pk=pk)
        form = NewAssignmentForm({'assignment_name': assignment.title, 'assignment_description': assignment.text})

    return render(request, 'triptech_web/assignment_edit.html', {'form': form, 'pk': pk})


def submission_details(request, pk, pk_sub):
    submission = Submissions.objects.get(pk=pk_sub)

    context = {
        'student_name': submission.student_name,
        'date': submission.date,
        'assignment': Assignments.objects.filter(pk=pk)[0].title,
        'data_location': submission.data_location,
        'pk': pk,
        'pk_sub': pk_sub
    }

    return render(request, 'triptech_web/submission_view.html', context)


def submission_new(request, pk):
    if request.method == 'POST':
        form = NewSubmissionForm(request.POST)
        if form.is_valid():
            s = Submissions(student_name=form.cleaned_data['student_name'], date=timezone.now(),
                            data_location=form.cleaned_data['data_location'],
                            metadata1='', metadata2='', assignment_id=pk)
            s.save()
            return HttpResponseRedirect(reverse('triptech_web:submissions', kwargs={'pk': pk}))
    else:
        form = NewSubmissionForm()

    return render(request, 'triptech_web/submission_new.html', {'form': form, 'pk': pk})


def submission_edit(request, pk, pk_sub):
    if request.method == 'POST':
        form = NewSubmissionForm(request.POST)
        if form.is_valid():
            s = Submissions.objects.get(pk=pk_sub)
            s.student_name = form.cleaned_data['student_name']
            s.data_location = form.cleaned_data['data_location']
            s.save()
            return HttpResponseRedirect(reverse('triptech_web:submissions_view', kwargs={'pk': pk, 'pk_sub': pk_sub}))
    else:
        sub = Submissions.objects.get(pk=pk_sub)
        form = NewSubmissionForm({'student_name': sub.student_name, 'data_location': sub.data_location})

    return render(request, 'triptech_web/submission_edit.html', {'form': form, 'pk': pk, 'pk_sub': pk_sub})


def data(request, pk, **kwargs):

    plot_type = None

    for name, value in kwargs.items():
        if name == 'plot_type':
            plot_type = value

    if plot_type == None:
        plot_type = 'line'

    x = []
    y = []

    file = Filenames.objects.get(pk=pk)

    for datapoint in file.data_set.all():
        x.append(datapoint.voltage)
        y.append(datapoint.current)

    title = file.filename
    plot = figure(title=title,
                  x_axis_label='Voltage [V]',
                  y_axis_label='Current [A]',
                  plot_width=650,
                  plot_height=650,)

    if len(x) <= 1:
        plot_type = 'scatter'

    if plot_type == 'line':
        plot.line(x, y, line_width=2)
    elif plot_type == 'scatter':
        plot.scatter(x, y, line_width=2)
    elif plot_type == 'hbar':
        plot.hbar(x, y)
    elif plot_type == 'vbar':
        plot.vbar(x, y)

    script, div = components(plot)

    type = Select(title='Plot Type:', value='line', options=['scatter', 'hbar', 'vbar'])

    controls = [type]
    """
    for control in controls:
        control.on_change('value', lambda attr, old, new: update())
    """
    source = ColumnDataSource(data=dict(x=[], y=[], color=[], voltage=[], current=[]))
    TOOLTIPS=[
        ('Voltage', '@voltage'),
        ('Current', '@current')
    ]

    type_script, type_div = components(widgetbox(type))

    context = {
        'filenames': file,
        'script': script,
        'div': div,
        'type_script': type_script,
        'type_div': type_div
    }

    return render_to_response('triptech_web/data.html', context)
