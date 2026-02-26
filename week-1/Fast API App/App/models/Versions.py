from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from App.database import Base

class DocumentVersion(Base):
    __tablename__ = "document_versions"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    version = Column(Integer)
    file_path = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    original_filename = Column(String(255), nullable=False)

    document = relationship("Document", back_populates="versions")
