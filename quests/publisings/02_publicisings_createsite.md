## 페이지 다시 구성

아래 내용의 페이지를 만들어줘

타이틀 : 뭐하고 놀지?
컨셉 : 공연, 팝업, 맛집 등 지역을 기반으로 한 다양한 놀이정보를 제공
메뉴 구성
- 공연정보
- 팝업정보
- 맛집정보
- 이벤트정보
- 놀이인증


페이지 구성 : 아래 링크와 동일.
- 상단 메뉴 구성
- 그 밑에 포스터 사이즈 썸네일로 놀이정보 카드형
- 그 밑에 월간일정 달력모양으로 배치

https://www.sac.or.kr/site/main/program/schedule?tab=2

기술사항
- HTML
- BS5
- JS만으로 사용


## CRUD 메뉴 프롬프트

{
  "pageTitle": "회원 피드 및 활동 기록",
  "pageDepth": "Second Depth",
  "pagePurpose": "사용자 활동 기록 및 공유 (CRUD)",
  "layout": {
    "header": {
      "component": "TopNavigation",
      "description": "기본 상단 메뉴 (로고, 알림, 프로필 등) 유지"
    },
    "body": {
      "sections": [
        {
          "id": "creationArea",
          "title": "글쓰기 입력 영역",
          "component": "PostCreationWidget",
          "description": "사용자가 새로운 활동 기록을 작성하는 영역",
          "label": "뭐하고 놀았나요?"
        },
        {
          "id": "feedContent",
          "title": "회원 활동 피드 목록",
          "component": "FeedList",
          "description": "시간순 최신순으로 회원들의 게시물이 표시되는 영역"
        }
      ]
    }
  },
  "dataModel": {
    "FeedItem": {
      "postId": "UUID/String (게시물 고유 ID)",
      "userId": "String (작성자 ID)",
      "userName": "String (작성자 닉네임)",
      "userProfileImage": "URL/String (작성자 프로필 이미지)",
      "content": "String (게시물 내용)",
      "timestamp": "Date (작성 시간)",
      "images": {
        "type": "Array<URL/String>",
        "description": "최소 1장에서 여러 장의 이미지 URL 목록"
      },
      "likesCount": "Number (좋아요 수)",
      "commentsCount": "Number (댓글 수)"
    }
  },
  "componentsDetails": {
    "PostCreationWidget": {
      "title": "뭐하고 놀았나요?",
      "features": [
        "텍스트 입력 필드",
        "이미지 첨부 버튼 (다중 선택 가능)",
        "작성(Create) 버튼 활성화/비활성화 로직"
      ],
      "crudOperation": "Create (C)"
    },
    "FeedList": {
      "itemStructure": "FeedItem",
      "interaction": "무한 스크롤 (Infinity Scroll) 또는 페이지네이션",
      "crudOperation": "Read (R)"
    },
    "FeedItem": {
      "display": {
        "image": {
          "format": "Square Aspect Ratio",
          "carousel": "다중 이미지일 경우 스와이프 가능한 캐러셀(Swipe/Slider) 구현"
        },
        "controls": {
          "ownerActions": "게시물 작성자에게만 수정(U) 및 삭제(D) 메뉴 표시",
          "userActions": "좋아요(Like), 댓글(Comment) 버튼"
        }
      },
      "crudOperation": "Update (U), Delete (D) - Post Owner only"
    }
  },
  "requiredCrudOperations": [
    {"action": "Create", "target": "FeedItem", "endpoint": "/api/posts", "method": "POST"},
    {"action": "Read", "target": "FeedList", "endpoint": "/api/posts", "method": "GET"},
    {"action": "Update", "target": "FeedItem", "endpoint": "/api/posts/{postId}", "method": "PUT"},
    {"action": "Delete", "target": "FeedItem", "endpoint": "/api/posts/{postId}", "method": "DELETE"}
  ]
}
## 관리자화면 프롬프트 ##
{
  "project_name": "futureleadet_관리자_시스템_구축",
  "template": {
    "name": "SB-Admin",
    "description": "Start Bootstrap의 SB-Admin 템플릿을 기본 레이아웃으로 사용",
    "reference_url": "https://startbootstrap.com/previews/sb-admin"
  },
  "system_type": "관리자_화면",
  "menu_structure": [
    {
      "id": "dashboard",
      "title": "대시보드",
      "icon": "fas fa-tachometer-alt",
      "module_spec": "사이트 현황 요약 및 주요 통계 표시 (SB-Admin 기본 레이아웃 활용)"
    },
    {
      "id": "member_management",
      "title": "회원 관리",
      "icon": "fas fa-users",
      "role": "관리자_직접_운영",
      "module_spec": "회원 목록 조회, 정보 수정/삭제, 권한 설정 기능 제공"
    },
    {
      "id": "admin_contents",
      "title": "관리자 직접 업로드 메뉴",
      "icon": "fas fa-edit",
      "sub_menus": [
        {
          "id": "post_management",
          "title": "게시물 관리",
          "role": "관리자_직접_운영",
          "module_spec": "CRUD 기능 (목록/작성/수정/삭제). 관리자가 직접 내용을 작성하여 게시"
        },
        {
          "id": "quest_management",
          "title": "퀘스트 관리",
          "role": "관리자_직접_운영",
          "module_spec": "CRUD 기능 (목록/작성/수정/삭제). 관리자가 직접 퀘스트 정보 및 미션 파일 업로드"
        }
      ]
    },
    {
      "id": "user_submission_review",
      "title": "놀이인증 관리",
      "icon": "fas fa-medal",
      "role": "회원_업로드_심사",
      "module_spec": {
        "description": "회원들이 직접 업로드한 내용을 심사하는 메뉴",
        "features": [
          "회원 제출 목록 조회 (미승인/승인/반려 상태 구분)",
          "제출된 인증 내용 및 첨부 파일(이미지/영상 등) 상세 확인",
          "승인/반려 처리 기능 제공",
          "반려 시 사유 입력 필드 제공"
        ]
      },
      "note": "요청에 따라, 회원들이 직접 정보를 올리는 **유일한 메뉴**이며, 관리자는 **심사 및 처리**만 담당함."
    },
    {
      "id": "settings",
      "title": "사이트 설정",
      "icon": "fas fa-cogs",
      "role": "관리자_직접_운영",
      "module_spec": "사이트 기본 설정, 운영 정책, 배너/팝업 관리 기능 제공"
    }
  ]
}