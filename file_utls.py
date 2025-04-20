import os
from datetime import datetime
from markdown_pdf import MarkdownPdf, Section

def create_output_file_name(goal: str | None = None) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    goal_slug = goal.replace(" ", "_").lower() if goal else "general"
    return f"{timestamp}_{goal_slug}.pdf"

def create_summary_output_file(output_dir: str = "summaries", goal: str | None = None) -> str:
    """Create a unique output file name for the summary
    :param output_dir: output directory
    :param goal: focus of the summary
    :return: the output file path
    """
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, create_output_file_name(goal))

    return output_file

def create_pdf(summary: str, title: str, output_file: str) -> None:
    pdf = MarkdownPdf(optimize=True)
    pdf.add_section(Section(summary))
    pdf.meta["title"] = title
    pdf.meta["author"] = "unscroll - Instagram Scraper - giuliopime.dev"

    pdf.save(output_file)
