u"""Набор видов для работы с опросами."""

from rest_framework.viewsets import ModelViewSet
from core.models import Interrogation
from api.interrogations.serializers import InterrogationListSerializer
from api.interrogations.serializers import InterrogationDetailSerializer
from api.interrogations.serializers import InterrogationWriteSerializer
from api.asks.serializers import AskWithOneAnswerListSerializer
from api.asks.serializers import AskWithMultipleAnswersListSerializer
from api.asks.serializers import AskWithTextAnswerListSerializer

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.models import AskWithOneAnswer
from core.models import AskWithMultipleAnswers
from core.models import AskWithTextAnswer


# Небезопасные действия
_UNSAFE_ACTIONS = (
    'create',
    'update',
    'destroy',
)


class InterrogationViewSet(ModelViewSet):

    u"""
    Набор представлений для работы с опросами.

    Действие asks позволяет получить список всех вопросов, относящихся к опросу.
    """

    def get_permissions(self):
        u"""Разрешаем всё админу и только чтение всем остальным."""

        if self.action in _UNSAFE_ACTIONS:
            return IsAdminUser()
        return AllowAny()

    def get_serializer_class(self):
        u"""Сериализацию выполняем в зависимости от того, какого типа запрос пришёл."""

        if self.action == 'list':
            return InterrogationListSerializer
        if self.action == 'detail':
            return InterrogationDetailSerializer
        if self.action in _UNSAFE_ACTIONS:
            return InterrogationWriteSerializer

    def get_queryset(self):
        u"""
        Получение списка опросов.

        Админ видит всё.
        Анонимусы и зарегистрированные пользователи видят только активные в данный момент опросы.
        """
        user = self.request.user

        if user.is_authenticated and user.is_superuser:
            return Interrogation.objects.all()

        return Interrogation.active_right_now.all()

    @action(detail=True, methods=['GET'])
    def asks(self, request, pk=None):
        u"""
        Это представление возвращает список вопросов, относящихся к опросу,
        разделенных на три категории:

        **with_one_answer** - вопросы с одним правильным ответом
        **with_multiple_answers** - с несколькими правильными ответами
        **with_text_answer** - с ответом, вводимым человеком с клавиатуры
        """

        interrogation = self.get_object()

        asks_with_one_answer = AskWithOneAnswer.objects.filter(
            interrogation=interrogation)
        asks_with_multiple_answers = AskWithMultipleAnswers.objects.filter(
            interrogation=interrogation)
        asks_with_text_asnwer = AskWithTextAnswer.objects.filter(
            interrogation=interrogation)

        serializer_one = AskWithOneAnswerListSerializer(
            asks_with_one_answer, many=True)
        serializer_multi = AskWithMultipleAnswersListSerializer(
            asks_with_multiple_answers, many=True)
        serializer_text = AskWithTextAnswerListSerializer(
            asks_with_text_asnwer, many=True)

        return Response(dict(
            with_one_answer=serializer_one.data,
            with_multiple_answers=serializer_multi.data,
            with_text_answer=serializer_text.data
        ))
