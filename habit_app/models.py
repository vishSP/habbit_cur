from django.conf import settings
from django.db import models

from users.models import NULLABLE


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    place = models.CharField(max_length=255, verbose_name='место')
    time = models.TimeField(default='00:00:00', verbose_name='время')
    action = models.CharField(max_length=255, verbose_name='действие')
    is_good = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    linked_habit = models.ForeignKey('self', on_delete=models.SET_NULL, **NULLABLE, verbose_name='cвязанная привычка')
    frequency = models.PositiveSmallIntegerField(default=1, verbose_name='периодичность')
    reward = models.CharField(max_length=255, **NULLABLE, verbose_name='вознаграждение')
    execution_time = models.TimeField(default='00:02:00', verbose_name='время на выполнение привычки')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'

    def __str__(self):
        return f'{self.user} будет {self.action} в {self.time} в {self.place}'

