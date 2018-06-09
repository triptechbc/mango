from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.urls import reverse
from django.views import generic
from .models import Filenames, Data, Assignments, Submissions
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
