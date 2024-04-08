import os
import subprocess
import csv
from typing import TextIO

from constants import UnitAssesments, CSV_FIELD_NAMES
from debug import debug_print
from retrieval import get_assesments_for_units

FILENAME = "timetable"
EXTENSION = "tex"
LATEX_TO_PDF_COMMAND = "pdflatex"
LATEX_COMMENT = '%'
DEFAULT_PDF_FOLDER = "."

DEFAULT_MARGIN_SIZE = 2
DEFAULT_HEADING_SIZE = 18
DEFAULT_SPACING = 2.5
LINES_BETWEEN_ROWS = True

NEWLINE = '\n'
HLINE = r"\hline" + NEWLINE
LINE_END = r" \\"
INDENT = "    "

DOCUMENT_BEGINNING_TEXT = r"""\documentclass{article}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{geometry}

\newcommand{\tabletitle}[2]{\begin{center}\fontsize{#1}{#1}\selectfont \textbf{#2}\end{center}}
"""

MARGIN_TEXT = r"""\geometry{{
    left={}cm,
    right={}cm,
}}
"""
BEGIN_DOCUMENT = r"\begin{document}" + NEWLINE
TABLE_FORMAT_TEXT = r"""\tabletitle{{{}}}{{{}}}
\begin{{table}}[htbp]
    \centering
    \renewcommand{{\arraystretch}}{{{}}}
"""
TABLE_BEGINNING_TEXT = r"\begin{{tabularx}}{{\textwidth}}{{{}}}" + NEWLINE
TABLE_HEADING_FORMAT = r"\textbf{{{}}}"

TABLE_END = r"""\end{tabularx}
\end{table}

\newpage
"""

DOCUMENT_END = r"\end{document}"

def _document_beginning(tex_file: TextIO, margin_size: int = DEFAULT_MARGIN_SIZE):
    tex_file.write(DOCUMENT_BEGINNING_TEXT)
    tex_file.write(MARGIN_TEXT.format(margin_size, margin_size))
    tex_file.write(BEGIN_DOCUMENT)

def _table_beginning(tex_file: TextIO, unit_code: str, 
                    column_headings: list[str] | tuple[str], 
                    heading_size: int = DEFAULT_HEADING_SIZE,
                    row_spacing: float = DEFAULT_SPACING):
    table_format_builder = ['|']
    table_headings_builder = []
    tex_file.write(TABLE_FORMAT_TEXT.format(heading_size, unit_code, row_spacing))
    for i, column_heading in enumerate(column_headings, start=1):
        if i == 4:
            table_format_builder.append("l|")
        else:
            table_format_builder.append("X|")
        table_headings_builder.append(TABLE_HEADING_FORMAT.format(column_heading.capitalize()))

    table_headings = " & ".join(table_headings_builder) + LINE_END
    table_format = ''.join(table_format_builder)
    tex_file.write(INDENT)
    tex_file.write(TABLE_BEGINNING_TEXT.format(table_format))
    tex_file.write(INDENT)
    tex_file.write(HLINE)
    tex_file.write(INDENT)
    tex_file.write(table_headings)
    tex_file.write(NEWLINE)
    tex_file.write(INDENT)
    tex_file.write(HLINE)

def _table_row(tex_file: TextIO, row: list[str]):
    for i, value in enumerate(row):
        if value is None:
            row[i] = value = ""
        if LATEX_COMMENT in value:
            # Escape any % characters to ensure they do not appear as comments
            row[i] = value.replace(LATEX_COMMENT, '\\' + LATEX_COMMENT)

    tex_file.write(INDENT)
    tex_file.write(" & ".join(row))
    tex_file.write(LINE_END)
    tex_file.write(NEWLINE)
    if LINES_BETWEEN_ROWS:
        tex_file.write(INDENT)
        tex_file.write(HLINE)

def _table_end(tex_file: TextIO):
    if not LINES_BETWEEN_ROWS:
        tex_file.write(INDENT)
        tex_file.write(HLINE)
    tex_file.write(INDENT)
    tex_file.write(TABLE_END)

def _document_end(tex_file: TextIO):
    tex_file.write(NEWLINE)
    tex_file.write(DOCUMENT_END)

def write_csv_to_latex(tex_file: TextIO, csv_path: str):
    unit_code = os.path.basename(csv_path).split('.')[0].upper()
    with open(csv_path) as csv_file:
        reader = iter(csv.reader(csv_file))
        column_headings = next(reader)
        
        _table_beginning(tex_file, unit_code, column_headings)
        for row in reader:
            _table_row(tex_file, row)
        _table_end(tex_file)

def write_unit_assesments_to_latex(tex_file: TextIO, unit_code: str, unit_assesments: UnitAssesments):
    _table_beginning(tex_file, unit_code, CSV_FIELD_NAMES)
    for unit_assesment in unit_assesments:
        row = list(map(unit_assesment.get, CSV_FIELD_NAMES))
        _table_row(tex_file, row)
    _table_end(tex_file)

def _compile_pdf(pdf_folder: str, tex_path: str, delete_tex: bool):
    try:
        subprocess.run(f"cd {pdf_folder}; {LATEX_TO_PDF_COMMAND} {tex_path}", shell=True, stdout=subprocess.DEVNULL)
    except:
        debug_print("Failed to generate PDF.")
        return
    else:
        print("Generated assesment timetable.")
    finally:
        _delete_files(pdf_folder, tex_path, delete_tex)

def _delete_files(pdf_folder: str, tex_path: str, delete_tex: bool):
    if delete_tex:
        subprocess.run(["rm", tex_path], stdout=subprocess.DEVNULL)

    subprocess.run(["rm", os.path.join(pdf_folder, f"{FILENAME}.aux")], stdout=subprocess.DEVNULL)
    subprocess.run(["rm", os.path.join(pdf_folder, f"{FILENAME}.log")], stdout=subprocess.DEVNULL)

def assesment_timetable_from_csv(csv_paths: list[str], 
                                 pdf_folder: str = DEFAULT_PDF_FOLDER, 
                                 delete_tex: bool = True):
    tex_path = os.path.join(pdf_folder, FILENAME)
    with open(tex_path, "w+") as tex_file:
        _document_beginning(tex_file)
        for csv_path in csv_paths:
            write_csv_to_latex(tex_file, csv_path)
        _document_end(tex_file)
    
    _compile_pdf(pdf_folder, tex_path, delete_tex)

def assesment_timetable(unit_codes: list[str], 
                        pdf_folder: str = DEFAULT_PDF_FOLDER, 
                        semester: int = 1,
                        delete_tex: bool = True):
    tex_path = os.path.join(pdf_folder, FILENAME + '.' + EXTENSION)
    assesments_for_units = get_assesments_for_units(unit_codes, semester=semester)
    with open(tex_path, "w+") as tex_file:
        _document_beginning(tex_file)
        for unit_code, unit_assesments in assesments_for_units.items():
            write_unit_assesments_to_latex(tex_file, unit_code, unit_assesments)
        _document_end(tex_file)
    
    exit()
    _compile_pdf(pdf_folder, tex_path, delete_tex)


    

