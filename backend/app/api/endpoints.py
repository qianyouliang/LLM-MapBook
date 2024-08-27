from fastapi import APIRouter, UploadFile, File, Form,Request
from fastapi.responses import JSONResponse,StreamingResponse
from enum import Enum
from models.text_processing import FileProcessor
from models.geocode_utils import GeocodeUtils
from models.model_back import ModelBack
from models.map import Map
from models.rag import RAG
from pydantic import BaseModel
import asyncio
import uuid
import os

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    model_type: str
    api_key: str = None
    use_rag: bool = False
    is_ragged: bool = False



@router.post("/chat/")
async def chat_with_agent(request: Request):
    data = await request.json()
    chat_request = ChatRequest(**data)

    api_key = ""
    llm = ModelBack(api_key=api_key, model_type=chat_request.model_type)
    prompt = chat_request.message

    if chat_request.use_rag and chat_request.is_ragged:
        rag = RAG(api_key=api_key, model_type=chat_request.model_type)
        query = rag.query_index(chat_request.message)
        prompt = f'辅助信息：{query}\n\n用户问题：{chat_request.message}'

    async def generate():
        response = ""
        streamer = llm.chat([{"role": "user", "content": prompt}], placeholder=None)  # 添加 placeholder 参数
        for text in streamer:
            response += text.choices[0].delta.content
            yield f"{response}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


class RAGStatus(str, Enum):
    BUILDING = "构建中"
    COMPLETED = "构建完成"

# 用于存储文件ID和RAG状态的全局字典
rag_status_dict = {}

@router.post("/upload_file/")
async def upload_file(uploaded_file: UploadFile = File(...)):
    data_dir = './data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if uploaded_file:
        file_id = str(uuid.uuid4())
        file_name = uploaded_file.filename
        save_path = os.path.join(data_dir, file_id + '_' + file_name)

        with open(save_path, "wb") as f:
            f.write(await uploaded_file.read())

        return {"status": "success", "file_id": file_id}
    else:
        raise HTTPException(status_code=400, detail="文件上传失败")


@router.post("/process_file/")
async def process_file(
    file_id: str = Form(...),
    model_type: str = Form(...),
    api_key: str = Form(None),
    geocode_type: str = Form(...),
    baidu_key: str = Form(None),
    username: str = Form(None),
    use_rag: bool = Form(False),
    is_ragged: bool = Form(False)
):
    data_dir = './data'
    file_path = None
    for file in os.listdir(data_dir):
        if file.startswith(file_id):
            file_path = os.path.join(data_dir, file)
            break

    if not file_path:
        raise HTTPException(status_code=404, detail="文件未找到")

    file_processor = FileProcessor()
    with open(file_path, "rb") as f:
        file_stream = BytesIO(f.read())
        if file_path.endswith('.pdf'):
            text_list = file_processor.extract_text_from_pdf(file_stream)
        elif file_path.endswith('.txt'):
            text_list = file_processor.extract_text_from_txt(file_stream)
        else:
            raise HTTPException(status_code=400, detail="不支持的文件类型")

    llm = ModelBack(api_key=api_key, model_type=model_type)
    geo_info_list = []
    geocode_utils = GeocodeUtils(api_type=geocode_type, baidu_key=baidu_key, user_agent=username)

    for text in text_list:
        event_list = llm.get_event_list(text)
        if event_list:
            for event in event_list:
                event_info = llm.process_event(event, language="英文")
                address = event_info.get("address")
                geocode_info = geocode_utils.geocode(address)
                if geocode_info:
                    event_info["geocode"] = geocode_info
                    geo_info_list.append(event_info)

    event_list_id = str(uuid.uuid4())

    rag_status = RAGStatus.BUILDING
    if use_rag and not is_ragged:
        rag = RAG(api_key=api_key, model_type=model_type)
        rag.build_index_from_file()
        rag_status = RAGStatus.COMPLETED
        rag_status_dict[file_id] = rag_status

    return {"status": "success", "event_list_id": event_list_id, "rag_status": rag_status}

@router.get("/check_rag_status/{file_id}")
async def check_rag_status(file_id: str):
    rag_status = rag_status_dict.get(file_id, RAGStatus.BUILDING)
    return {"rag_status": rag_status}