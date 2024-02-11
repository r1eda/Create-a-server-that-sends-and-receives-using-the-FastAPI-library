from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.post('/upload')
async def upload_file(files: list[UploadFile] = File(...)):
    for file in files:
        with open(os.path.join(UPLOAD_FOLDER, file.filename), 'wb') as buffer:
            buffer.write(await file.read())
    return {'message': 'Files uploaded successfully'}

@app.get('/request')
async def request_file():
    files = os.listdir(UPLOAD_FOLDER)
    if len(files) == 0:
        raise HTTPException(status_code=404, detail='No files available')

    # For simplicity, just return the first file found
    requested_file = files[0]

    # Provide the requested file for download
    return FileResponse(os.path.join(UPLOAD_FOLDER, requested_file), filename=requested_file)

# uvicorn fastAPI:app --reload
# uvicorn fastAPI:app --reload --port 5000
# uvicorn fastAPI:app --reload --host 0.0.0.0 --port 5000
