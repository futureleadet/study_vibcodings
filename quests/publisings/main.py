import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Get the directory of the current file (main.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 정적 파일 마운트 (css, js, img, vendor 등)
app.mount("/css", StaticFiles(directory=os.path.join(BASE_DIR, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(BASE_DIR, "js")), name="js")
app.mount("/vendor", StaticFiles(directory=os.path.join(BASE_DIR, "vendor")), name="vendor")
app.mount("/img", StaticFiles(directory=os.path.join(BASE_DIR, "img")), name="img")
app.mount("/scss", StaticFiles(directory=os.path.join(BASE_DIR, "scss")), name="scss")

# Jinja2 템플릿 설정
templates = Jinja2Templates(directory=BASE_DIR)

# HTML 파일 목록
html_files = [
    "404.html",
    "blank.html",
    "buttons.html",
    "cards.html",
    "charts.html",
    "detail_page.html",
    "event_info.html",
    "feed.html",
    "forgot-password.html",
    "index.html",
    "login.html",
    "main_page.html",
    "member_management.html",
    "performance_info.html",
    "popup_info.html",
    "post_management.html",
    "quest_management.html",
    "register.html",
    "restaurant_info.html",
    "settings.html",
    "tables.html",
    "user_submission_review.html",
    "utilities-animation.html",
    "utilities-border.html",
    "utilities-color.html",
    "utilities-other.html",
]

# 루트 경로 (main_page.html)
@app.get("/", response_class=HTMLResponse)
async def read_main(request: Request):
    return templates.TemplateResponse("main_page.html", {"request": request})

# 각 HTML 파일에 대한 동적 라우트 생성
for html_file in html_files:
    # index.html은 /index 경로로 별도 처리
    if html_file == "index.html":
        path = "/index"
    else:
        path = "/" + html_file.replace(".html", "")

    # https://fastapi.tiangolo.com/advanced/advanced-routing/#path-operations-with-the-same-path
    # The first one declared will be used.
    # We need to create a closure to capture the html_file variable
    def create_route_function(file_name):
        async def route_function(request: Request):
            return templates.TemplateResponse(file_name, {"request": request})
        return route_function

    app.add_api_route(path, create_route_function(html_file), methods=["GET"], response_class=HTMLResponse)
