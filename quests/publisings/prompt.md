## 프롬프트

해당 폴더에 있는 html를 main_page.html을 중심으로 fastapi로 연결하고 싶어. launch.json 파일은 폴더에 넣어놓았고. main.py파일은 아래를 참조해서 작성해줘. 모든 메뉴의 링크도 누르면 오류없이 연결해줘.
```
{
  "description": "FastAPI를 사용하여 main_page.html을 중심으로 서비스 구축 및 정적 파일 연결",
  "files": [
    {
      "filepath": "main.py",
      "content": "import os\nfrom fastapi import FastAPI, Request\nfrom fastapi.staticfiles import StaticFiles\nfrom fastapi.templating import Jinja2Templates\n\n# FastAPI 애플리케이션 초기화\napp = FastAPI()\n\n# 1. 정적 파일 경로 설정\nstatic_css_directory = os.path.join(\"resources\", \"css\")\nstatic_images_directory = os.path.join(\"resources\", \"images\")\n\n# 2. 정적 파일 마운트 (URL 경로와 물리적 경로 연결)\n# /css 로 시작하는 요청은 'resources/css' 폴더에서 파일을 찾습니다.\napp.mount(\"/css\", StaticFiles(directory=static_css_directory), name=\"static_css\")\n# /images 로 시작하는 요청은 'resources/images' 폴더에서 파일을 찾습니다.\napp.mount(\"/images\", StaticFiles(directory=static_images_directory), name=\"static_images\")\n\n# 3. Jinja2 템플릿 엔진 설정\n# HTML 파일이 있는 폴더 위치\ntemplates = Jinja2Templates(directory=\"templates/\")\n\n# 4. 루트(Root) 엔드포인트 정의: main_page.html 연결\n@app.get(\"/\")\nasync def root(request: Request):\n    # templates 폴더 내의 main_page.html 파일을 렌더링합니다.\n    return templates.TemplateResponse(\"main_page.html\", {'request': request, 'page_title': '메인 페이지'})\n\n# 5. 추가 메뉴 엔드포인트 정의 (오류 없이 연결)\n@app.get(\"/about\")\nasync def about(request: Request):\n    # about.html이 없으므로, 일단 main_page.html을 재활용하고 제목만 변경합니다.\n    # 실제 프로젝트에서는 about.html을 생성해야 합니다.\n    return templates.TemplateResponse(\"main_page.html\", {'request': request, 'page_title': '소개 페이지'})\n\n@app.get(\"/contact\")\nasync def contact(request: Request):\n    return templates.TemplateResponse(\"main_page.html\", {'request': request, 'page_title': '문의 페이지'})\n\n# 참고: 이 서비스는 templates/main_page.html이 존재해야 정상 작동합니다."
    },
    {
      "filepath": "templates/main_page.html",
      "content": "<!DOCTYPE html>\n<html lang=\"ko\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>FastAPI - {{ page_title }}</title>\n    <!-- 정적 CSS 파일 로드 -->\n    <link rel=\"stylesheet\" href=\"/css/style.css\">\n    <script src=\"https://cdn.tailwindcss.com\"></script>\n</head>\n<body class=\"font-sans\">\n    <header class=\"bg-indigo-600 text-white p-4 shadow-lg\">\n        <nav class=\"max-w-4xl mx-auto flex justify-between items-center\">\n            <a href=\"/\" class=\"text-2xl font-bold\">My FastAPI App</a>\n            <div class=\"space-x-4\">\n                <a href=\"/\" class=\"hover:text-indigo-200 transition duration-150\">홈</a>\n                <a href=\"/about\" class=\"hover:text-indigo-200 transition duration-150\">소개</a>\n                <a href=\"/contact\" class=\"hover:text-indigo-200 transition duration-150\">문의</a>\n            </div>\n        </nav>\n    </header>\n\n    <main class=\"max-w-4xl mx-auto p-8 bg-white shadow-xl rounded-lg mt-8\">\n        <h1 class=\"text-4xl font-extrabold text-gray-800 mb-6\">{{ page_title }}</h1>\n        <p class=\"text-lg text-gray-600 leading-relaxed mb-8\">\n            이 페이지는 <strong>main_page.html</strong> 템플릿을 사용하여 FastAPI 서버를 통해 렌더링되었습니다.\n            현재 URL 경로에 따라 동적으로 <code>{{ page_title }}</code>을(를) 표시하고 있습니다.\n            상단 메뉴 링크를 클릭하여 페이지 이동을 테스트해 보세요. 모든 링크는 <code>main.py</code>에 정의되어 오류 없이 연결됩니다.\n        </p>\n        \n        <div class=\"p-6 bg-indigo-50 rounded-lg border border-indigo-200\">\n            <h2 class=\"text-xl font-semibold text-indigo-700 mb-3\">정적 파일 확인</h2>\n            <p class=\"text-gray-700\">\n                아래 텍스트는 <code>/css/style.css</code> 파일에 정의된 클래스입니다. 스타일이 적용되었다면 정적 파일 연결이 성공한 것입니다.\n            </p>\n            <div class=\"test-box mt-4 p-4 rounded-md shadow-inner\">CSS 연결 테스트 성공</div>\n        </div>\n    </main>\n\n    <footer class=\"text-center p-4 mt-10 text-gray-500\">\n        &copy; 2024 FastAPI Service by Jisu\n    </footer>\n</body>\n</html>"
    },
    {
      "filepath": "resources/css/style.css",
      "content": "/* resources/css/style.css 파일 내용 */\n\n/* Tailwind CSS의 기본 설정을 보완하는 사용자 정의 스타일 */\n\n.font-sans {\n    font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, \"Helvetica Neue\", Arial, \"Noto Sans\", sans-serif, \"Apple Color Emoji\", \"Segoe UI Emoji\", \"Segoe UI Symbol\", \"Noto Color Emoji\";\n}\n\n.test-box {\n    background-color: #e0f2f1; /* Teal 50 */\n    color: #0f766e; /* Teal 700 */\n    border: 1px solid #14b8a6; /* Teal 500 */\n    font-weight: 600;\n    text-align: center;\n    transition: transform 0.3s ease;\n}\n\n.test-box:hover {\n    transform: translateY(-2px);\n    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);\n}\n"
    },
    {
      "filepath": "resources/images/.gitkeep",
      "content": "# 이미지 폴더 유지를 위한 빈 파일"
    }
  ]
}
```