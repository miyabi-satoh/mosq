import os
import sys
import re
from fractions import Fraction
from typing import List
from django.core.management.base import BaseCommand
from django.db import connection, IntegrityError
from ...models import Grade, Unit


def isFrac(x: Fraction) -> bool:
    return x.denominator != 1


def emath_bunsuu(x: Fraction) -> str:
    b = x.denominator
    a = x.numerator
    sign = ''
    if a < 0:
        a *= -1
        sign = '-'
    if b < 0:
        b *= -1
        sign = '-'
    if b == 1:
        return f'{sign}{a}'

    return sign + "\\bunsuu{" + f'{a}' + "}{" + f'{b}' + "}"


def charaexp_addsub_question() -> str:
    """
    文字式の加法・減法を作る
    """
    u = Unit.objects.get(unit_code='0201')

    count = 0
    listNum: list[Fraction] = []
    for a in range(-5, 6):
        if a == 0:
            continue
        for b in range(1, 4):
            if b == 0:
                continue
            x = Fraction(a, b)
            if isFrac(x) and abs(x.numerator) > x.denominator:
                # 仮分数は除外
                continue
            if x.denominator == b:
                listNum.append(x)

    # a(b + c)を表現するクラス
    class CharaExpr:
        def __init__(self, a, b, c) -> None:
            self.a = Fraction(a)
            self.b = Fraction(b)
            self.c = Fraction(c)

        def expandable(self) -> bool:
            """
            カッコの前の分数を展開して、分子式にできるか判定
            """
            if isFrac(self.a) and abs(self.a.numerator) == 1:  # a = 1/m
                if (not isFrac(self.b)) and (not isFrac(self.c)):  # b,c = 整数
                    ab = self.a * self.b
                    ac = self.a * self.c
                    if self.a.denominator == ab.denominator and self.a.denominator == ac.denominator:
                        return True
            return False

        def __eq__(self, o: object) -> bool:
            return self.a == o.a and self.b == o.b and self.c == o.c

        def __str__(self) -> str:
            inner = ''
            if self.b == -1:
                inner += '-'
            elif self.b != 1:
                inner += emath_bunsuu(self.b)
            inner += 'a'

            if self.c > 0:
                inner += '+'
                if self.c != 1:
                    inner += emath_bunsuu(self.c)
            elif self.c == -1:
                inner += '-'
            else:
                inner += emath_bunsuu(self.c)
            inner += "b"

            if self.expandable():
                sign = '-' if self.a < 0 else ''
                return sign + "\\bunsuu{" + inner + "}{" + f'{self.a.denominator}' + "}"

            if self.a == -1:
                return "-\\left(" + inner + "\\right)"

            if self.a != 1:
                return emath_bunsuu(self.a) + "\\left(" + inner + "\\right)"

            return inner

    listCharaExpr: list[CharaExpr] = []
    for a in listNum:
        for b in listNum:
            for c in listNum:
                # 同数は除外する
                if abs(a) == abs(b) or b == c:
                    continue
                # a が分数なら、b,cは整数
                if isFrac(a):
                    if isFrac(b) or isFrac(c):
                        continue
                    if a.denominator == abs(b) and a.denominator == abs(c):
                        continue
                # b,c分数なら異分母であること
                if isFrac(b) and isFrac(c) and b.denominator == c.denominator:
                    continue
                # 片っ端が分数なら、係数は1であること
                if isFrac(b) != isFrac(c) and a != 1:
                    continue
                # カッコ内で偶数のみは除外
                if (not isFrac(b)) and (not isFrac(c)):
                    if b % 2 == 0 and c % 2 == 0:
                        continue
                listCharaExpr.append(CharaExpr(a, b, c))

    for expr_a in listCharaExpr:
        # カッコの前後は正の数
        if expr_a.a < 0 or expr_a.b < 0:
            continue
        # カッコ内で整数と分数は混在させない
        if isFrac(expr_a.b) != isFrac(expr_a.c):
            continue
        for expr_b in listCharaExpr:
            # 公立入試問題の係数比較した感じで除外
            if abs(expr_a.a) == abs(expr_b.a):  # A=D/ABS
                continue
            if expr_a.a == expr_b.c:            # A=F
                continue
            if expr_a.b == expr_b.a:            # B=D
                continue
            if abs(expr_a.b) == abs(expr_b.c):  # B=F/ABS
                continue
            if expr_a.c == expr_b.c:            # C=F
                continue
            if expr_b.a != 1 and expr_b.b < 0:  # a(-b...)
                continue
            # F は整数
            if isFrac(expr_b.c):
                continue
            # A/D が分数なら異分母
            if isFrac(expr_a.a) and isFrac(expr_b.a):
                if expr_a.a.denominator == expr_b.a.denominator:
                    continue

            # if not expr_a.expandable() and not expr_b.expandable():
            #     if isFrac(expr_a.a):
            #         if abs(expr_b.a) > 1:
            #             continue
            #         if abs(expr_a.a) == abs(expr_b.b):
            #             continue
            #         if abs(expr_a.a) == abs(expr_b.c):
            #             continue
            #         if isFrac(expr_b.b) or isFrac(expr_b.c):
            #             continue
            #     if isFrac(expr_b.a):
            #         if abs(expr_a.a) > 1:
            #             continue
            #         if abs(expr_b.a) == abs(expr_a.b):
            #             continue
            #         if abs(expr_b.a) == abs(expr_a.c):
            #             continue

            # 分数の数で仕分け
            fracCount = 0
            if isFrac(expr_a.a):
                fracCount += 1
            if isFrac(expr_a.b):
                fracCount += 1
            if isFrac(expr_a.c):
                fracCount += 1
            if isFrac(expr_b.a):
                fracCount += 1
            if isFrac(expr_b.b):
                fracCount += 1
            if isFrac(expr_b.c):
                fracCount += 1

            if fracCount > 3:
                continue
            if fracCount == 3:
                if isFrac(expr_a.a) or isFrac(expr_b.a):
                    continue
                if abs(expr_a.a) != 1 and abs(expr_b.a) != 1:
                    continue

            if expr_a.expandable():
                if isFrac(expr_b.a) and not expr_b.expandable():
                    continue
            #     elif not expr_b.expandable():
            #         continue

            if expr_b.expandable():
                if isFrac(expr_a.a) and not expr_a.expandable():
                    continue
            #     elif not expr_a.expandable():
            #         continue

            aX = expr_a.a * expr_a.b
            bX = expr_b.a * expr_b.b
            ansX = aX + bX
            if ansX.denominator > 9:
                continue
            if abs(ansX.numerator) > 9:
                continue

            aY = expr_a.a * expr_a.c
            bY = expr_b.a * expr_b.c
            ansY = aY + bY
            if ansY.denominator > 9:
                continue
            if abs(ansY.numerator) > 9:
                continue

            if ansX == 0 and ansY == 0:
                continue

            if ansX == 0:
                ansX = ""
            elif ansX == 1:
                ansX = "a"
            elif ansX == -1:
                ansX = "-a"
            else:
                ansX = emath_bunsuu(ansX) + 'a'

            if ansY == 0:
                ansY = ""
            elif ansY == 1:
                ansY = "+b"
            elif ansY == -1:
                ansY = "-b"
            else:
                sign = '+' if ansX != 0 and ansY > 0 else ''
                ansY = sign + emath_bunsuu(ansY) + 'b'

            strA = str(expr_a)
            strB = str(expr_b)
            if expr_b.a > 0:
                if expr_b.a == 1 and expr_b.b < 0:
                    pass
                else:
                    strB = '+' + strB

            u.question_set.create(
                question_text=f'${strA}{strB}$ を計算しなさい。',
                answer_text=f'${ansX}{ansY}$',
                source_text="自動生成"
            )
            count += 1
            # if count > 1000:
            #     return count

    return f'{count}問を自動生成しました。'


def ternary_number_question() -> str:
    """
    正負の三項計算を作る
    """
    u = Unit.objects.get(unit_code='0105')  # 乗除混合

    # A : 正の整数・負の整数(-1, 0, 1は含まない)
    # B : 正の整数・負の整数(-1, 0, 1は含まない)
    listA: list[int] = []
    listB: list[int] = []
    for x in range(-18, 19):
        if abs(x) > 1:
            listA.append(x)
            listB.append(x)
    # C : 1桁, 分数アリ(-1, 0, 1は含まない)
    listC: list[Fraction] = []
    for x in range(-9, 10):
        if x == 0:
            continue
        for y in range(1, 10):
            c = Fraction(x, y)
            if c.denominator != y or abs(c) == 1:
                continue
            listC.append(c)

    count = 0
    zero_count = 0
    for a in listA:
        for b in listB:
            if a < 0 and b < 0:
                continue
            if abs(a) == abs(b):
                continue
            for c in listC:
                if b < 0 and c < 0:
                    continue
                if a == 0 and b * c > 0:
                    continue
                if a < 0 and b < 0 and c < 0:
                    continue
                if abs(a) == abs(c) or abs(b) == abs(c):
                    continue

                for ex in range(1, 4):
                    valA = a
                    valB = b
                    valC = c
                    expA = ''
                    expB = ''
                    expC = ''
                    negA = ''

                    if ex == 1:
                        if a == 0 or abs(a) > 4:
                            # 0と5以上の2乗は除外
                            continue
                        valA = a * a
                        expA = '^2'
                        if a > 0 and b > 0:
                            negA = '-'
                            valA *= -1
                    elif a < 0:       # 素の負数は除外
                        continue
                    if ex == 2:
                        if abs(b) > 4:
                            continue
                        valB = b * b
                        expB = '^2'
                    if ex == 3:
                        if c > 0 or abs(c.numerator) > 4 or c.denominator > 4:
                            continue
                        valC = c * c
                        expC = '^2'

                    for mul_div in ['*', '/']:
                        if mul_div == '*':
                            bc = b * c
                            if isFrac(c):
                                # 一発約分できるものは除外
                                if abs(b) == c.denominator:
                                    continue
                                # 約分できないものも除外
                                if bc.denominator == c.denominator:
                                    continue
                            opBC = " \\times "
                            valBC = valB * valC
                        else:
                            bc = b / c
                            if isFrac(c):
                                # 約分できないものは除外
                                if bc.denominator == abs(c.numerator):
                                    continue
                            opBC = " \\div "
                            valBC = valB / valC
                        if abs(valBC) > 15:
                            continue

                        for add_sub in ['+', '-']:
                            if add_sub == '+':
                                abc = valA + valBC
                            else:
                                if a == 0:
                                    continue
                                abc = valA - valBC

                            if abs(abc.numerator) > 15 or abc.denominator > 15:
                                continue

                            expr = negA
                            if a != 0:
                                expr += f'{a}' if a > 0 else f'({a})'
                                expr += expA
                                expr += add_sub
                            else:
                                zero_count += 1

                            expr += f'{b}' if b > 0 else f'({b})'
                            expr += expB
                            expr += opBC
                            if c < 0 or (ex == 3 and isFrac(c)):
                                expr += f"\\left({emath_bunsuu(c)}\\right)"
                            else:
                                expr += emath_bunsuu(c)
                            expr += expC

                            u.question_set.create(
                                question_text=f'${expr}$ を計算しなさい。',
                                answer_text=f'${emath_bunsuu(abc)}$',
                                source_text="自動生成"
                            )
                            count += 1
                            # if count > 1000:
                            #     return count
    return f'{count}問を自動生成しました。'


def exponents_question() -> str:
    """
    指数の問題を作る
    """
    u = Unit.objects.get(unit_code='0103')

    c256 = 16 * 16
    count = 0
    for x in range(1, 11):
        for y in range(2, 17):
            xy = Fraction(y, x)
            if xy.denominator != x:
                continue
            for e in range(2, 4):
                # x^e
                ans = xy ** e
                if ans.numerator > c256 or ans.denominator > c256:
                    continue
                expr = emath_bunsuu(xy)
                if xy.denominator != 1:
                    expr = f'({expr})'
                expr += f'^{e}'
                u.question_set.create(
                    question_text=f'${expr}$ を計算しなさい。',
                    answer_text=f'${emath_bunsuu(ans)}$',
                    source_text="自動生成"
                )
                count += 1

                # (-x)^e
                expr = f'(-{emath_bunsuu(xy)})^{e}'
                u.question_set.create(
                    question_text=f'${expr}$ を計算しなさい。',
                    answer_text=f'${"-" if e == 3 else ""}{emath_bunsuu(ans)}$',
                    source_text="自動生成"
                )
                count += 1

                # -x^e
                if xy.denominator != 1:
                    continue
                expr = f'-{xy}^{e}'
                u.question_set.create(
                    question_text=f'${expr}$ を計算しなさい。',
                    answer_text=f'$-{ans}$',
                    source_text="自動生成"
                )
                count += 1
    return f'{count}問を自動生成しました。'


def binary_number_question() -> str:
    """
    正負の二項計算を作る
    """
    u0101 = Unit.objects.get(unit_code='0101')  # 加減
    u0102 = Unit.objects.get(unit_code='0102')  # 乗除

    # A : 正の数・負の数(-1, 0, 1は含まない)
    # B : 負の数(-1は含まない)
    listA: list[int] = []
    listB: list[int] = []
    for x in range(-18, 19):
        if x == 0 or x == -1 or x == 1:
            continue
        listA.append(x)
        if x < 0:
            listB.append(x)

    count = 0
    for a in listA:
        for b in listB:
            if abs(a) == abs(b):
                continue
            if len(f'{abs(a)}{abs(b)}') > 3:    # 2桁同士の演算はスキップ
                continue
            for op in ['+', '-', '*', '/', '']:
                if op == '+' or op == '':   # 加法
                    c = Fraction(a + b)
                    u = u0101
                elif op == '-':             # 減法
                    c = Fraction(a - b)
                    u = u0101
                elif op == '*':             # 乗法
                    c = Fraction(a * b)
                    u = u0102
                    op = "\\times "
                elif op == '/':             # 除法
                    c = Fraction(a, b)
                    if isFrac(c):
                        continue
                    u = u0102
                    op = "\\div "

                if abs(c) > 15:
                    continue

                lhs = a
                rhs = b
                if b < 0 and op != '':
                    rhs = f'({b})'

                expr = []
                if lhs > 0:
                    expr.append(f'{lhs}{op}{rhs}')
                else:
                    expr.append(f'{lhs}{op}{rhs}')
                    expr.append(f'({lhs}){op}{rhs}')

                for e in expr:
                    u.question_set.create(
                        question_text=f'${e}$ を計算しなさい。',
                        answer_text=f'${c}$',
                        source_text="自動生成"
                    )
                    count += 1
    return f'{count}問を自動生成しました。'


class Command(BaseCommand):
    """
    import_questions カスタムコマンド
    python manage.py import_questions で実行できる
    resources/計算問題.tex から問題をデータベースに投入する
    """
    help = 'Clear tables and import questions from TeX file.'

    def handle(self, *args, **options):
        # resources/計算問題.tex へのパスを取得する
        path = os.path.dirname(__file__)
        path = os.path.join(path, '../../resources/計算問題.tex')
        path = os.path.normpath(path)
        # self.stdout.write(path)

        with open(path, encoding='utf-8') as f:
            # 既存データを削除する
            tables = [
                # 'api_printdetail_units',
                # 'api_printdetail',
                # 'api_printhead',
                # 'api_printtype',
                'api_question',
                # 'api_unit',
                # 'api_grade',
                # 'api_archive',
            ]
            cursor = connection.cursor()
            for table in tables:
                cursor.execute(f"DELETE FROM {table}")
                self.stdout.write(f"DELETE FROM {table}")
                # 自動採番もリセットする
                try:
                    # sqlite3
                    cursor.execute(
                        f"DELETE FROM sqlite_sequence WHERE name = '{table}'")
                except Exception:
                    pass

                try:
                    # postgresql
                    cursor.execute(
                        f"select setval ('{table}_id_seq', 1, false)"
                    )
                except Exception:
                    pass

            if Grade.objects.count() == 0:
                # 学年マスタを作成する
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
                    g = Grade(
                        grade_code=f'00{index + 1}'[-2:], grade_text=text)
                    g.save()

            isQuestion = True
            question_list: List[str] = []
            answer_list: List[str] = []
            url_text: str = ''

            for line in f:
                # 改行削除
                line = line.rstrip()
                if (match := re.search(r'%define ([^ ]+) (\d{4}) (.+)$', line)):
                    # 単元マスタを更新する
                    grade_text = match.group(1).strip()
                    unit_code = match.group(2).strip()
                    unit_text = match.group(3).strip()

                    g = Grade.objects.get(grade_text=grade_text)
                    if not g:
                        sys.exit(f'grade not found : {grade_text}')
                    try:
                        u = Unit.objects.get(
                            grade=g, unit_code=unit_code, unit_text=unit_text)
                    except Unit.DoesNotExist:
                        try:
                            u = Unit.objects.get(grade=g, unit_code=unit_code)
                            u.unit_text = unit_text
                            u.save()
                        except Unit.DoesNotExist:
                            try:
                                u = Unit.objects.get(
                                    grade=g, unit_text=unit_text)
                                u.unit_code = unit_code
                                u.save()
                            except Unit.DoesNotExist:
                                g.unit_set.create(
                                    unit_code=unit_code, unit_text=unit_text)
                elif (match := re.search(r'%%URL (.+)$', line)):
                    # 出典URLを保持しておく
                    url_text = match.group(1).strip()
                elif re.search(r'\\item ', line):
                    # 問題と解答を保持しておく
                    # 問題->解答->問題->解答...を前提に isQuestion を反転させることで
                    # 保存先リストを切り替える
                    if isQuestion:
                        question_list.append(f'{line}, {url_text}')
                    else:
                        answer_list.append(line)
                    isQuestion = not isQuestion

            if len(question_list) != len(answer_list):
                sys.exit('問題と答えの数が違います。')

            autogen_unit_codes = [
                '0101', '0102', '0103', '0105', '0201'
            ]
            # 0101
            # 0102
            result = binary_number_question()
            self.stdout.write(result)
            # 0103
            result = exponents_question()
            self.stdout.write(result)
            # 0105
            result = ternary_number_question()
            self.stdout.write(result)
            # 0201
            result = charaexp_addsub_question()
            self.stdout.write(result)

            count = 0
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

                if unit_code not in autogen_unit_codes:
                    u = Unit.objects.get(unit_code=unit_code)
                    if not u:
                        sys.exit(f'単元コードが未定義です : {unit_code}')

                    try:
                        u.question_set.create(
                            question_text=question_text,
                            answer_text=answer_text,
                            source_text=source_text,
                            url_text=url_text
                        )
                        count += 1
                    except IntegrityError:
                        self.stdout.write(question_text)

            self.stdout.write(f'{count}問をインポートしました。')
