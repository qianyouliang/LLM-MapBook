from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from io import BytesIO
import json
from utils.geocode_utils import GeocodeUtils
from utils.text_processing import FileProcessor

app = FastAPI()
geocode_utils = GeocodeUtils()
file_processor = FileProcessor()

def create_geojson(geo_info_list):
    features = []
    for info in geo_info_list:
        geocode_result = geocode_utils.geocode(info["address"])
        if 'error' not in geocode_result:
            feature = {
                "type": "Feature",
                "properties": {
                    "description": info["description"]
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [geocode_result["longitude"], geocode_result["latitude"]]
                }
            }
            features.append(feature)
    return {
        "type": "FeatureCollection",
        "features": features
    }

class FileUpload(BaseModel):
    file: UploadFile

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_content = await file.read()
    file_stream = BytesIO(file_content)
    
    if file.filename.endswith('.pdf'):
        text = file_processor.extract_text_from_pdf(file_stream)
    elif file.filename.endswith('.txt'):
        text = file_processor.extract_text_from_txt(file_stream)
    else:
        return JSONResponse(content={"error": "Unsupported file type"}, status_code=400)
    
    # 使用 call_llm_model 函数处理文本并获取地理信息列表
    geo_info_list = file_processor.process_text(text)
    geojson = create_geojson(geo_info_list)
    
    return JSONResponse(content=geojson)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)