from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from io import BytesIO
import os
import json
from utils.geocode_utils import GeocodeUtils
from utils.text_processing import FileProcessor
from utils.model_back import ModelBack
from utils.map import Map
from utils.rag import RAG

app = FastAPI()

# Initialize session-like storage
session_state = {
    "username": "GISerLiu",
    "api_key": "",
    "baidu_key": "",
    "geocode_type": "free",
    "uploaded_file": None,
    "file_changed": False,
    "processed": False,
    "geo_info_list": [],
    "selected_info": None,
    "model_type": "deepseek",
    "isRAG": False,
    "isSmartMap": False,
    "RAGed": False,
}

# Model to represent the upload and processing information
class ProcessedInfo(BaseModel):
    message: str
    success: bool
    geo_info_list: list = []

@app.post("/upload/")
async def upload_and_process_file(
    file: UploadFile = File(...),
    isRAG: bool = Form(False),
    geocode_type: str = Form("free"),
    model_type: str = Form("deepseek"),
    api_key: str = Form(""),
    baidu_key: str = Form(""),
    username: str = Form("GISerLiu"),
):
    # Ensure the data directory exists
    data_dir = './data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    session_state["geocode_type"] = geocode_type
    session_state["api_key"] = api_key
    session_state["baidu_key"] = baidu_key
    session_state["username"] = username
    session_state["model_type"] = model_type
    session_state["isRAG"] = isRAG

    # File upload handling
    file_name = file.filename
    file_content = await file.read()
    save_path = os.path.join(data_dir, file_name)
    
    with open(save_path, "wb") as f:
        f.write(file_content)
    
    session_state["uploaded_file"] = file_name
    session_state["file_changed"] = True
    session_state["processed"] = False
    session_state["geo_info_list"] = []

    llm = ModelBack(api_key=session_state["api_key"], model_type=session_state["model_type"])
    rag = RAG(api_key=session_state["api_key"], model_type=session_state["model_type"])

    # RAG indexing
    if session_state["isRAG"] and not session_state["RAGed"]:
        rag.build_index_from_file()
        session_state["RAGed"] = True

    # File processing
    file_processor = FileProcessor()
    file_stream = BytesIO(file_content)
    text_list = []

    if file_name.endswith('.pdf'):
        text_list = file_processor.extract_text_from_pdf(file_stream)
    elif file_name.endswith('.txt'):
        text_list = file_processor.extract_text_from_txt(file_stream)
    else:
        return JSONResponse(content={"message": "Unsupported file type"}, status_code=400)
    
    geo_info_list = []
    geocode_utils = GeocodeUtils(
        api_type=session_state["geocode_type"], 
        baidu_key=session_state["baidu_key"], 
        user_agent=session_state["username"]
    )
    
    processed_event_ids = []
    for text in text_list:
        event_list = llm.get_event_list(text)
        if event_list:
            for i, event in enumerate(event_list):
                event_id = i  # Assuming event object has a unique ID
                if event_id is None:
                    continue

                if event_id not in processed_event_ids:
                    event_info = llm.process_event(event, language="英文")
                    address = event_info["address"]
                    geocode_info = geocode_utils.geocode(address)
                    
                    if geocode_info:
                        event_info["geocode"] = geocode_info
                        processed_event_ids.append(event_id)
                        geo_info_list.append(event_info)
                    else:
                        continue

    session_state["geo_info_list"] = geo_info_list
    session_state["processed"] = True

    return ProcessedInfo(
        message=f"File processed and saved at {save_path}",
        success=True,
        geo_info_list=geo_info_list
    )

@app.get("/map/")
async def get_map():
    m = Map()
    if len(session_state["geo_info_list"]) > 0:
        for info in session_state["geo_info_list"]:
            geo_info = info["geocode"]
            m.add_marker(info, geo_info)
    
    geojson_data = m.export_geojson()
    return JSONResponse(content=json.loads(geojson_data))

@app.post("/chat/")
async def chat(prompt: str):
    llm = ModelBack(api_key=session_state["api_key"], model_type=session_state["model_type"])
    response = ""
    
    if session_state["isRAG"] and session_state["RAGed"]:
        rag = RAG(api_key=session_state["api_key"], model_type=session_state["model_type"])
        query = rag.query_index(prompt)
        prompt = f'''
            辅助信息：{query};
            ___________________
            用户问题：{prompt};
        '''

    # Simulate chat with model (simplified for demonstration)
    response = llm.chat([{"role": "user", "content": prompt}])

    return JSONResponse(content={"response": response})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
