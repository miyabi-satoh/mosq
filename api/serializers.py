from django.db import transaction
from rest_framework import serializers
from .models import Archive, Grade, PrintDetail, PrintHead, PrintType, Unit, Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['grade'] = GradeSerializer(instance.grade).data
        return response

    def get_question_count(self, obj):
        return Question.objects.filter(unit=obj.id).count()


class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archive
        fields = '__all__'


class PrintTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintType
        fields = ['id', 'type_text']


class PrintDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintDetail
        exclude = ['printhead']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        i = 0
        for unit in instance.units.all():
            response['units'][i] = UnitSerializer(unit).data
            i += 1

        # response['unit'] = UnitSerializer(instance.unit).data
        return response


class PrintSerializer(serializers.ModelSerializer):
    details = PrintDetailSerializer(many=True)

    class Meta:
        model = PrintHead
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['printtype'] = PrintTypeSerializer(instance.printtype).data
        return response

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        if not details_data:
            raise serializers.ValidationError('単元と問題数を入力してください。')

        with transaction.atomic():
            printhead = PrintHead.objects.create(**validated_data)
            for detail_data in details_data:
                units = detail_data.pop('units')
                printdetail = PrintDetail.objects.create(
                    printhead=printhead, **detail_data)
                printdetail.units.set(units)

        return printhead

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details')
        if not details_data:
            raise serializers.ValidationError('単元と問題数を入力してください。')

        with transaction.atomic():
            PrintDetail.objects.filter(printhead=instance).delete()
            for detail_data in details_data:
                units = detail_data.pop('units')
                printdetail = PrintDetail.objects.create(
                    printhead=instance, **detail_data)
                printdetail.units.set(units)

            instance.title = validated_data.get('title', instance.title)
            instance.description = validated_data.get(
                'description', instance.description)
            instance.printtype = validated_data.get(
                'printtype', instance.printtype)
            instance.save()

        return instance
