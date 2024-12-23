from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader


def generate_pdf(project):
    """
    Generate a PDF file for the given project.
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    text_style = styles["Normal"]

    # Initial y-coordinate for content
    y = 750

    def add_header(canvas, project_title, y_position=800):
        """
        Add a header to the current page.
        """
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(80, y_position, f"Project Report: {project_title}")
        canvas.line(80, y_position - 5, 530, y_position - 5)
        canvas.setFont("Helvetica", 12)

    ################################
    # Add project details to the PDF
    ################################
    add_header(p, project.title)
    y -= 40

    # Project Title
    p.setFont("Helvetica-Bold", 12)
    p.drawString(80, y, "Project Title:")
    p.setFont("Helvetica", 12)
    p.drawString(180, y, project.title)
    y -= 20

    # Project Description
    p.setFont("Helvetica-Bold", 12)
    p.drawString(80, y, "Description:")
    p.setFont("Helvetica", 12)
    y -= 15
    description = Paragraph(project.description, text_style)
    max_width = 400
    _, height = description.wrap(max_width, y - 50)
    if height > y - 50:  # Check if it fits the current page
        p.showPage()  # Add a new page if needed
        add_header(p, project.title)
        y = 750
    description.drawOn(p, 90, y - height)
    y -= height + 20

    # Project Priority
    p.setFont("Helvetica-Bold", 12)
    p.drawString(80, y, "Priority:")
    p.setFont("Helvetica", 12)
    p.drawString(180, y, project.priority)
    y -= 20

    # Project Status
    p.setFont("Helvetica-Bold", 12)
    p.drawString(80, y, "Status:")
    p.setFont("Helvetica", 12)
    p.drawString(180, y, project.status)
    y -= 40

    ################################
    # Add images to the PDF
    ################################
    for image in project.images.all():
        try:
            # Check if there is enough space for the image;
            # add a new page if needed
            if y < 200:
                p.showPage()
                add_header(p, project.title)
                y = 750

            # Load the image
            image_path = image.image.path
            img = ImageReader(image_path)

            # Draw the image
            p.drawImage(img, 80, y - 150, width=200, height=150)

            # Add a caption or label for the image
            p.setFont("Helvetica-Bold", 10)
            p.drawString(80, y - 170, image.image.name.split('/')[-1])

            # Update y-coordinate for the next image
            y -= 200
        except Exception as e:
            # Handle any image loading errors
            if y < 50:
                p.showPage()
                add_header(p, project.title)
                y = 750
            p.setFont("Helvetica", 10)
            p.drawString(80, y, f"Error loading image: {e}")
            y -= 20

    ################################
    # Finalize and save the PDF
    ################################
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
