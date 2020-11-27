u"""Сериализаторы для вопросов."""

from core.models import AskWithOneAnswer, AskWithMultipleAnswers, AskWithTextAnswer


from rest_framework.serializers import ModelSerializer


class AskWithOneAnswerListSerializer(ModelSerializer):

    class Meta:
        model = AskWithOneAnswer
        fields = (
            'id',
            'text',
        )


class AskWitOneAnswerDetailSerializer(ModelSerializer):

    class Meta:
        model = AskWithOneAnswer
        fields = (
            'id',
            'text',
        )


class AskWithMultipleAnswersListSerializer(ModelSerializer):

    class Meta:
        model = AskWithMultipleAnswers
        fields = (
            'id',
            'text',
        )


class AskWithMultipleAnswersDetailSerializer(ModelSerializer):

    class Meta:
        model = AskWithMultipleAnswers
        fields = (
            'id',
            'text',
        )


class AskWithTextAnswerListSerializer(ModelSerializer):

    class Meta:
        model = AskWithTextAnswer
        fields = (
            'id',
            'text',
        )


class AskWithTextAnswerDetailSerializer(ModelSerializer):

    class Meta:
        model = AskWithTextAnswer
        fields = (
            'id',
            'text',
        )
