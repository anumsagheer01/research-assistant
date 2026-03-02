from utils.s3_handler import save_report_to_s3

sample_report = """# AI in Healthcare

## Executive Summary
AI is transforming healthcare in significant ways.

## Key Findings
- AI improves diagnostic accuracy
- Reduces costs by 30%
- Speeds up drug discovery

## Conclusion
AI will continue to reshape healthcare delivery.
"""

url = save_report_to_s3(sample_report, "AI in Healthcare")
if url:
    print("\n⬇️ Download URL:")
    print(url)
else:
    print("S3 upload failed")