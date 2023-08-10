from django.urls import path

from habit_app.apps import HabitAppConfig
from habit_app.views import HabitListView, HabitDetailView, PublicHabitListView

app_name = HabitAppConfig.name

urlpatterns = [
    path('habits/', HabitListView.as_view(), name='habit_list_create'),
    path('habits/<int:pk>/', HabitDetailView.as_view(), name='habit_retrieve_update_destroy'),
    path('habits/public/', PublicHabitListView.as_view(), name='public_habits_list')

]