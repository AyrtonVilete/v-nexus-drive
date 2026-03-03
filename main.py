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
        # 1. Recupera o JSON do Bot da variável de ambiente do Render
        cred_json_str = os.getenv("GOOGLE_CREDENTIALS_JSON")
        if not cred_json_str:
            raise HTTPException(status_code=500, detail="Variável GOOGLE_CREDENTIALS_JSON não configurada.")

        # 2. Autentica o Service Account
        cred_info = json.loads(cred_json_str)
        credentials = service_account.Credentials.from_service_account_info(
            cred_info, scopes=['https://www.googleapis.com/auth/drive.file']
        )

        # 3. Inicializa o serviço do Drive
        service = build('drive', 'v3', credentials=credentials)

        # 4. Lê o arquivo enviado pelo Streamlit
        file_content = await file.read()
        file_stream = io.BytesIO(file_content)

        # 5. Configura o upload
        media = MediaIoBaseUpload(file_stream, mimetype=file.content_type, resumable=True)
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

        return {"status": "success", "file_id": uploaded_file.get("id")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "Drive Bridge is Online! 🚀", "message": "Bem-vindo à API V-Nexus Drive Bridge"}


@app.get("/health")
def health_check_simple():
    return {"status": "healthy"}


# Registrar routers
app.include_router(items.router, prefix="/api/v1")