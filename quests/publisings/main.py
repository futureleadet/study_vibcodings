import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from notices import notices_router, initialize_db, get_latest_notice

# FastAPI 애플리케이션 초기화
app = FastAPI()

# 1. DB 초기화 (테이블 생성) - 서버 시작 시 한 번 실행
initialize_db()

# 2. 정적 파일 경로 설정 및 마운트
app.mount("/vendor", StaticFiles(directory="vendor"), name="vendor")
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/img", StaticFiles(directory="img"), name="img")


# 3. Jinja2 템플릿 엔진 설정
templates = Jinja2Templates(directory=".")

# 4. 공지사항 라우터 포함
# 모든 공지사항 관련 경로는 /notices/ 로 시작합니다.
app.include_router(notices_router, prefix="/notices", tags=["Notices"])

# 5. 루트(Root) 엔드포인트 정의: main_page.html 연결
@app.get("/")
async def root(request: Request):
    # 최신 공지사항을 DB에서 가져옵니다.
    latest_notice = get_latest_notice()
    
    # templates 폴더 내의 main_page.html 파일을 렌더링합니다.
    return templates.TemplateResponse("main_page.html", {
        'request': request, 
        'page_title': '메인 페이지',
        'latest_notice': latest_notice # 최신 공지사항을 템플릿에 전달
    })

# 6. 다른 페이지들도 연결
@app.get("/{page_name}")
async def other_pages(request: Request, page_name: str):
    latest_notice = get_latest_notice()
    return templates.TemplateResponse(f"{page_name}.html", {
        'request': request,
        'latest_notice': latest_notice
    })