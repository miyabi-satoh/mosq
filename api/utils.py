import datetime
import os
import textwrap
import subprocess
from django.core.files import File
from mako.template import Template
from .models import PrintDetail, PrintHead, Question
from config.settings import BASE_DIR


def print_contest_pdf(printhead: PrintHead) -> File:
    template = ''
    tmplPath = os.path.join(BASE_DIR, 'api', 'resources',
                            'templates', 'contest.tex')
    with open(tmplPath, 'r') as f:
        template = f.read()

    if not template:
        return None

    template = template.replace("\\_", '_')
    template = template.replace("@[", "${")
    template = template.replace("]@", "}")

    items = []
    printdetails = PrintDetail.objects.filter(printhead=printhead).all()
    for detail in printdetails:
        query_sets = Question.objects.filter(unit=detail.unit).order_by('?')[
            :detail.quantity]
        for q in query_sets:
            items.append(q)

    dt_now = datetime.datetime.now()
    filename = dt_now.strftime('%Y%m%d_%H%M%S%f')
    with open(f'{filename}.tex', 'w') as f:
        mt = Template(template)
        f.write(
            mt.render(
                title=printhead.title,
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


def create_print(printhead: PrintHead) -> File:
    question_list = []
    answer_list = []
    printdetails = PrintDetail.objects.filter(printhead=printhead).all()
    for detail in printdetails:
        questions = Question.objects.filter(unit=detail.unit).order_by('?')[
            :detail.quantity]
        for question in questions:
            question_text = r'\item \begin{minipage}[t][4.72cm][t]{\linewidth}' + "\n"
            question_text += question.question_text.replace(
                r'\item ', '') + "\n"
            question_text += r'''
                \vfill
                \hfill
                \framebox[0.5\linewidth]{\rule{0ex}{7mm}}
                \end{minipage}
            '''
            question_list.append(question_text)
            answer_list.append(question.answer_text + "\n")

    document_header = r'''
        \documentclass[uplatex,a4j,11pt]{jsarticle}
        \usepackage[margin=15mm]{geometry}
        \usepackage{emath}
        \usepackage{titlesec}
        \usepackage{bxpapersize}
        \usepackage{multicol}
        \usepackage{enumitem}
        \usepackage{fancyhdr}

        \setlength\parindent{0pt}

        \setlist[enumerate]{
        leftmargin=*,
        itemindent=0pt,
        itemsep=1mm,
        labelsep=1ex,
        label=(\arabic*)}

        \pagestyle{fancy}
        \lhead{''' + printhead.title + r'''}

        \titleformat{\chapter}[hang]
        {\large}{}{0pt}{
        }[
        \hrule
        ]
        \titlespacing*{\chapter}{0pt}{-3em}{2em}

        \renewcommand{\thesection}{\arabic{section}}
        \titleformat{\section}[hang]
        {\Huge\bfseries\upshape}{}{0pt}{
        }[
        ]
        \titlespacing*{\section}{0pt}{3em}{0pt}

        \begin{document}
    '''

    question_header = r'''
        \begin{enumerate}
    '''

    question_footer = r'''
        \end{enumerate}
    '''

    answer_header = r'''
        \begin{multicols}{3}
        \begin{enumerate}
    '''

    answer_footer = r'''
        \end{enumerate}
        \newpage
        \end{multicols}
    '''

    document_footer = r'''
        \end{document}
    '''

    dt_now = datetime.datetime.now()
    filename = dt_now.strftime('%Y%m%d_%H%M%S%f')
    with open(f'{filename}.tex', 'w') as f:
        f.write(textwrap.dedent(document_header)[1:-1])
        f.write(textwrap.dedent(question_header))
        f.writelines(question_list)
        f.write(textwrap.dedent(question_footer))
        f.write(r'\newpage' + "\n")
        f.write(r'\lhead{' + printhead.title + r'解答}')
        f.write(textwrap.dedent(answer_header))
        f.writelines(answer_list)
        f.write(textwrap.dedent(answer_footer))
        f.write(textwrap.dedent(document_footer))

    cp = subprocess.run(['latexmk', f'{filename}.tex'])
    if cp.returncode != 0:
        file = None
    else:
        file = File(open(f'{filename}.pdf', 'rb'))
    subprocess.run(['latexmk', '-C', f'{filename}.tex'])
    os.remove(f'{filename}.tex')

    return file
