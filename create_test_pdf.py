#!/usr/bin/env python3
"""
Create a test A3 PDF file for testing the splitter
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3
from reportlab.lib import colors
from reportlab.lib.units import cm

def create_test_a3_pdf(filename="test_a3.pdf"):
    """Create a test A3 PDF with numbered pages"""
    c = canvas.Canvas(filename, pagesize=A3)
    width, height = A3

    # Create 3 A3 pages for testing
    for page_num in range(1, 4):
        # Draw page border
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.rect(10, 10, width - 20, height - 20)

        # Draw vertical center line to show where split will occur
        mid_x = width / 2
        c.setStrokeColor(colors.red)
        c.setLineWidth(1)
        c.setDash(3, 3)
        c.line(mid_x, 10, mid_x, height - 10)
        c.setDash()  # Reset dash

        # Left side content (will become page 1)
        c.setFont("Helvetica-Bold", 36)
        c.setFillColor(colors.blue)
        c.drawString(width / 4 - 100, height / 2 + 50, f"A3 Page {page_num}")
        c.setFont("Helvetica", 24)
        c.drawString(width / 4 - 100, height / 2, "LEFT SIDE")
        c.drawString(width / 4 - 100, height / 2 - 50, f"(Will be A4 Page {page_num * 2 - 1})")

        # Right side content (will become page 2)
        c.setFillColor(colors.green)
        c.setFont("Helvetica-Bold", 36)
        c.drawString(3 * width / 4 - 100, height / 2 + 50, f"A3 Page {page_num}")
        c.setFont("Helvetica", 24)
        c.drawString(3 * width / 4 - 100, height / 2, "RIGHT SIDE")
        c.drawString(3 * width / 4 - 100, height / 2 - 50, f"(Will be A4 Page {page_num * 2})")

        # Add some markers in corners
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 12)
        # Top left
        c.drawString(20, height - 30, "TL")
        # Top right
        c.drawString(width - 40, height - 30, "TR")
        # Bottom left
        c.drawString(20, 20, "BL")
        # Bottom right
        c.drawString(width - 40, 20, "BR")

        c.showPage()

    c.save()
    print(f"Created test A3 PDF: {filename}")
    return filename

if __name__ == "__main__":
    create_test_a3_pdf()