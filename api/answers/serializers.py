u"""Сериализаторы для работы с ответами."""

from rest_framework.serializers import ModelSerializer

from core.models import AnswerForAskWithOneAnswer
from core.models import AnswerForAskWithMultipleAnswers

class AnswersForAskWithOneAnswerListSerializer(ModelSerializer):

    u"""Сериализатор для списка ответов на вопрос с одним ответом."""

    class Meta:
        model = AnswerForAskWithOneAnswer
        fields = (
            'id',
            'text',
        )

class AnswersForAskWithOneAnswerWriteSerializer(ModelSerializer):

    u"""Сериализатор записи ответов на вопрос с одним ответом."""

    class Meta:
        model = AnswerForAskWithOneAnswer
        fields = (
            'id',
            'text',
            'ask',
        )

class AnswersForAskWithMultipleAnswerListSerializer(ModelSerializer):

    u"""Сериализатор для ответов на вопросы с несколькими ответами."""

    class Meta:
        model = AnswerForAskWithMultipleAnswers
        fields = (
            'id',
            'text',
        )


class AnswersForAskWithMultipleAnswerWriteSerializer(ModelSerializer):

    u"""Сериализатор записи ответов на вопросы с несколькими вариантами ответа."""

    class Meta:
        model = AnswerForAskWithMultipleAnswers
        fields = (
            'id',
            'text',
            'ask',
        )
