"""
Endpoints para integração com Google Drive
"""
from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import os
import json
import io

router = APIRouter(prefix="/drive", tags=["drive"])


@router.post("/upload")
async def upload_to_drive(file: UploadFile = File(...), folder_id: str = Form(...)):
    """
    Faz upload de um arquivo para o Google Drive
    
    - **file**: Arquivo a ser enviado
    - **folder_id**: ID da pasta no Google Drive
    """
    try:
        # 1. Recupera o JSON do Bot da variável de ambiente
        cred_json_str = os.getenv("GOOGLE_CREDENTIALS_JSON")
        if not cred_json_str:
            raise HTTPException(
                status_code=500,
                detail="Variável GOOGLE_CREDENTIALS_JSON não configurada."
            )

        # 2. Autentica o Service Account
        cred_info = json.loads(cred_json_str)
        credentials = service_account.Credentials.from_service_account_info(
            cred_info,
            scopes=['https://www.googleapis.com/auth/drive.file']
        )

        # 3. Inicializa o serviço do Drive
        service = build('drive', 'v3', credentials=credentials)

        # 4. Lê o arquivo enviado
        file_content = await file.read()
        file_stream = io.BytesIO(file_content)

        # 5. Configura o upload
        media = MediaIoBaseUpload(
            file_stream,
            mimetype=file.content_type,
            resumable=True
        )
        file_metadata = {
            'name': file.filename,
            'parents': [folder_id]
        }

        # 6. Executa a criação no Drive
        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        return {
            "status": "success",
            "file_id": uploaded_file.get("id"),
            "message": f"Arquivo '{file.filename}' enviado com sucesso!"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
