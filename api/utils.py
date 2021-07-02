import datetime
import os
import subprocess
from django.core.files import File
from mako.template import Template
from .models import PrintDetail, PrintHead, Question


def print_contest_pdf(printhead: PrintHead, title: str) -> File:
    template = ''
    with open(printhead.printtype.template.path, 'r', encoding='utf-8') as f:
        template = f.read()

    if not template:
        return None

    template = template.replace("\\_", '_')
    template = template.replace("@[", "${")
    template = template.replace("]@", "}")

    items = []
    printdetails = PrintDetail.objects.filter(printhead=printhead).all()
    for detail in printdetails:
        query_sets = (
            Question.objects
            .filter(unit__in=detail.units.all())
            .order_by('?')[:detail.quantity]
        )
        for q in query_sets:
            items.append(q)

    dt_now = datetime.datetime.now()
    filename = dt_now.strftime('%Y%m%d_%H%M%S%f')
    with open(f'{filename}.tex', 'w', encoding='utf-8') as f:
        mt = Template(template)
        f.write(
            mt.render(
                title=title,
                items=items,
            )
        )

    cp = subprocess.run(['latexmk', f'{filename}.tex'])
    if cp.returncode != 0:
        file = None
    else:
        file = File(open(f'{filename}.pdf', 'rb'))
    subprocess.run(['latexmk', '-C', f'{filename}.tex'])
    os.remove(f'{filename}.tex')

    return file


def print_minitest_pdf(printhead: PrintHead, title: str) -> File:
    template = ''
    with open(printhead.printtype.template.path, 'r', encoding='utf-8') as f:
        template = f.read()

    if not template:
        return None

    template = template.replace("\\_", '_')
    template = template.replace("@[", "${")
    template = template.replace("]@", "}")

    printdetails = PrintDetail.objects.filter(printhead=printhead).all()
    sections = []
    selected = []
    for i in range(8):
        items = []
        for detail in printdetails:
            query_sets = (
                Question.objects
                .filter(unit__in=detail.units.all())
                .exclude(pk__in=selected)
                .order_by('?')[:detail.quantity]
            )
            for q in query_sets:
                items.append(q)
                selected.append(q.id)
        sections.append(items)

    dt_now = datetime.datetime.now()
    filename = dt_now.strftime('%Y%m%d_%H%M%S%f')
    with open(f'{filename}.tex', 'w', encoding='utf-8') as f:
        mt = Template(template)
        f.write(
            mt.render(
                title=title,
                data=sections,
            )
        )

    cp = subprocess.run(['latexmk', f'{filename}.tex'])
    if cp.returncode != 0:
        file = None
    else:
        file = File(open(f'{filename}.pdf', 'rb'))
    subprocess.run(['latexmk', '-C', f'{filename}.tex'])
    os.remove(f'{filename}.tex')

    return file
