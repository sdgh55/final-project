from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.responses import FileResponse

api = FastAPI()

photo_path = "C:\\Users\\zkauk\\Downloads\\example4.jpeg"


@api.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

@api.get("/download-photo/")
async def download_photo():
    try:
        # Используйте FileResponse для отправки файла в ответе
        return FileResponse(photo_path, media_type="image/jpeg", filename="downloaded_photo.jpg")
    except Exception as e:
        # Если произошла ошибка, верните 404 Not Found
        raise HTTPException(status_code=404, detail="Photo not found")
