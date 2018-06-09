from django.urls import path
from . import views

app_name = 'triptech_web'
urlpatterns = [
    # ex: /triptech_web/
    path('', views.FileView.as_view(), name='files'),
    # ex: /triptech_web/5
    path('<int:pk>/', views.data, name='data'),
    #ex: /assignments/
    path('assignments/', views.AssignmentView.as_view(), name='assignments')
]
