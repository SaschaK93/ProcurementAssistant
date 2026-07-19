# PDF Download Function

# Import necessary libraries
import re                                                       # Provides regular expressions for detecting Markdown formatting
from datetime import date                                       # Used to insert the current date into the PDF report
from io import BytesIO                                          # Creates an in-memory binary stream for PDF data
from xml.sax.saxutils import escape                             # Escapes special characters for safe use in PDF paragraphs

from reportlab.lib.enums import TA_CENTER                       # Provides constants for text alignment
from reportlab.lib.pagesizes import A4                          # Defines the page size for the PDF document
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet   # Provides predefined styles and allows custom text styles
from reportlab.lib.units import mm                              # Allows margins and spacing to be defined in millimeters
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer
)


def format_markdown_text(text):
    # Converts basic Markdown bold formatting into ReportLab-compatible HTML formatting

    safe_text = escape(text)                                    # Escapes special XML characters before adding supported HTML tags

    formatted_text = re.sub(                                    # Replaces Markdown bold formatting such as **Price:** with HTML bold tags
        r"\*\*(.+?)\*\*",
        r"<b>\1</b>",
        safe_text
    )

    return formatted_text                                       # Returns the safely formatted text for use in a ReportLab paragraph


def create_procurement_report_pdf(report_text, supplier):
    # Creates a styled PDF from the procurement report and returns the PDF as bytes

    buffer = BytesIO()                                          # Creates an in-memory binary stream to hold the PDF data

    document = SimpleDocTemplate(                               # Creates a simple PDF document with custom page margins
        buffer,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()                              # Retrieves a set of predefined styles for text formatting

    # Create custom text styles
    title_style = ParagraphStyle(
        name="CustomTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        alignment=TA_CENTER,
        spaceAfter=12
    )

    metadata_style = ParagraphStyle(
        name="Metadata",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        spaceAfter=4
    )

    heading_style = ParagraphStyle(
        name="Heading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        spaceBefore=14,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        name="Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=15,
        spaceAfter=6
    )

    story = []                                                  # Initializes an empty list to hold the PDF content

    # Add the report title
    story.append(
        Paragraph(
            "AI Procurement Report",
            title_style
        )
    )

    # Add supplier information
    story.append(
        Paragraph(
            f"<b>Supplier:</b> {escape(supplier)}",             # Escapes special XML characters in the supplier name so they are displayed correctly
            metadata_style
        )
    )

    # Add the current date
    story.append(
        Paragraph(
            f"<b>Generated:</b> {date.today().strftime('%d %B %Y')}",
            metadata_style
        )
    )

    story.append(Spacer(1, 12))                                 # Adds vertical spacing after the report header

    # Define all report section headings
    section_headings = {
        "executive summary",
        "supplier overview",
        "commercial terms",
        "key commercial terms",
        "business risk assessment",
        "risk assessment",
        "negotiation strategy",
        "recommendations",
        "management summary",
        "missing information",
        "key findings",
        "conclusion"
    }

    # Process the report line by line
    for line in report_text.splitlines():

        clean_line = line.strip()                               # Removes leading and trailing whitespace

        # Add spacing for empty lines
        if not clean_line:
            story.append(Spacer(1, 5))
            continue

        # Replace Markdown separator lines with vertical spacing
        if clean_line in {"---", "***", "___"}:
            story.append(Spacer(1, 10))
            continue

        heading_candidate = clean_line.lstrip("#").strip()      # Removes Markdown heading symbols if present
        normalized_heading = heading_candidate.lower()          # Converts the heading to lowercase for comparison

        # Remove numbering such as "1. Executive Summary"
        if ". " in normalized_heading:

            first_part, remaining_text = normalized_heading.split(". ", 1)

            if first_part.isdigit():
                normalized_heading = remaining_text

        normalized_heading = normalized_heading.rstrip(":")     # Removes trailing colons from headings
        normalized_heading = normalized_heading.strip("*")      # Removes surrounding Markdown bold symbols for heading comparison

        safe_text = format_markdown_text(heading_candidate)     # Converts Markdown bold formatting and escapes special XML characters

        # Apply the heading style if the line is a section heading
        if normalized_heading in section_headings:

            heading_text = heading_candidate.strip("*").rstrip(":")   # Removes Markdown bold symbols and trailing colons from headings

            story.append(
                Paragraph(
                    escape(heading_text),
                    heading_style
                )
            )

        # Otherwise apply the normal body style
        else:

            story.append(
                Paragraph(
                    safe_text,
                    body_style
                )
            )

    document.build(story)                                       # Builds the PDF document with the specified content

    pdf_bytes = buffer.getvalue()                               # Retrieves the PDF data from the in-memory binary stream
    buffer.close()                                              # Closes the in-memory binary stream to free up resources

    return pdf_bytes                                            # Returns the PDF data as bytes for downloading