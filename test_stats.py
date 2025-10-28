from app import app, db, Document
import os

with app.app_context():
    total = Document.query.filter_by(user_id=1).count()
    analyzed = Document.query.filter_by(user_id=1).filter(Document.extracted_text.isnot(None)).count()
    summarized = Document.query.filter_by(user_id=1).filter(Document.summary.isnot(None)).count()
    
    print("Stats being sent to template:")
    print(f"  Total Documents: {total}")
    print(f"  Analyzed: {analyzed}")
    print(f"  Summarized: {summarized}")
    print(f"  Coverage: {(analyzed / total * 100) if total > 0 else 0}%")
    
    doc = Document.query.first()
    if doc:
        print(f"\nFirst document details:")
        print(f"  Filename: {doc.original_filename}")
        print(f"  Has text: {doc.extracted_text is not None}")
        print(f"  Has summary: {doc.summary is not None}")
        print(f"  Text length: {len(doc.extracted_text) if doc.extracted_text else 0}")
        print(f"  Summary length: {len(doc.summary) if doc.summary else 0}")
