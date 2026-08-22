from pathlib import Path

parts = [
  '01-overview-and-context.md',
  '02-mathematical-approach.md',
  '03-ai-ml-mathematical-extensions.md',
  '04-test-beds.md',
  '05-other-applications.md',
  '06-example-applications.md',
  '07-crop-motivation-and-software-plan.md',
  '08-roadmap-and-licensing.md',
  '09-hybrid-and-translational-reading.md',
  '10-clinical-operations-and-treatment-delivery-reading.md',
  '11-engineering-environmental-and-biological-applications-reading.md',
  '12-labs-and-modeling-limits-reading.md'
]


source_dir = Path("docs/readme-parts")
content = "\n\n".join(
    (source_dir / part).read_text(encoding="utf-8").rstrip()
    for part in parts
)

Path("README.md").write_text(content + "\n", encoding="utf-8")
