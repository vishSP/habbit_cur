import datetime

from rest_framework import serializers

from habit_app.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = ('id', 'user', 'place', 'time', 'action',
                  'is_good', 'linked_habit', 'frequency',
                  'reward', 'execution_time', 'is_public')
        read_only_fields = ('id',)

    def validate(self, data):
        if data.get('linked_habit') and data.get('reward'):
            raise serializers.ValidationError("Нельзя одновременно указывать связанную привычку и вознаграждение")

        if data.get('execution_time') is not None:
            if data.get('execution_time') > datetime.time(hour=0, minute=2, second=0):
                raise serializers.ValidationError("Время выполнения не может превышать 120 секунд")

        if data.get('linked_habit') and not data.get('linked_habit').is_pleasurable:
            raise serializers.ValidationError("В связанные привычки можно добавлять только с признаком приятной")

        if data.get('is_good') and (data.get('reward') or data.get('linked_habit')):
            raise serializers.ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки")

        if data.get('frequency') is not None:
            if data.get('frequency') < 7:
                raise serializers.ValidationError("Периодичность не может быть реже, чем один раз в 7 дней")

        return data