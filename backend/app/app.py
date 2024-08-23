from fastapi import FastAPI, UploadFile, File, Form
from utils.geocode_utils import GeocodeUtils
from utils.text_processing import FileProcessor
from utils.model_back import LLM
from utils.map import Map
from io import BytesIO
from typing import List

app = FastAPI()

@app.post("/upload-file/")
async def upload_and_process_file(
    uploaded_file: UploadFile = File(...),
    api_key: str = Form(...),
    geocode_type: str = Form(...),
    baidu_key: str = Form(None),
    username: str = Form(None)
):
    file_processor = FileProcessor()
    file_content = await uploaded_file.read()
    file_stream = BytesIO(file_content)
    
    if uploaded_file.filename.endswith('.pdf'):
        text_list = file_processor.extract_text_from_pdf(file_stream)
    elif uploaded_file.filename.endswith('.txt'):
        text_list = file_processor.extract_text_from_txt(file_stream)
    else:
        return {"error": "不支持的文件类型"}
    
    geo_info_list = []
    geocode_utils = GeocodeUtils(api_type=geocode_type, baidu_key=baidu_key, user_agent=username)
    llm = LLM(api_key=api_key)
    
    for text in text_list:
        event_list = llm.get_event_list(text)
        if event_list:
            for i, event in enumerate(event_list):
                try:
                    event_info = llm.process_event(event, language="英文")
                    address = event_info["address"]
                    geocode_info = geocode_utils.geocode(address)
                    if geocode_info["longitude"]:
                        event_info["geocode"] = geocode_info
                        geo_info_list.append(event_info)
                except Exception as e:
                    continue
    
    return {"geo_info_list": geo_info_list}

@app.get("/map/")
async def get_map():
    m = Map()
    m.init_map(selected_tile="OpenStreetMap")
    m.add_polyline()
    map_data = m.display()
    return map_data

@app.post("/export/")
async def export_data(format: str = Form(...)):
    m = Map()
    if format == "geojson":
        return {"data": m.export_geojson()}
    elif format == "shp":
        return {"data": m.export_shp()}
    return {"error": "不支持的导出格式"}
