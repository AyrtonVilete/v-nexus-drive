from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import os
import json
import io
from app.api.v1.endpoints import items

app = FastAPI(title="V-Nexus Drive Bridge", version="1.0")

# Permite que seu Streamlit (localhost) envie arquivos para cá
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_to_drive(file: UploadFile = File(...), folder_id: str = Form(...)):
    try:
        cred_json_str = os.getenv("GOOGLE_CREDENTIALS_JSON")
        cred_info = json.loads(cred_json_str)
        credentials = service_account.Credentials.from_service_account_info(
            cred_info, scopes=['https://www.googleapis.com/auth/drive'] # Escopo full aqui
        )
        service = build('drive', 'v3', credentials=credentials)

        file_content = await file.read()
        file_stream = io.BytesIO(file_content)
        media = MediaIoBaseUpload(file_stream, mimetype=file.content_type, resumable=True)
        
        file_metadata = {
            'name': file.filename,
            'parents': [folder_id]
        }

        # 1. Cria o arquivo
        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        file_id = uploaded_file.get("id")

        # 2. MÁGICA: Transfere a propriedade para o seu e-mail pessoal
        # Substitua 'seu-email@gmail.com' pelo seu e-mail dos 200GB
        permission = {
            'type': 'user',
            'role': 'owner',
            'emailAddress': 'seu-email@gmail.com' # <--- COLOQUE SEU EMAIL AQUI
        }
        
        # O transferOwnership=True faz o arquivo "sair" da cota do bot e ir para a sua
        service.permissions().create(
            fileId=file_id,
            body=permission,
            transferOwnership=True,
            fields='id'
        ).execute()

        return {"status": "success", "file_id": file_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))