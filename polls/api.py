from .models import Question, Choice

from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import Authorization


class QuestionResource(ModelResource):

    question_text_duplicate = fields.CharField(attribute='question_text')

    class Meta:
        # queryset = Question.objects.all()
        object_class = Question
        resource_name = 'questions'
        authorization = Authorization()
        # excludes = ('id',)

    def dehydrate_question_text(self, bundle):
        return bundle.data['question_text'].upper()

    def build_filters(self, filters=None):
        filters = super(QuestionResource, self).build_filters(filters)
        filters['id__gt'] = 72
        return filters

    def get_object_list(self, request):
        return Question.objects.filter(id__gt=71)

    def dehydrate(self, bundle):
        bundle.data['len_question_text'] = len(bundle.data['question_text'])
        return bundle


class ChoiceResource(ModelResource):

    question = fields.ForeignKey(QuestionResource, 'question', full=True)

    class Meta:
        queryset = Choice.objects.all()
        resource_name = 'choices'

class PersonResource(ModelResource):

    name = fields.CharField()
