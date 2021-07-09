import os
import sys
import re
from fractions import Fraction
from typing import List
from django.core.management.base import BaseCommand
from django.db import connection, IntegrityError
from ...models import Grade, Unit


class CharaExpr:
    """
    文字式 a(bx + cy) を表現するクラス
    """

    def __init__(self, a, b, c, x='x', y='y') -> None:
        self.a = Fraction(a)
        self.b = Fraction(b)
        self.c = Fraction(c)
        self.x = x
        self.y = y

    def isExpandable(self) -> bool:
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

    def getInnerStr(self) -> str:
        """
        カッコ内 bx + cy の文字列化
        """
        bx = to_product(self.b, self.x)
        cy = to_product(self.c, self.y)
        if self.c > 0:
            cy = '+' + cy

        return bx + cy

        # inner = ''
        # if self.b == -1:
        #     inner += '-'
        # elif self.b != 1:
        #     inner += emath_bunsuu(self.b)
        # inner += self.x

        # if self.c > 0:
        #     inner += '+'
        #     if self.c != 1:
        #         inner += emath_bunsuu(self.c)
        #     elif self.y == '':
        #         inner += '1'
        # elif self.c == -1:
        #     inner += '-'
        #     if self.y == '':
        #         inner += '1'
        # else:
        #     inner += emath_bunsuu(self.c)
        # inner += self.y

    def __eq__(self, o: object) -> bool:
        return self.a == o.a and self.b == o.b and self.c == o.c

    def __str__(self) -> str:
        # inner = ''
        # if self.b == -1:
        #     inner += '-'
        # elif self.b != 1:
        #     inner += emath_bunsuu(self.b)
        # inner += self.x

        # if self.c > 0:
        #     inner += '+'
        #     if self.c != 1:
        #         inner += emath_bunsuu(self.c)
        #     elif self.y == '':
        #         inner += '1'
        # elif self.c == -1:
        #     inner += '-'
        #     if self.y == '':
        #         inner += '1'
        # else:
        #     inner += emath_bunsuu(self.c)
        # inner += self.y

        inner = self.getInnerStr()
        if self.isExpandable():
            sign = '-' if self.a < 0 else ''
            return sign + "\\bunsuu{" + inner + "}{" + f'{self.a.denominator}' + "}"

        if self.a == 1:
            return inner

        sign = '-' if self.a == -1 else emath_bunsuu(self.a)
        if self.b.denominator != 1 or self.c.denominator != 1:
            inner = f'\\left({inner}\\right)'
        else:
            inner = f'({inner})'

        return sign + inner


def getNumbers(r: int, m: int) -> List[Fraction]:
    listNum: list[Fraction] = []
    for a in range(r * -1, r + 1):
        if a == 0:
            continue
        for b in range(1, m + 1):
            if b == 0:
                continue
            x = Fraction(a, b)
            if x.denominator != b:
                continue
            if isFrac(x) and abs(x.numerator) > 4:
                continue
            listNum.append(x)

    return listNum


def to_product(n: Fraction, c: str) -> str:
    """
    文字式の積の形を返す
    """
    if c == '':
        return emath_bunsuu(n)
    if n == 0:
        return '0'
    if n == 1:
        return c
    if n == -1:
        return f'-{c}'
    return emath_bunsuu(n) + c


def isFrac(x: Fraction) -> bool:
    return x.denominator != 1


def isInteger(x: Fraction) -> bool:
    return x.denominator == 1


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


def getCharaExprs(listNum: List[Fraction], charX='x', charY='y') -> List[CharaExpr]:
    listCharaExpr: list[CharaExpr] = []
    for a in listNum:
        if a.denominator > 4:
            continue
        if isFrac(a) and abs(a.numerator) > 2:
            continue
        for b in listNum:
            if isFrac(a) and isFrac(b):
                continue

            if a == b:
                # a,bが同数はナシ
                continue
            if b < 0 and a != 1:
                # bが負の数ならa=1
                continue
            if isFrac(b) and isFrac(a):
                # bが分数ならaは整数
                continue
            for c in listNum:
                if isFrac(a) and isFrac(b):
                    continue
                if a < 0 and b < 0 and c < 0:
                    continue
                if isInteger(a) and isInteger(b) and isInteger(c):
                    if abs(b) % 2 == 0 and abs(c) % 2 == 0:
                        continue
                if isFrac(b) and isInteger(c):
                    if a != 1:
                        continue

                if b == c:
                    # b,cが同数はナシ
                    continue
                if a == c and abs(a) != 1:
                    # a,cが同数は±1のみOK
                    continue
                if isFrac(c):
                    # cが分数なら
                    if abs(a) < 3:
                        # aは±3以上の整数
                        continue
                    if isInteger(b):
                        # bも分数
                        continue
                    if c.denominator == b.denominator:
                        # bとは異分母
                        continue
                    if isFrac(b):
                        if abs(b.numerator) != 1 and abs(c.numerator) != 1:
                            continue
                        ab = a * b
                        ac = a * c
                        if ab.denominator == b.denominator and ac.denominator == c.denominator:
                            continue
                        if isFrac(ab) and isFrac(ac):
                            continue

                listCharaExpr.append(CharaExpr(a, b, c, charX, charY))
    return listCharaExpr


def integer_addsub_question() -> str:
    """
    整数のたし算・ひき算
    """
    count = 0

    u_add: List[Unit] = []
    u_sub: List[Unit] = []
    for x in range(0, 3):
        u = Unit.objects.get(unit_code=f'100{x}')
        u_add.append(u)
        u = Unit.objects.get(unit_code=f'101{x}')
        u_sub.append(u)

    for a in range(1, 10):
        for b in range(1, 10):
            x = a + b
            for c in range(0, 10):
                lhs = a + c * 10
                for d in range(0, 10):
                    carried = 0
                    if a + b > 9:
                        carried += 1
                    if c + d + carried > 9:
                        carried += 1

                    rhs = b + d * 10
                    ans = lhs + rhs

                    u_add[carried].question_set.create(
                        question_text=f'${lhs}+{rhs} = $',
                        answer_text=f'${ans}$',
                        source_text="自動生成"
                    )
                    u_sub[carried].question_set.create(
                        question_text=f'${ans}-{rhs} = $',
                        answer_text=f'${lhs}$',
                        source_text="自動生成"
                    )
                    count += 1

    return f'{count}問を自動生成しました。'


def charaexp_mul_question() -> str:
    """
    文字式 × 数を作る
    """
    u = Unit.objects.get(unit_code="0117")

    listNum = getNumbers(9, 10)
    listCharExpr = getCharaExprs(listNum, 'x', '')

    count = 0
    for e in listCharExpr:
        if e.isExpandable():
            if e.a < 0:
                continue
            for x in range(-9, 10):
                if abs(x) <= 1:
                    continue
                if abs(x) % e.a.denominator == 0:
                    expr = str(e) + '\\times '
                    if x < 0:
                        expr += f'\\left({x}\\right)'
                    else:
                        expr += f'{x}'
                    ansX = to_product(e.a * e.b * x, e.x)
                    ansY = e.a * e.c * x
                    if ansY > 0:
                        ans = f'{ansX}+{ansY}'
                    else:
                        ans = f'{ansX}{ansY}'

                    u.question_set.create(
                        question_text=f'${expr}$ を計算しなさい。',
                        answer_text=f'${ans}$',
                        source_text="自動生成"
                    )
                    count += 1
        elif abs(e.a) != 1:
            expr = f'\\left({e.getInnerStr()}\\right)'
            expr += '\\times '
            if e.a > 0:
                expr += emath_bunsuu(e.a)
            else:
                expr += f'\\left({emath_bunsuu(e.a)}\\right)'

            ansX = to_product(e.a * e.b, e.x)
            ansY = e.a * e.c
            if ansY > 0:
                ans = f'{ansX}+{emath_bunsuu(ansY)}'
            else:
                ans = f'{ansX}{emath_bunsuu(ansY)}'

            u.question_set.create(
                question_text=f'${expr}$ を計算しなさい。',
                answer_text=f'${ans}$',
                source_text="自動生成"
            )
            count += 1

    return f'{count}問を自動生成しました。'


def charaexp_addsub_question(unit_code: str) -> str:
    """
    文字式の加法・減法を作る
    """
    u = Unit.objects.get(unit_code=unit_code)
    charX = 'x'
    if unit_code[1] == '1':
        charY = ''
    else:
        charY = 'y'

    # listNum: list[Fraction] = []
    # for a in range(-9, 10):
    #     if a == 0:
    #         continue
    #     for b in range(1, 11):
    #         if b == 0:
    #             continue
    #         x = Fraction(a, b)
    #         if x.denominator != b:
    #             continue
    #         if isFrac(x) and abs(x.numerator) > 4:
    #             continue
    #         listNum.append(x)

    listNum = getNumbers(9, 10)
    listCharaExpr: list[CharaExpr] = []
    for a in listNum:
        if a.denominator > 4:
            continue
        if isFrac(a) and abs(a.numerator) > 2:
            continue
        for b in listNum:
            if isFrac(a) and isFrac(b):
                continue

            if a == b:
                # a,bが同数はナシ
                continue
            if b < 0 and a != 1:
                # bが負の数ならa=1
                continue
            if isFrac(b) and isFrac(a):
                # bが分数ならaは整数
                continue
            for c in listNum:
                if isFrac(a) and isFrac(b):
                    continue
                if a < 0 and b < 0 and c < 0:
                    continue
                if isInteger(a) and isInteger(b) and isInteger(c):
                    if abs(b) % 2 == 0 and abs(c) % 2 == 0:
                        continue
                if isFrac(b) and isInteger(c):
                    if a != 1:
                        continue

                if b == c:
                    # b,cが同数はナシ
                    continue
                if a == c and abs(a) != 1:
                    # a,cが同数は±1のみOK
                    continue
                if isFrac(c):
                    # cが分数なら
                    if abs(a) < 3:
                        # aは±3以上の整数
                        continue
                    if isInteger(b):
                        # bも分数
                        continue
                    if c.denominator == b.denominator:
                        # bとは異分母
                        continue
                    if isFrac(b):
                        if abs(b.numerator) != 1 and abs(c.numerator) != 1:
                            continue
                        ab = a * b
                        ac = a * c
                        if ab.denominator == b.denominator and ac.denominator == c.denominator:
                            continue
                        if isFrac(ab) and isFrac(ac):
                            continue

                listCharaExpr.append(CharaExpr(a, b, c, charX, charY))

    count = 0
    for expr_a in listCharaExpr:
        # a
        if expr_a.a < 0 or 6 < expr_a.a:
            # [0 ... 6]
            continue
        if expr_a.a == 1:
            if expr_a.b < 1:
                continue
        # b
        if expr_a.b < 0 or 8 < expr_a.b:
            # [0 ... 8]
            continue
        if isFrac(expr_a.b):
            # 1/2, 3/2, 1/3, 2/3のみ
            if expr_a.b.denominator > 3 or expr_a.b.numerator > 3:
                continue
            # cはマイナスのみ
            if expr_a.c > 0:
                continue
        # c
        if abs(expr_a.c) > 6:
            # [-6 ... 6]
            continue
        if abs(expr_a.b) == abs(expr_a.c):
            continue

        for expr_b in listCharaExpr:
            if isFrac(expr_a.c) and isFrac(expr_b.c):
                # cが分数ならc'は整数
                continue
            if isFrac(expr_a.a) and isFrac(expr_b.a):
                if abs(expr_a.a.numerator) != 1 or abs(expr_b.a.numerator) != 1:
                    continue
            # a'
            if expr_b.a > 0 and isFrac(expr_b.a):
                if expr_b.c > 0:
                    continue
            if abs(expr_b.a) > 5:
                continue
            if expr_a.a == 1:
                if abs(expr_b.a) > 1:
                    continue
                if isFrac(expr_b.a) and abs(expr_b.a.numerator) != 1:
                    continue
                if isFrac(expr_a.b):
                    if isInteger(expr_b.a):
                        continue
            if abs(expr_a.a) == abs(expr_b.a):
                continue
            if expr_a.a == 1 and isFrac(expr_a.b):
                if expr_a.b.denominator == expr_b.a.denominator:
                    continue
            if isFrac(expr_a.b) and isFrac(expr_a.c):
                if abs(expr_b.a) != 1:
                    continue
                if expr_b.b > 0 and expr_b.c > 0:
                    continue

            # b'
            if expr_a.b == expr_b.b:
                continue
            # c'
            if abs(expr_b.b) == abs(expr_b.c):
                if abs(expr_b.b) != 1:
                    continue

            if expr_a.isExpandable():
                if abs(expr_b.a) == 1:
                    pass
                elif expr_b.isExpandable():
                    pass
                else:
                    continue
            if expr_b.isExpandable():
                if abs(expr_a.a) == 1:
                    pass
                elif expr_a.isExpandable():
                    pass
                else:
                    continue
            if expr_b.c > 0 and expr_a.a > 1:
                continue
            if expr_b.a > 0 and expr_b.b > 0 and expr_b.c > 0:
                continue
            if isFrac(expr_b.b) and isFrac(expr_b.c):
                if isFrac(expr_a.a) or isFrac(expr_a.b) or isFrac(expr_a.c):
                    continue

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
            if ansX < 0 and ansY < 0:
                continue
            if ansX > 0 and ansY > 0:
                continue
            if abs(ansX) == abs(ansY):
                continue

            ansX = to_product(ansX, charX)
            if ansX == '0':
                ansX = ''

            op = ''
            if ansX != '' and ansY > 0:
                op = '+'

            ansY = to_product(ansY, charY)
            if ansY == '0':
                ansY = ''

            # if ansY == 0:
            #     ansY = ""
            # elif ansY == 1:
            #     ansY = "+" + charY
            # elif ansY == -1:
            #     ansY = "-" + ("1" if charY == '' else charY)
            # else:
            #     sign = '+' if ansX != 0 and ansY > 0 else ''
            #     ansY = sign + emath_bunsuu(ansY) + charY

            strA = str(expr_a)
            strB = str(expr_b)
            if expr_b.a > 0:
                if expr_b.a == 1 and expr_b.b < 0:
                    pass
                else:
                    strB = '+' + strB

            u.question_set.create(
                question_text=f'${strA}{strB}$ を計算しなさい。',
                answer_text=f'${ansX}{op}{ansY}$',
                source_text="自動生成"
            )
            count += 1
            # if count > 9999:
            #     return "中断しました。"

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


def binary_number_question() -> str:
    """
    正負の二項計算を作る
    """
    u = Unit.objects.get(unit_code='0100')

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
                elif op == '-':             # 減法
                    c = Fraction(a - b)
                elif op == '*':             # 乗法
                    c = Fraction(a * b)
                    op = "\\times "
                elif op == '/':             # 除法
                    c = Fraction(a, b)
                    if isFrac(c):
                        continue
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
                    '小学',
                    '中学',
                    '高校'
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

            # 0100：正負の二項計算
            result = binary_number_question()
            self.stdout.write("0100 : " + result)
            # 0105：正負の四則混合
            result = ternary_number_question()
            self.stdout.write("0105 : " + result)
            # 0117：分子式×数
            result = charaexp_mul_question()
            self.stdout.write("0117 : " + result)
            # 0118：展開と整理
            result = charaexp_addsub_question('0118')
            self.stdout.write("0118 : " + result)
            # 0201：多項式の計算
            result = charaexp_addsub_question('0201')
            self.stdout.write("0201 : " + result)
            # 100x, 101x：たし算、ひき算
            result = integer_addsub_question()
            self.stdout.write("10xx : " + result)

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
