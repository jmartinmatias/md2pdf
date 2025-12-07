#!/usr/bin/env python3
"""
Quick Markdown to PDF Converter

Simple tool to convert Markdown files to nicely formatted PDFs.
Supports code blocks, tables, lists, and basic formatting.
"""

import sys
import os
from pathlib import Path
import re
from typing import List, Tuple

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.platypus import Table, TableStyle, Preformatted, ListFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


class MarkdownToPDF:
    """Convert Markdown to PDF with basic formatting."""

    def __init__(self, pagesize=letter):
        self.pagesize = pagesize
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()

    def _create_custom_styles(self):
        """Create custom paragraph styles."""

        # Modify existing heading styles
        self.styles['Heading1'].fontSize = 24
        self.styles['Heading1'].textColor = colors.HexColor('#1a1a1a')
        self.styles['Heading1'].spaceAfter = 12
        self.styles['Heading1'].spaceBefore = 12
        self.styles['Heading1'].fontName = 'Helvetica-Bold'

        self.styles['Heading2'].fontSize = 18
        self.styles['Heading2'].textColor = colors.HexColor('#2a2a2a')
        self.styles['Heading2'].spaceAfter = 10
        self.styles['Heading2'].spaceBefore = 10
        self.styles['Heading2'].fontName = 'Helvetica-Bold'

        self.styles['Heading3'].fontSize = 14
        self.styles['Heading3'].textColor = colors.HexColor('#3a3a3a')
        self.styles['Heading3'].spaceAfter = 8
        self.styles['Heading3'].spaceBefore = 8
        self.styles['Heading3'].fontName = 'Helvetica-Bold'

        # Modify code style
        self.styles['Code'].fontSize = 9
        self.styles['Code'].fontName = 'Courier'
        self.styles['Code'].textColor = colors.HexColor('#333333')
        self.styles['Code'].backColor = colors.HexColor('#f5f5f5')
        self.styles['Code'].leftIndent = 20
        self.styles['Code'].rightIndent = 20
        self.styles['Code'].spaceAfter = 6
        self.styles['Code'].spaceBefore = 6

        # Add custom body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            leading=16,
            spaceAfter=6
        ))

    def parse_markdown(self, md_content: str) -> List:
        """Parse markdown and return ReportLab flowables."""
        flowables = []
        lines = md_content.split('\n')

        i = 0
        in_code_block = False
        code_block_lines = []
        in_list = False
        list_items = []

        while i < len(lines):
            line = lines[i]

            # Code blocks
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_block_lines = []
                else:
                    # End code block
                    code_text = '\n'.join(code_block_lines)
                    flowables.append(Preformatted(
                        code_text,
                        self.styles['Code']
                    ))
                    flowables.append(Spacer(1, 0.2*inch))
                    in_code_block = False
                    code_block_lines = []
                i += 1
                continue

            if in_code_block:
                code_block_lines.append(line)
                i += 1
                continue

            # Handle lists
            if line.strip().startswith(('-', '*', '+')):
                if not in_list:
                    in_list = True
                    list_items = []

                # Extract list item text
                item_text = re.sub(r'^[\-\*\+]\s+', '', line.strip())
                item_text = self._format_inline(item_text)
                list_items.append(Paragraph(item_text, self.styles['CustomBody']))
                i += 1
                continue

            elif in_list and line.strip() == '':
                # End of list
                if list_items:
                    flowables.append(ListFlowable(
                        list_items,
                        bulletType='bullet',
                        start='•'
                    ))
                    flowables.append(Spacer(1, 0.1*inch))
                in_list = False
                list_items = []
                i += 1
                continue

            # Headings
            if line.startswith('# '):
                if in_list and list_items:
                    flowables.append(ListFlowable(list_items, bulletType='bullet'))
                    in_list = False
                    list_items = []

                text = line[2:].strip()
                text = self._format_inline(text)
                flowables.append(Paragraph(text, self.styles['Heading1']))
                flowables.append(Spacer(1, 0.15*inch))

            elif line.startswith('## '):
                if in_list and list_items:
                    flowables.append(ListFlowable(list_items, bulletType='bullet'))
                    in_list = False
                    list_items = []

                # Add page break before Heading2
                flowables.append(PageBreak())

                text = line[3:].strip()
                text = self._format_inline(text)
                flowables.append(Paragraph(text, self.styles['Heading2']))
                flowables.append(Spacer(1, 0.12*inch))

            elif line.startswith('### '):
                if in_list and list_items:
                    flowables.append(ListFlowable(list_items, bulletType='bullet'))
                    in_list = False
                    list_items = []

                text = line[4:].strip()
                text = self._format_inline(text)
                flowables.append(Paragraph(text, self.styles['Heading3']))
                flowables.append(Spacer(1, 0.1*inch))

            # Horizontal rule
            elif line.strip() in ('---', '***', '___'):
                if in_list and list_items:
                    flowables.append(ListFlowable(list_items, bulletType='bullet'))
                    in_list = False
                    list_items = []

                flowables.append(Spacer(1, 0.2*inch))

            # Regular paragraphs
            elif line.strip():
                if in_list and list_items:
                    flowables.append(ListFlowable(list_items, bulletType='bullet'))
                    in_list = False
                    list_items = []

                text = self._format_inline(line.strip())
                flowables.append(Paragraph(text, self.styles['CustomBody']))
                flowables.append(Spacer(1, 0.05*inch))

            # Empty line
            else:
                if in_list and list_items:
                    flowables.append(ListFlowable(list_items, bulletType='bullet'))
                    flowables.append(Spacer(1, 0.1*inch))
                    in_list = False
                    list_items = []

            i += 1

        # Handle remaining list items
        if in_list and list_items:
            flowables.append(ListFlowable(list_items, bulletType='bullet'))

        return flowables

    def _format_inline(self, text: str) -> str:
        """Format inline markdown (bold, italic, code, links)."""

        # Escape XML special characters
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')

        # Inline code FIRST (to prevent nested formatting inside code)
        # Use a placeholder to protect code content from further processing
        code_parts = []
        def save_code(match):
            code_parts.append(match.group(1))
            return f'__CODE_PLACEHOLDER_{len(code_parts)-1}__'

        text = re.sub(r'`(.+?)`', save_code, text)

        # Bold (**text** or __text__)
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)

        # Italic (*text* or _text_) - avoid matching underscores in words
        text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
        text = re.sub(r'\b_(.+?)_\b', r'<i>\1</i>', text)

        # Links [text](url)
        text = re.sub(
            r'\[(.+?)\]\((.+?)\)',
            r'<font color="blue"><u>\1</u></font>',
            text
        )

        # Restore code parts with formatting
        for i, code in enumerate(code_parts):
            text = text.replace(
                f'__CODE_PLACEHOLDER_{i}__',
                f'<font name="Courier" color="#c7254e" backColor="#f9f2f4">{code}</font>'
            )

        return text

    def convert(self, md_file: str, pdf_file: str = None):
        """Convert markdown file to PDF."""

        # Read markdown file
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Determine output filename
        if pdf_file is None:
            pdf_file = str(Path(md_file).with_suffix('.pdf'))

        # Create PDF
        doc = SimpleDocTemplate(
            pdf_file,
            pagesize=self.pagesize,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Parse markdown and build PDF
        flowables = self.parse_markdown(md_content)

        # Add title from filename if no H1 in content
        if not any('Heading1' in str(f) for f in flowables[:5] if hasattr(f, 'style')):
            title = Path(md_file).stem.replace('-', ' ').replace('_', ' ').title()
            flowables.insert(0, Spacer(1, 0.2*inch))
            flowables.insert(0, Paragraph(title, self.styles['Heading1']))

        doc.build(flowables)

        return pdf_file


def main():
    """Command-line interface."""

    if len(sys.argv) < 2:
        print("Usage: python md2pdf.py <markdown_file> [output_pdf]")
        print("\nExamples:")
        print("  python md2pdf.py README.md")
        print("  python md2pdf.py doc.md output.pdf")
        print("  python md2pdf.py *.md  # Convert all .md files")
        sys.exit(1)

    # Get input files
    input_pattern = sys.argv[1]

    # Handle wildcards
    if '*' in input_pattern:
        from glob import glob
        input_files = glob(input_pattern)

        if not input_files:
            print(f"No files matching: {input_pattern}")
            sys.exit(1)

        print(f"Converting {len(input_files)} file(s)...")

        converter = MarkdownToPDF()

        for md_file in input_files:
            try:
                pdf_file = converter.convert(md_file)
                print(f"✓ {md_file} → {pdf_file}")
            except Exception as e:
                print(f"✗ {md_file}: {e}")

        print(f"\n✓ Converted {len(input_files)} files!")

    else:
        # Single file
        md_file = sys.argv[1]
        output_pdf = sys.argv[2] if len(sys.argv) > 2 else None

        if not os.path.exists(md_file):
            print(f"Error: File not found: {md_file}")
            sys.exit(1)

        print(f"Converting {md_file} to PDF...")

        converter = MarkdownToPDF()

        try:
            pdf_file = converter.convert(md_file, output_pdf)
            print(f"✓ Created: {pdf_file}")
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    main()
