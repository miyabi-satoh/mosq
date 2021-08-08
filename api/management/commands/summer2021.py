import os
import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from mako.template import Template
from ...models import Grade, Question, Unit


class Command(BaseCommand):
    @transaction.atomic
    def delete_questions(self):
        Question.objects.all().delete()

    def create_question(self, que, ans):
        return Question.objects.create(
            unit=self.unit,
            question_text=f"${que}$",
            answer_text=f"${que}{ans}$",
            source_text="自動生成"
        )

    @transaction.atomic
    def level1(self):
        """
        Level1  1桁同士の計算
        """
        for a in range(1, 10):
            for b in range(1, 10):
                # 足し算
                (self.unit, created) = Unit.objects.get_or_create(
                    unit_code="9911",
                    defaults={
                        "grade": self.grade,
                        "unit_text": "Level1(たす)",
                    }
                )
                self.create_question(f"{a}+{b}=", a + b)

                # 引き算
                if a != b:
                    (self.unit, created) = Unit.objects.get_or_create(
                        unit_code="9912",
                        defaults={
                            "grade": self.grade,
                            "unit_text": "Level1(ひく)",
                        }
                    )
                    self.create_question(f"{a}-{b}=", a - b)

                # 掛け算
                if a != 1 and b != 1:
                    (self.unit, created) = Unit.objects.get_or_create(
                        unit_code="9913",
                        defaults={
                            "grade": self.grade,
                            "unit_text": "Level1(かけ)",
                        }
                    )
                    self.create_question(f"{a}\\times {b}=", a * b)

                # 割り算
                if a != 1 and b != 1 and a >= b and a % b == 0:
                    (self.unit, created) = Unit.objects.get_or_create(
                        unit_code="9914",
                        defaults={
                            "grade": self.grade,
                            "unit_text": "Level1(わり)",
                        }
                    )
                    self.create_question(f"{a}\\div {b}=", int(a / b))

    @transaction.atomic
    def level2(self):
        """
        Level2  2桁と1桁同士の計算
        """
        for a in range(10, 100):
            for b in range(1, 10):
                # 足し算
                (self.unit, created) = Unit.objects.get_or_create(
                    unit_code="9921",
                    defaults={
                        "grade": self.grade,
                        "unit_text": "Level2(たす)",
                    }
                )
                self.create_question(f"{a}+{b}=", a + b)

                # 引き算
                (self.unit, created) = Unit.objects.get_or_create(
                    unit_code="9922",
                    defaults={
                        "grade": self.grade,
                        "unit_text": "Level2(ひく)",
                    }
                )
                self.create_question(f"{a}-{b}=", a - b)

                # 掛け算
                if b != 1:
                    (self.unit, created) = Unit.objects.get_or_create(
                        unit_code="9923",
                        defaults={
                            "grade": self.grade,
                            "unit_text": "Level2(かけ)",
                        }
                    )
                    self.create_question(f"{a}\\times {b}=", a * b)

                # 割り算
                if b != 1 and a > b and a % b == 0:
                    (self.unit, created) = Unit.objects.get_or_create(
                        unit_code="9924",
                        defaults={
                            "grade": self.grade,
                            "unit_text": "Level2(わり)",
                        }
                    )
                    self.create_question(f"{a}\\div {b}=", int(a / b))

    @transaction.atomic
    def level3(self):
        """
        Level3  2桁と2桁同士の計算
        """
        for a in range(10, 100):
            for b in range(10, 100):
                # 足し算
                (self.unit, created) = Unit.objects.get_or_create(
                    unit_code="9931",
                    defaults={
                        "grade": self.grade,
                        "unit_text": "Level3(たす)",
                    }
                )
                self.create_question(f"{a}+{b}=", a + b)

                # 引き算
                (self.unit, created) = Unit.objects.get_or_create(
                    unit_code="9932",
                    defaults={
                        "grade": self.grade,
                        "unit_text": "Level3(ひく)",
                    }
                )
                self.create_question(f"{a}-{b}=", a - b)

                # 掛け算
                (self.unit, created) = Unit.objects.get_or_create(
                    unit_code="9933",
                    defaults={
                        "grade": self.grade,
                        "unit_text": "Level3(かけ)",
                    }
                )
                self.create_question(f"{a}\\times {b}=", a * b)

                # 割り算
                if a > b and a % b == 0:
                    (self.unit, created) = Unit.objects.get_or_create(
                        unit_code="9934",
                        defaults={
                            "grade": self.grade,
                            "unit_text": "Level3(わり)",
                        }
                    )
                    self.create_question(f"{a}\\div {b}=", int(a / b))

    def handle(self, *args, **options):
        self.grade = Grade.objects.get(grade_code="09")
        self.delete_questions()
        self.level1()
        self.level2()
        self.level3()

        selected = []
        level1 = []
        unit = Unit.objects.get(unit_code="9911")
        query_sets = (
            Question.objects.filter(
                unit=unit
            ).order_by('?')[:13]
        )
        for q in query_sets:
            level1.append(q)
            selected.append(q.id)
        unit = Unit.objects.get(unit_code="9912")
        query_sets = (
            Question.objects.filter(
                unit=unit
            ).order_by('?')[:13]
        )
        for q in query_sets:
            level1.append(q)
            selected.append(q.id)
        unit = Unit.objects.get(unit_code="9913")
        query_sets = (
            Question.objects.filter(
                unit=unit
            ).order_by('?')[:12]
        )
        for q in query_sets:
            level1.append(q)
            selected.append(q.id)
        unit = Unit.objects.get(unit_code="9914")
        query_sets = (
            Question.objects.filter(
                unit=unit
            ).order_by('?')[:12]
        )
        for q in query_sets:
            level1.append(q)
            selected.append(q.id)

        level2 = []
        unit = Unit.objects.get(unit_code="9921")
        query_sets = (
            Question.objects.filter(
                unit=unit
            ).order_by('?')[:8]
        )
        for q in query_sets:
            level2.append(q)
            selected.append(q.id)
        unit = Unit.objects.get(unit_code="9922")
        query_sets = (
            Question.objects.filter(
                unit=unit
            ).order_by('?')[:8]
        )
        for q in query_sets:
            level2.append(q)
            selected.append(q.id)
        unit = Unit.objects.get(unit_code="9923")
        query_sets = (
            Question.objects.filter(
                unit=unit
            ).order_by('?')[:7]
        )
        for q in query_sets:
            level2.append(q)
            selected.append(q.id)
        unit = Unit.objects.get(unit_code="9924")
        query_sets = (
            Question.objects.filter(
                unit=unit
            ).order_by('?')[:7]
        )
        for q in query_sets:
            level2.append(q)
            selected.append(q.id)

        level3 = []
        unit = Unit.objects.get(unit_code="9931")
        query_sets = (
            Question.objects.filter(
                unit=unit
            ).order_by('?')[:8]
        )
        for q in query_sets:
            level3.append(q)
            selected.append(q.id)
        unit = Unit.objects.get(unit_code="9932")
        query_sets = (
            Question.objects.filter(
                unit=unit
            ).order_by('?')[:8]
        )
        for q in query_sets:
            level3.append(q)
            selected.append(q.id)
        unit = Unit.objects.get(unit_code="9933")
        query_sets = (
            Question.objects.filter(
                unit=unit
            ).order_by('?')[:7]
        )
        for q in query_sets:
            level3.append(q)
            selected.append(q.id)
        unit = Unit.objects.get(unit_code="9934")
        query_sets = (
            Question.objects.filter(
                unit=unit
            ).order_by('?')[:7]
        )
        for q in query_sets:
            level3.append(q)
            selected.append(q.id)

        level4 = []
        for i in range(0, 12):
            questions = []
            units = Unit.objects.filter(unit_code__in=["9911", "9921", "9931"])
            query_sets = (
                Question.objects.filter(
                    unit__in=units
                ).exclude(
                    pk__in=selected
                ).order_by('?')[:8]
            )
            for q in query_sets:
                questions.append(q)
                selected.append(q.id)
            units = Unit.objects.filter(unit_code__in=["9912", "9922", "9932"])
            query_sets = (
                Question.objects.filter(
                    unit__in=units
                ).exclude(
                    pk__in=selected
                ).order_by('?')[:8]
            )
            for q in query_sets:
                questions.append(q)
                selected.append(q.id)
            units = Unit.objects.filter(unit_code__in=["9913", "9923", "9933"])
            query_sets = (
                Question.objects.filter(
                    unit__in=units
                ).exclude(
                    pk__in=selected
                ).order_by('?')[:7]
            )
            for q in query_sets:
                questions.append(q)
                selected.append(q.id)
            units = Unit.objects.filter(unit_code__in=["9914", "9924", "9934"])
            query_sets = (
                Question.objects.filter(
                    unit__in=units
                ).exclude(
                    pk__in=selected
                ).order_by('?')[:7]
            )
            for q in query_sets:
                questions.append(q)
                selected.append(q.id)
            level4.append(questions[:])

        path = os.path.dirname(__file__)
        path = os.path.join(path, '../../resources/summer2021.tex')
        path = os.path.normpath(path)
        with open(path, encoding='utf-8') as f:
            template = f.read()

        template = template.replace("\\_", '_')
        template = template.replace("@[", "${")
        template = template.replace("]@", "}")

        dt_now = datetime.datetime.now()
        filename = dt_now.strftime('%Y%m%d_%H%M%S%f')
        with open(f'{filename}.tex', 'w', encoding='utf-8') as f:
            mt = Template(template)
            f.write(
                mt.render(
                    level1=level1,
                    level2=level2,
                    level3=level3,
                    level4=level4
                )
            )
