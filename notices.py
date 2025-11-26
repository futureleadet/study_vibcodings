from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from db import get_db_connection
import datetime

# APIRouter 인스턴스 생성
notices_router = APIRouter()

# 템플릿 설정 (FastAPI 메인 인스턴스에서 설정된 templates를 사용하지만, 여기서는 독립적으로 설정)
templates = Jinja2Templates(directory="templates/")

def initialize_db():
    """공지사항 테이블을 생성합니다. 서버 시작 시 main.py에서 호출됩니다."""
    conn = get_db_connection()
    if not conn:
        print("DB 연결 실패로 테이블 생성을 건너뜁니다.")
        return
    
    try:
        with conn.cursor() as cur:
            cur.execute(
                """ 
                CREATE TABLE IF NOT EXISTS notices (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
        conn.commit()
        print("공지사항 테이블이 준비되었습니다.")
    except Exception as e:
        print(f"테이블 생성 중 오류 발생: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()

def get_latest_notice():
    """가장 최근에 작성된 공지사항 하나를 반환합니다."""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title FROM notices ORDER BY created_at DESC LIMIT 1;")
            notice = cur.fetchone()
            if notice:
                return {'id': notice[0], 'title': notice[1]}
            return None
    except Exception as e:
        print(f"최신 공지사항 조회 중 오류 발생: {e}")
        return None
    finally:
        if conn:
            conn.close()


# R (Read All) - 공지사항 목록
@notices_router.get("/list")
async def notices_list(request: Request):
    conn = get_db_connection()
    notices = []
    if conn:
        try:
            with conn.cursor() as cur:
                # 최신 순으로 전체 목록 조회
                cur.execute("SELECT id, title, created_at FROM notices ORDER BY created_at DESC;")
                # 데이터를 딕셔너리 형태로 변환
                for id, title, created_at in cur.fetchall():
                    notices.append({
                        'id': id,
                        'title': title,
                        # 날짜 형식을 보기 좋게 변환
                        'created_at': created_at.strftime('%Y-%m-%d %H:%M') 
                    })
        except Exception as e:
            print(f"공지사항 목록 조회 중 오류 발생: {e}")
        finally:
            conn.close()
            
    return templates.TemplateResponse(
        "notices_list.html", 
        {'request': request, 'page_title': '공지사항 목록', 'notices': notices}
    )

# C (Create) - 폼 표시
@notices_router.get("/create")
async def notices_create_form(request: Request):
    return templates.TemplateResponse(
        "notices_create.html", 
        {'request': request, 'page_title': '공지사항 작성'}
    )

# C (Create) - 데이터 처리
@notices_router.post("/create")
async def notices_create(request: Request, title: str = Form(...), content: str = Form(...)):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=503, detail="Database connection failed")
        
    try:
        with conn.cursor() as cur:
            # SQL Injection 방지를 위해 파라미터(%s) 사용
            cur.execute(
                "INSERT INTO notices (title, content) VALUES (%s, %s);",
                (title, content)
            )
        conn.commit()
    except Exception as e:
        print(f"공지사항 생성 중 오류 발생: {e}")
        conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to create notice")
    finally:
        conn.close()
        
    # 생성 후 목록 페이지로 리다이렉트
    return RedirectResponse(url="/notices/list", status_code=303)

# R (Read One), U (Update Form) - 상세 보기 및 수정 폼
@notices_router.get("/{notice_id}")
async def notices_detail(request: Request, notice_id: int):
    conn = get_db_connection()
    notice = None
    
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, title, content, created_at FROM notices WHERE id = %s;", (str(notice_id),))
                data = cur.fetchone()
                if data:
                    notice = {
                        'id': data[0],
                        'title': data[1],
                        'content': data[2],
                        'created_at': data[3].strftime('%Y-%m-%d %H:%M')
                    }
                else:
                    raise HTTPException(status_code=404, detail="Notice not found")
        except Exception as e:
            print(f"공지사항 상세 조회 중 오류 발생: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            conn.close()
            
    return templates.TemplateResponse(
        "notices_detail.html", 
        {'request': request, 'page_title': notice['title'], 'notice': notice}
    )

# U (Update) - 데이터 처리
@notices_router.post("/{notice_id}/edit")
async def notices_update(request: Request, notice_id: int, title: str = Form(...), content: str = Form(...)):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=503, detail="Database connection failed")
        
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE notices SET title = %s, content = %s WHERE id = %s;",
                (title, content, str(notice_id))
            )
        conn.commit()
    except Exception as e:
        print(f"공지사항 수정 중 오류 발생: {e}")
        conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to update notice")
    finally:
        conn.close()
        
    # 수정 후 상세 페이지로 리다이렉트
    return RedirectResponse(url=f"/notices/{notice_id}", status_code=303)

# D (Delete) - 데이터 처리
@notices_router.post("/{notice_id}/delete")
async def notices_delete(request: Request, notice_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=503, detail="Database connection failed")
        
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM notices WHERE id = %s;", (str(notice_id),))
        conn.commit()
    except Exception as e:
        print(f"공지사항 삭제 중 오류 발생: {e}")
        conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete notice")
    finally:
        conn.close()
        
    # 삭제 후 목록 페이지로 리다이렉트
    return RedirectResponse(url="/notices/list", status_code=303)