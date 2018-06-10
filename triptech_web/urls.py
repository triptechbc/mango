from django.urls import path
from . import views

app_name = 'triptech_web'
urlpatterns = [
    # ex: /triptech_web/
    path('', views.FileView.as_view(), name='files'),
    # ex: /triptech_web/5
    path('<int:pk>/', views.data, name='data'),
    # ex: /assignments/
    path('assignments/', views.AssignmentView.as_view(), name='assignments'),
    # ex: /assignments/new
    path('assignments/new/', views.new_assignment, name='new_assignment'),
    # ex: /assignments/5
    path('assignments/<int:pk>', views.assignment_details, name='view_assignment'),
    # ex: /assignments/5/edit
    path('assignments/<int:pk>/edit', views.edit_assignment, name='edit_assignment'),
    # ex: /assignment/5/submissions/
    path('assignments/<int:pk>/submissions/', views.SubmissionView.as_view(), name='submissions'),
    # es: /assignment/5/submissions/new
    path('assignments/<int:pk>/submissions/new', views.submission_new, name='submissions_new'),
    # ex: /assignment/5/submissions/1
    path('assignments/<int:pk>/submissions/<int:pk_sub>', views.submission_details, name='submissions_view'),
    # ex: /assignments/5/submissions/1/edit
    path('assignments/<int:pk>/submissions/<int:pk_sub>/edit', views.submission_edit, name='submissions_edit')
]
