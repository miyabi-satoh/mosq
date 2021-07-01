import os
import sys
import re
from typing import List
from django.core.management.base import BaseCommand
from django.db import connection
from ...models import Grade, Unit


class Command(BaseCommand):
    help = 'Import questions from TeX file'

    def handle(self, *args, **options):
        path = os.path.dirname(__file__)
        path = os.path.join(path, '../../resources/計算問題.tex')
        path = os.path.normpath(path)
        self.stdout.write(path)

        with open(path, encoding='utf-8') as f:
            tables = [
                'api_printdetail',
                'api_printhead',
                'api_question',
                'api_unit',
                'api_grade',
            ]
            cursor = connection.cursor()
            for table in tables:
                cursor.execute(f"DELETE FROM {table}")
                cursor.execute(
                    f"DELETE FROM sqlite_sequence WHERE name = '{table}'")

            grade_list = [
                '小1',
                '小2',
                '小3',
                '小4',
                '小5',
                '小6',
                '中1',
                '中2',
                '中3',
                '高1',
                '高2',
                '高3',
            ]
            for index, text in enumerate(grade_list):
                g = Grade(grade_code=f'00{index + 1}'[-2:], grade_text=text)
                g.save()

            isQuestion = True
            question_list: List[str] = []
            answer_list: List[str] = []
            url_text: str = ''

            for line in f:
                # 改行削除
                line = line.rstrip()
                if (match := re.search(r'%define ([^ ]+) (\d{4}) (.+)$', line)):
                    grade_text = match.group(1).strip()
                    unit_code = match.group(2).strip()
                    unit_text = match.group(3).strip()

                    g = Grade.objects.get(grade_text=grade_text)
                    if not g:
                        sys.exit(f'grade not found : {grade_text}')
                    g.unit_set.create(unit_code=unit_code, unit_text=unit_text)
                elif (match := re.search(r'%%URL (.+)$', line)):
                    url_text = match.group(1).strip()
                elif re.search(r'\\item ', line):
                    if isQuestion:
                        question_list.append(f'{line}, {url_text}')
                    else:
                        answer_list.append(line)
                    isQuestion = not isQuestion

            if len(question_list) != len(answer_list):
                sys.exit('問題と答えの数が違います。')

            for index, text in enumerate(question_list):
                match = re.search(r'^(.*?)%%(.*?),(.*?),(.*?)$', text.strip())
                if not match:
                    self.stdout.write(text)
                    sys.exit('予期しないフォーマットです。')
                question_text = match.group(1).replace("\\item", '').strip()
                source_text = match.group(2).strip()
                unit_code = match.group(3).strip()
                url_text = match.group(4).strip()
                answer_text = answer_list[index].replace("\\item", '').strip()

                u = Unit.objects.get(unit_code=unit_code)
                if not u:
                    sys.exit(f'単元コードが未定義です : {unit_code}')

                u.question_set.create(
                    question_text=question_text,
                    answer_text=answer_text,
                    source_text=source_text,
                    url_text=url_text
                )

            self.stdout.write('success.')
