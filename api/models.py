from django.db import models
from django.utils import timezone
from django.contrib import admin


class Grade(models.Model):
    """
    学年マスタ

    Attributes
    ----------
    grade_code : str
        学年コード2桁。
    grade_text : str
        学年の名称。
    """
    grade_code = models.CharField('学年コード', max_length=2, unique=True)
    grade_text = models.CharField('学年', max_length=10, unique=True)

    def __str__(self) -> str:
        return f'{self.grade_text}'

    class Meta:
        ordering = ['grade_code']
        verbose_name = '学年'
        verbose_name_plural = '学年マスタ'


class Unit(models.Model):
    """
    単元マスタ

    Attributes
    ----------
    grade : int
        Gradeへの外部キー。
    unit_code : str
        単元コード4桁。
    unit_text : str
        単元の名称。
    """
    grade = models.ForeignKey(
        Grade,
        on_delete=models.PROTECT,
        verbose_name='学年'
    )
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
    """
    設問マスタ

    Attributes
    ----------
    unit : int
        Unitへの外部キー
    question_text : str
        問題のテキスト。
    answer_text : str
        答えのテキスト。
    source_text : str
        出典元。
    url_text : str
        参照先URL(任意)。
    """
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, verbose_name='単元')
    question_text = models.CharField('問題', max_length=100, unique=True)
    answer_text = models.CharField('解答', max_length=100)
    source_text = models.CharField('出典', max_length=100)
    url_text = models.CharField('URL', max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return self.question_text

    class Meta:
        ordering = ['unit', 'id']
        verbose_name = '設問'
        verbose_name_plural = '設問マスタ'


class PrintType(models.Model):
    """
    プリント形式

    Attibutes
    ---------
    type_text : str
        形式の名称。
    template : str
        テンプレートファイル
    cover : str
        表紙。
    """
    type_text = models.CharField('形式', max_length=100)
    template = models.FileField('テンプレート', upload_to='template')
    cover = models.FileField('表紙', upload_to='cover', null=True, blank=True)

    def __str__(self) -> str:
        return self.type_text

    class Meta:
        verbose_name = 'プリント形式'
        verbose_name_plural = 'プリント形式'


class PrintHead(models.Model):
    """
    プリントヘッダ

    Attributes
    ----------
    title : str
        ヘッダータイトル。
    description : str
        プリントの説明(任意)。
    password : str
        保護パスワード(任意)。最大32桁。
    """
    title = models.CharField('タイトル', max_length=100,)
    description = models.CharField('説明', null=True, blank=True, max_length=100)
    password = models.CharField('パスワード', null=True, blank=True, max_length=32)
    printtype = models.ForeignKey(
        PrintType,
        on_delete=models.PROTECT,
        verbose_name='形式'
    )

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
    """
    プリント明細

    Attributes
    ----------
    printhead : int
        PrintHeadへの外部キー。
    unit : int
        Unitへの外部キー。
    quantity : int
        問題数。
    """
    printhead = models.ForeignKey(
        PrintHead,
        related_name='details',
        on_delete=models.CASCADE,
        verbose_name='プリントヘッダ'
    )
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
    """
    アーカイブ(作成済みプリントのストック)

    Attributes
    ----------
    printhead : int
        PrintHeadへの外部キー。
    file : str
        ファイルパス。
    title : str
        タイトル。
    created_at : datetime
        作成日時。
    """
    printhead = models.ForeignKey(
        PrintHead,
        related_name='archives',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='プリントヘッダ'
    )
    file = models.FileField('ファイル', upload_to='archive')
    title = models.CharField('タイトル', max_length=100)
    created_at = models.DateTimeField('作成日時', default=timezone.now)

    def __str__(self) -> str:
        return f"{self.title}@{self.created_at}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'プリントアーカイブ'
        verbose_name_plural = 'プリントアーカイブ'
