from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
import base64
import io
from textwrap import wrap


def generate_pdf_report(report_data):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50

    def check_page_space(required_space=80):
        nonlocal y
        if y < required_space:
            pdf.showPage()
            y = height - 50

    def draw_title(title, size=14):
        nonlocal y
        check_page_space(40)
        pdf.setFont("Helvetica-Bold", size)
        pdf.drawString(40, y, title)
        y -= 24

    def draw_bold_subtitle(text, size=12):
        nonlocal y
        check_page_space(30)
        pdf.setFont("Helvetica-Bold", size)
        pdf.drawString(40, y, text)
        y -= 18

    def draw_paragraph(text, font="Helvetica", size=10, leading=14, wrap_width=95):
        nonlocal y
        check_page_space()
        pdf.setFont(font, size)
        for paragraph in text.split("\n\n"):
            lines = wrap(paragraph.strip(), width=wrap_width)
            for line in lines:
                if y < 60:
                    pdf.showPage()
                    y = height - 50
                    pdf.setFont(font, size)
                pdf.drawString(40, y, line)
                y -= leading
            y -= 8  # space between paragraphs

    # === Report Content ===
    draw_title(f"{report_data['company']} ({report_data['ticker']}) Investment Report")

    # Market Data
    draw_bold_subtitle("Market Data")
    market = report_data.get("marketData", {})
    draw_paragraph(f"""
    Current Price: ${market.get('currentPrice', 'N/A')}
    Market Cap: {market.get('marketCap', 'N/A')}
    P/E Ratio: {market.get('trailingPE', 'N/A')}
    52-Week High: {market.get('fiftyTwoWeekHigh', 'N/A')}
    52-Week Low: {market.get('fiftyTwoWeekLow', 'N/A')}
    Sector: {market.get('sector', 'N/A')}
    """)

    # Price Forecast Chart
    chart_data = report_data.get("priceChart")
    if chart_data:
        try:
            draw_bold_subtitle("Price Forecast")
            chart_image = ImageReader(io.BytesIO(base64.b64decode(chart_data)))
            pdf.drawImage(chart_image, 40, y - 200, width=5.5 * inch, height=2.5 * inch, preserveAspectRatio=True)
            y -= 220
        except Exception as e:
            draw_paragraph(f"[Chart failed to render: {e}]")

    # News Summary
    news_summary = report_data.get("news", {}).get("summary", "")
    if news_summary:
        draw_bold_subtitle("News Summary")
        draw_paragraph(news_summary)

    # SWOT Analysis
    swot_text = report_data.get("swot", "")
    if swot_text:
        draw_bold_subtitle("SWOT & Investment Summary")
        for line in swot_text.split("\n"):
            stripped = line.strip()
            if stripped.startswith("### "):
                draw_bold_subtitle(stripped[4:], size=11)
            elif stripped.startswith("## "):
                draw_bold_subtitle(stripped[3:], size=12)
            elif stripped.startswith("# "):
                draw_bold_subtitle(stripped[2:], size=13)
            else:
                draw_paragraph(stripped)

    # AI Recommendation
    recommendation = report_data.get("recommendation", "")
    if recommendation:
        draw_bold_subtitle("AI Recommendation")
        draw_paragraph(recommendation)

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer.read()
