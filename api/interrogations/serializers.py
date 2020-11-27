u"""Сериализаторы для работы с опросами."""

from rest_framework.serializers import ModelSerializer
from core.models import Interrogation


class InterrogationListSerializer(ModelSerializer):

    u"""
    Сериализатор для представления опросов в списках.
    """

    class Meta:
        model = Interrogation
        fields = (
            'id',
            'name',
            'date_begin',
            'date_end',
        )


class InterrogationDetailSerializer(ModelSerializer):

    u"""
    Сериализатор для подробной информации об опросе.
    """

    class Meta:
        model = Interrogation
        fields = (
            'id',
            'name',
            'date_begin',
            'date_end',
            'active',
        )


class InterrogationWriteSerializer(ModelSerializer):

    u"""
    Сериализатор для записи сведений об опросе.
    """

    class Meta:
        model = Interrogation
        fields = (
            'id',
            'name',
            'date_begin',
            'date_end',
            'active',
        )
