from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('login/', views.LoginApiView.as_view(), name='login'),
    # опросник
    path('questionnaire/create/', views.QuestionnaireCreate.as_view(), name='questionnaire_create'),
    path('questionnaire/update/<int:questionnaire_id>/', views.QuestionnaireUpdate.as_view(),
         name='questionnaire_update'),
    path('questionnaire/view/', views.QuestionnaireView.as_view(), name='questionnaire_view'),
    path('questionnaire/view/active/', views.QuestionnaireViewActive.as_view(), name='active_questionnaire_view'),
    # вопросы
    path('question/create/', views.QuestionCreate.as_view(), name='question_create'),
    path('question/update/<int:question_id>/', views.QuestionUpdate.as_view(), name='question_update'),
    # выборы вопросов
    path('choice/create/', views.ChoiceCreate.as_view(), name='choice_create'),
    path('choice/update/<int:choice_id>/', views.ChoiceUpdate.as_view(), name='choice_update'),
    # ответы вопросов
    path('answer/create/', views.AnswerCreate.as_view(), name='answer_create'),
    path('answer/view/<int:user_id>/', views.AnswerView.as_view(), name='answer_view'),
    path('answer/update/<int:answer_id>/', views.AnswerUpdate.as_view(), name='answer_update')
]

