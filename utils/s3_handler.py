import boto3
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def generate_pdf(report_text: str, topic: str) -> bytes:
    """Convert report text to PDF bytes."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                           rightMargin=inch, leftMargin=inch,
                           topMargin=inch, bottomMargin=inch)
    
    styles = getSampleStyleSheet()
    story = []

    for line in report_text.split('\n'):
        if line.startswith('# '):
            story.append(Paragraph(line[2:], styles['Title']))
        elif line.startswith('## '):
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph(line[3:], styles['Heading2']))
        elif line.strip() == '':
            story.append(Spacer(1, 0.1*inch))
        else:
            story.append(Paragraph(line, styles['Normal']))

    doc.build(story)
    return buffer.getvalue()

def save_report_to_s3(report_text: str, topic: str) -> str:
    """
    Saves report as PDF to S3 and returns a presigned download URL.
    """
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION")
        )

        # Generate PDF
        pdf_bytes = generate_pdf(report_text, topic)

        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        clean_topic = topic[:50].replace(" ", "_").replace("/", "_")
        filename = f"reports/{clean_topic}_{timestamp}.pdf"

        # Upload to S3
        bucket_name = os.getenv("AWS_BUCKET_NAME")
        s3_client.put_object(
            Bucket=bucket_name,
            Key=filename,
            Body=pdf_bytes,
            ContentType='application/pdf'
        )

        # Generate presigned URL (valid for 1 hour)
        download_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': filename},
            ExpiresIn=3600
        )

        print(f"Report saved to S3: {filename}")
        return download_url

    except Exception as e:
        print(f"S3 upload failed: {e}")
        return None