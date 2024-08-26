from fastapi import FastAPI, UploadFile, File, Depends, HTTPException,Request
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import router as api_router
from fastapi.responses import JSONResponse,StreamingResponse
app = FastAPI(title="LLM-MapBook")

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可以修改为指定的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to LLM-MapBook API"}
    
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )