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
        fields = ['unit', 'quantity']


class PrintSerializer(serializers.ModelSerializer):
    print_detail = PrintDetailSerializer(many=True)

    class Meta:
        model = PrintHead
        fields = ['title', 'print_detail']

    def create(self, validated_data):
        result_dict = {}
        detail_list = []

        print_detail = validated_data.pop('print_detail')

        created_printhead = PrintHead.objects.create(**validated_data)
        result_dict['head_id'] = created_printhead.id

        for print_detail_data in print_detail:
            created_printdetail = PrintDetail.objects.create(
                printhead=created_printhead, **print_detail_data)
            detail_list.append(created_printdetail.id)

        result_dict['detail_id'] = detail_list
        return result_dict
