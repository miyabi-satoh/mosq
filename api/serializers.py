from rest_framework import serializers
from .models import Grade, PrintDetail, PrintHead, Unit, Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    # question_count = serializers.IntegerField(read_only=True)
    question_count = serializers.SerializerMethodField()
    grade = GradeSerializer()

    class Meta:
        model = Unit
        fields = '__all__'
        # fields = ['id', 'unit_code', 'unit_text',
        #           'grade', 'question_count']

    def get_question_count(self, obj):
        return Question.objects.filter(unit=obj.id).count()


class PrintDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintDetail
        fields = ['id', 'unit', 'quantity']


class PrintSerializer(serializers.ModelSerializer):
    details = PrintDetailSerializer(many=True)

    class Meta:
        model = PrintHead
        fields = '__all__'

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        printhead = PrintHead.objects.create(**validated_data)
        for detail_data in details_data:
            PrintDetail.objects.create(printhead=printhead, **detail_data)

        return printhead
