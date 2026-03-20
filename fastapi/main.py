from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import router
import asyncio
from fastapi.middleware.cors import CORSMiddleware


# 输出欢迎页面
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时打印欢迎信息
    print("╔══════════════════════════════════════════════════════╗")
    print("║                                                      ║")
    print("║               欢迎使用  二手房交易系统                   ║")
    print("║                                                      ║")
    print("║           🚀 服务器启动成功！                           ║")
    print("║           📊 数据库: mySQL                            ║")
    print("║           🌐 访问地址: http://localhost:8000          ║")
    print("║           📚 API文档: http://localhost:8000/docs      ║")
    print("║                                                      ║")
    print("╚══════════════════════════════════════════════════════╝")

    await asyncio.sleep(0.1)

    yield

    # 关闭时打印再见信息
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║                                                        ║")
    print("║             API 服务器已关闭                             ║")
    print("║                再见！👋                                ║")
    print("║                                                       ║")
    print("╚══════════════════════════════════════════════════════╝")


app = FastAPI(
    title="API",
    description="管理API",
    version="1.0.0",
    lifespan=lifespan
)

# 允许跨域
origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to admin API",
        "docs": "/docs",
        "database": "mySQL"
    }


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "admin API",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)