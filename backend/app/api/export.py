from io import BytesIO
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from sqlalchemy import text

from app.core.database import engine

router = APIRouter(prefix="/api/v1/export", tags=["Export"])


@router.get("/pdf")
def export_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    story = [Paragraph("EDIP Executive Report", styles["Title"])]

    query = text("""
        SELECT category, region, revenue, profit, priority
        FROM vw_business_recommendations
        ORDER BY root_cause_score DESC
        LIMIT 10
    """)

    with engine.connect() as conn:
        rows = conn.execute(query).mappings().all()

    for row in rows:
        story.append(
            Paragraph(
                f"<b>{row['category']}</b> | {row['region']} | "
                f"Revenue: ${row['revenue']:.0f} | "
                f"Profit: ${row['profit']:.0f} | "
                f"Priority: {row['priority']}",
                styles["BodyText"],
            )
        )

    doc.build(story)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=EDIP_Report.pdf"},
    )