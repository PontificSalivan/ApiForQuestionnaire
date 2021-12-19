from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.status import \
    HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from .models import Question, Questionnaire, Choice, Answer
from .serializers import QuestionnaireSerializer, QuestionSerializer, ChoiceSerializer, AnswerSerializer


class LoginApiView(APIView):

    def post(self, request):
        data = request.data
        username = data.get("username", None)
        password = data.get("password", None)

        if username is None or password is None:
            return Response({'error': 'Укажите имя пользователя и пароль'},
                            status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Неверные учетные данные, попробуйте снова'}, status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=HTTP_200_OK)


class QuestionnaireCreate(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = QuestionnaireSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            questionnaire = serializer.save()
            return Response(QuestionnaireSerializer(questionnaire).data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class QuestionnaireUpdate(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, questionnaire_id):
        questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_id)
        serializer = QuestionnaireSerializer(questionnaire, data=request.data, partial=True)
        if serializer.is_valid():
            questionnaire = serializer.save()
            return Response(QuestionnaireSerializer(questionnaire).data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, questionnaire_id):
        questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_id)
        questionnaire.delete()
        return Response(f"Опрос {questionnaire.questionnaire_name} удален", status=HTTP_204_NO_CONTENT)


class QuestionnaireView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questionnaire = Questionnaire.objects.all()
        serializer = QuestionnaireSerializer(questionnaire, many=True)
        return Response(serializer.data)


class QuestionnaireViewActive(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questionnaire = Questionnaire.objects.filter(end_date__gte=timezone.now()).\
            filter(pub_date__lte=timezone.now())
        serializer = QuestionnaireSerializer(questionnaire, many=True)
        return Response(serializer.data)


class QuestionCreate(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionSerializer(question).data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class QuestionUpdate(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionSerializer(question).data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        question.delete()
        return Response(f"Вопрос {question.question_text} удален", status=HTTP_204_NO_CONTENT)


class ChoiceCreate(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = ChoiceSerializer(data=request.data)
        if serializer.is_valid():
            choice = serializer.save()
            return Response(ChoiceSerializer(choice).data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    
class ChoiceUpdate(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, choice_id):
        choice = get_object_or_404(Choice, pk=choice_id)
        serializer = ChoiceSerializer(choice, data=request.data, partial=True)
        if serializer.is_valid():
            choice = serializer.save()
            return Response(ChoiceSerializer(choice).data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, choice_id):
        choice = get_object_or_404(Choice, pk=choice_id)
        choice.delete()
        return Response(f"Выбор {choice.choice_text} удален", status=HTTP_204_NO_CONTENT)


class AnswerCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AnswerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            answer = serializer.save()
            return Response(AnswerSerializer(answer).data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class AnswerUpdate(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, answer_id):
        answer = get_object_or_404(Answer, pk=answer_id)
        serializer = AnswerSerializer(answer, data=request.data, partial=True)
        if serializer.is_valid():
            answer = serializer.save()
            return Response(AnswerSerializer(answer).data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, answer_id):
        answer = get_object_or_404(Answer, pk=answer_id)
        answer.delete()
        return Response(f"Ответ номер {answer_id} удален", status=HTTP_204_NO_CONTENT)


class AnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        answers = Answer.objects.filter(user_id=user_id)
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)
