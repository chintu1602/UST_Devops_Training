from fastapi import APIRouter, Depends,UploadFile,File,HTTPException,Query,status,Request,Form
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
import os
import mimetypes

from App.database import get_db
from App.dependency import get_current_user
from App.schemas.documents import DocumentCreate,DocumentResponse,DocumentVersionResponse,DocumentUpdate
from App.models.Documents import Document
from App.models.Versions import DocumentVersion
from App.models.User import User
from App.utils.filehandler import save_file


router = APIRouter(prefix="/documents", tags=["Documents"])
templates = Jinja2Templates(directory="App/templates")

# Getting index page
@router.get("/")
def documents_page(
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    username = db.query(User).filter(User.id == user_id).first().Username
    return templates.TemplateResponse("index.html", {"request": request, "username": username})

# Creating a Document 
@router.post("/add")
def create_document(
    title: str = Form(...),
    description: str = Form(...),
    tag:str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    if db.query(Document).filter(
        Document.title == title,
        Document.description == description,
        Document.owner_id == user_id
    ).first():
        raise HTTPException(status_code=400, detail="Document already exists with this title.")
    
    # Save file
    file_path,file_name = save_file(file)

    # Create document
    document = Document(
        title=title,
        description=description,
        tag=tag,
        owner_id=user_id
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    # 3 Create version 1
    version = DocumentVersion(
        document_id=document.id,
        version=1,
        file_path=file_path,
        original_filename=file_name
    )
    db.add(version)
    db.commit()

    return {"message": "Document uploaded successfully."}

#uploading newer version of existing document..
@router.post("/{document_id}/versions")
def upload_new_version(
    document_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.owner_id == user_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    last_version = (
        db.query(DocumentVersion)
        .filter(DocumentVersion.document_id == document_id)
        .order_by(DocumentVersion.version.desc())
        .first()
    )

    new_version_number = last_version.version + 1

    file_path,file_name = save_file(file)

    new_version = DocumentVersion(
        document_id=document_id,
        version=new_version_number,
        file_path=file_path,
        original_filename=file_name
    )
    db.add(new_version)
    db.commit()

    return {"message": "New version uploaded successfully."}

#Tag based searching ...
@router.get("/tag_search",response_model=list[DocumentResponse])
def list_doc_viatag(tag:str= Query(...),db:Session=Depends(get_db),user_id:int=Depends(get_current_user)):
   if not tag:
        return []   #THIS LINE FIXES YOUR BUG

   documents = (
        db.query(Document)
        .filter(
            Document.owner_id == user_id,
            Document.tag.isnot(None),
            Document.tag.ilike(f"%{tag}%")
        )
        .order_by(Document.created_at.desc())
        .all()
    )
   return documents


#Getting all the documents..
@router.get("/list_all", response_model=list[DocumentResponse])
def list_my_documents(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    documents = db.query(Document).filter(Document.owner_id == user_id).order_by(Document.created_at.desc()).all()
    
    return documents


 #Getting all the verions of a document 
@router.get("/{document_id}/versions", response_model=list[DocumentVersionResponse])
def list_document_versions(
    document_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    # 1️ Check ownership
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.owner_id == user_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    #2 Get versions
    versions = (
        db.query(DocumentVersion)
        .filter(DocumentVersion.document_id == document_id)
        .order_by(DocumentVersion.version.desc())
        .all()
    )

    return versions


#Downloading a particular document
@router.get("/{document_id}/versions/{version_id}/download")
def download_version(
    document_id: int,
    version_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    # Ownership check
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.owner_id == user_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Get version
    version = db.query(DocumentVersion).filter(
        DocumentVersion.id == version_id,
        DocumentVersion.document_id == document_id
    ).first()

    if not version:
        raise HTTPException(status_code=404, detail="Version not found")

    # File existence check
    if not os.path.exists(version.file_path):
        raise HTTPException(status_code=404, detail="File missing on server")

    # Secure download
    return FileResponse(
        path=version.file_path,
        filename=version.original_filename,
        media_type="application/octet-stream"
    )

#Previewing a particular document version
@router.get("/{document_id}/versions/{version_id}/preview")
def preview_version(
    document_id: int,
    version_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    # Ownership check
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.owner_id == user_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Get version
    version = db.query(DocumentVersion).filter(
        DocumentVersion.id == version_id,
        DocumentVersion.document_id == document_id
    ).first()

    if not version:
        raise HTTPException(status_code=404, detail="Version not found")

    # File existence check
    if not os.path.exists(version.file_path):
        raise HTTPException(status_code=404, detail="File missing on server")

    # Detect correct media type
    media_type, _ = mimetypes.guess_type(version.file_path)
    if media_type is None:
        media_type = "application/octet-stream"

    # Inline preview
    return FileResponse(
        path=version.file_path,
        media_type=media_type,
        headers={
            "Content-Disposition": f'inline; filename="{version.original_filename}"'
        }
    )


#Updating a document
@router.patch("/update/{document_id}")
def update_document(
    document_id: int,
    data: DocumentUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.owner_id == user_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if db.query(Document).filter(
        Document.title == data.title,
        Document.description == data.description,
        Document.id != document_id,
        Document.owner_id == user_id,
    ).first():
        raise HTTPException(status_code=400, detail="Document already exists with this title and description.")

    if data.title is not None:
        document.title = data.title
    if data.description is not None:
        document.description = data.description
    if data.tag is not None:
        document.tag = data.tag

    db.commit()
    return {"message": "Document updated successfully."}


#Deleting a document..
@router.delete("/delete/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.owner_id == user_id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # 1️ Delete files from disk
    for version in document.versions:
        if os.path.exists(version.file_path):
            os.remove(version.file_path)

    # 2 Delete document
    db.delete(document)
    db.commit()

    return {"message": "Document deleted successfully."}