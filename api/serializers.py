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
    grade = GradeSerializer()

    class Meta:
        model = Unit
        fields = '__all__'

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
    unit = UnitSerializer()

    class Meta:
        model = PrintDetail
        fields = '__all__'


class PrintSerializer(serializers.ModelSerializer):
    details = PrintDetailSerializer(many=True)
    # archives = ArchiveSerializer(many=True, read_only=True)
    printtype = PrintTypeSerializer(read_only=True)
    printtype_id = serializers.PrimaryKeyRelatedField(
        queryset=PrintType.objects.filter(),
        source='printtype',
        write_only=True)

    class Meta:
        model = PrintHead
        fields = '__all__'

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        if not details_data:
            raise serializers.ValidationError('単元と問題数を入力してください。')

        printhead = PrintHead.objects.create(**validated_data)
        for detail_data in details_data:
            PrintDetail.objects.create(printhead=printhead, **detail_data)

        return printhead

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details')
        PrintDetail.objects.filter(printhead=instance).delete()
        for detail_data in details_data:
            PrintDetail.objects.create(printhead=instance, **detail_data)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance
