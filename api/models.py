from django.db import models
from django.utils import timezone
from django.contrib import admin


class Grade(models.Model):
    grade_code = models.CharField('学年コード', max_length=2, unique=True)
    grade_text = models.CharField('学年', max_length=10, unique=True)

    def __str__(self) -> str:
        return f'{self.grade_text}'

    class Meta:
        ordering = ['grade_code']
        verbose_name = '学年'
        verbose_name_plural = '学年マスタ'


class Unit(models.Model):
    grade = models.ForeignKey(
        Grade, on_delete=models.CASCADE, verbose_name='学年')
    unit_code = models.CharField('単元コード', max_length=4)
    unit_text = models.CharField('単元', max_length=100)

    class Meta:
        ordering = ['unit_code']
        verbose_name = '単元'
        verbose_name_plural = '単元マスタ'
        constraints = [
            models.UniqueConstraint(
                fields=['grade', 'unit_code'],
                name='unit_unique'
            ),
        ]

    def __str__(self) -> str:
        return f'{self.grade} {self.unit_text}'


class Question(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name='単元')
    question_text = models.CharField('問題', max_length=100, unique=True)
    answer_text = models.CharField('解答', max_length=100)
    source_text = models.CharField('出典', max_length=100)
    url_text = models.CharField('URL', max_length=200, null=True)

    def __str__(self) -> str:
        return self.question_text

    class Meta:
        ordering = ['unit', 'id']
        verbose_name = '設問'
        verbose_name_plural = '設問マスタ'


class PrintHead(models.Model):
    title = models.CharField('タイトル', max_length=100)

    @admin.display(description='問題数')
    def total_questions(self):
        total = 0
        for detail in self.details.all():
            total += detail.quantity
        return total

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'プリントヘッダ'
        verbose_name_plural = 'プリントヘッダ'


class PrintDetail(models.Model):
    printhead = models.ForeignKey(
        PrintHead, related_name='details', on_delete=models.CASCADE, verbose_name='プリントヘッダ')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name='単元')
    quantity = models.PositiveSmallIntegerField(verbose_name='問題数')

    def __str__(self) -> str:
        return f'{self.printhead} {self.unit} {self.quantity}問'

    class Meta:
        ordering = ['printhead', 'unit']
        verbose_name = 'プリント明細'
        verbose_name_plural = 'プリント明細'
        constraints = [
            models.UniqueConstraint(
                fields=['printhead', 'unit'],
                name='printdetail_unique'
            ),
        ]


class Archive(models.Model):
    file = models.FileField('ファイル', upload_to='archive')
    title = models.CharField('タイトル', max_length=100)
    created_at = models.DateTimeField('作成日時', default=timezone.now)

    def __str__(self) -> str:
        return f"{self.title}@{self.created_at}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'プリントアーカイブ'
        verbose_name_plural = 'プリントアーカイブ'
