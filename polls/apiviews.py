from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Question, Choice
from .serializers import QuestionListPageSerializer, QuestionDetailPageSerializer, QuestionChoiceSerializer, VoteSerializer, QuestionResultPageSerializer, ChoiceSerializer


class QuestionsView(APIView):

    def get(self, request, *args, **kwargs):
        questions = Question.objects.all()
        serializer = QuestionListPageSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = QuestionDetailPageSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            serializer = QuestionDetailPageSerializer(question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailView(APIView):

    def get(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['question_id'])
        serializer = QuestionDetailPageSerializer(question)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['question_id'])
        serializer = QuestionDetailPageSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionDetailPageSerializer(question).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['question_id'])
        question.delete()
        return Response("Question deleted", status=status.HTTP_204_NO_CONTENT)


class QuestionChoicesView(APIView):
    
    def get(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['question_id'])
        choices = question.choice_set.all()
        serializer = QuestionChoiceSerializer(choices, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['question_id'])
        serializer = QuestionChoiceSerializer(data=request.data)
        if serializer.is_valid():
            choice = serializer.save(question=question)
            return Response("Choice created with id %s" % (choice.id), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChoicesView(APIView):

    def get(self, request, *args, **kwargs):
        choices = Choice.objects.all()
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ChoiceSerializer(data=request.data)
        if serializer.is_valid():
            choice = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteView(APIView):

    def patch(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['question_id'])
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            choice = get_object_or_404(Choice, pk=serializer.validated_data['choice_id'], question=question)
            choice.votes += 1
            choice.save()
            return Response("Voted")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionResultView(APIView):

    def get(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['question_id'])
        serializer = QuestionResultPageSerializer(question)
        return Response(serializer.data)
