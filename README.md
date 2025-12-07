# MD2PDF - Quick Markdown to PDF Converter

Simple, fast tool to convert Markdown files to nicely formatted PDFs.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Convert a file
python md2pdf.py README.md

# Specify output name
python md2pdf.py input.md output.pdf

# Convert all markdown files
python md2pdf.py *.md
```

## Features

✅ **Headings** - # ## ### styled with different sizes
✅ **Bold** - `**bold**` or `__bold__`
✅ **Italic** - `*italic*` or `_italic_`
✅ **Code blocks** - ``` code ```
✅ **Inline code** - \`code\`
✅ **Lists** - Bullet points
✅ **Links** - `[text](url)` (blue underlined)
✅ **Auto-styling** - Nice colors and spacing

## Usage Examples

### Convert Single File

```bash
python md2pdf.py documentation.md
```

Creates `documentation.pdf` in the same folder.

### Specify Output

```bash
python md2pdf.py input.md my-output.pdf
```

### Convert Multiple Files

```bash
# All markdown files in current directory
python md2pdf.py *.md

# Specific pattern
python md2pdf.py docs/*.md
```

### As a Module

```python
from md2pdf import MarkdownToPDF

converter = MarkdownToPDF()
converter.convert('input.md', 'output.pdf')
```

## Example Output

Input (Markdown):
```markdown
# My Document

This is **bold** and this is *italic*.

## Code Example

Here's some `inline code` and a block:

\```python
def hello():
    print("Hello, World!")
\```

## Lists

- First item
- Second item
- Third item
```

Output: Nicely formatted PDF with:
- Large heading for "My Document"
- Proper bold/italic rendering
- Syntax-highlighted code block
- Clean bullet list

## Supported Markdown

| Feature | Syntax | Supported |
|---------|--------|-----------|
| Heading 1 | `# Text` | ✅ |
| Heading 2 | `## Text` | ✅ |
| Heading 3 | `### Text` | ✅ |
| Bold | `**text**` | ✅ |
| Italic | `*text*` | ✅ |
| Code block | ` ``` ` | ✅ |
| Inline code | `` `code` `` | ✅ |
| Lists | `- item` | ✅ |
| Links | `[text](url)` | ✅ (styled) |
| Horizontal rule | `---` | ✅ |
| Images | `![](url)` | ❌ |
| Tables | `| a | b |` | ❌ |

## Configuration

Edit `md2pdf.py` to customize:

### Page Size

```python
converter = MarkdownToPDF(pagesize=A4)  # or letter (default)
```

### Styles

Modify `_create_custom_styles()` method in `md2pdf.py`:

```python
# Change heading color
self.styles['Heading1'].textColor = colors.blue

# Change font size
self.styles['Heading1'].fontSize = 28

# Change body text
self.styles['CustomBody'].fontSize = 12
self.styles['CustomBody'].leading = 18  # line height
```

## Requirements

- Python 3.6+
- reportlab
- markdown (optional, for advanced features)

## Installation

```bash
# Clone or download
cd md2pdf

# Install dependencies
pip install -r requirements.txt

# Use it
python md2pdf.py your-file.md
```

## Advanced Usage

### Batch Convert with Custom Names

```python
from md2pdf import MarkdownToPDF
from pathlib import Path

converter = MarkdownToPDF()

# Convert all docs
for md_file in Path('docs').glob('*.md'):
    pdf_file = f"pdfs/{md_file.stem}.pdf"
    converter.convert(str(md_file), pdf_file)
    print(f"✓ {md_file.name} → {pdf_file}")
```

### Custom Styling

```python
from md2pdf import MarkdownToPDF
from reportlab.lib import colors

converter = MarkdownToPDF()

# Customize before converting
converter.styles['Heading1'].textColor = colors.blue
converter.styles['Heading1'].fontSize = 28

converter.convert('doc.md', 'styled.pdf')
```

## Limitations

- No image embedding (yet)
- No table support (yet)
- Basic list support (no nested lists)
- No HTML passthrough

## Use Cases

✅ Convert documentation to PDF
✅ Create printable versions of README files
✅ Generate PDF reports from Markdown
✅ Quick document formatting
✅ Batch convert multiple files

## Tips

1. **Use simple markdown** - Complex features may not render perfectly
2. **Check output** - Review the PDF to ensure formatting is correct
3. **Adjust styles** - Modify the code to match your preferences
4. **Batch processing** - Use wildcards for multiple files

## Troubleshooting

**Error: No module named 'reportlab'**
```bash
pip install reportlab
```

**Error: File not found**
```bash
# Use full path
python md2pdf.py /full/path/to/file.md
```

**PDF looks wrong**
- Check your markdown syntax
- Ensure proper spacing around headings
- Close all code blocks with ```

## License

MIT - Free to use and modify
