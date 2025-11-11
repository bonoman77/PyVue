from .accounts import get_accounts_swagger
from .boards import get_boards_swagger
from .todos import get_todos_swagger

def get_swagger_docs():
    # 공통 정보
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "SMPW API",
            "description": "SMPW 백엔드 API 문서",
            "version": "1.0"
        },
        "basePath": "/",
        "schemes": ["http", "https"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "tags": [
            {"name": "accounts", "description": "사용자 계정 관련 API"},
            {"name": "boards", "description": "게시판 관련 API"},
            {"name": "todos", "description": "할 일 관련 API"}
        ],
        "paths": {},
        "definitions": {
            "User": {
                "type": "object",
                "properties": {
                    "userId": {
                        "type": "integer",
                        "description": "사용자 ID"
                    },
                    "userName": {
                        "type": "string",
                        "description": "사용자 이름"
                    },
                    "userEmail": {
                        "type": "string",
                        "description": "사용자 이메일"
                    }
                }
            },
            "Board": {
                "type": "object",
                "properties": {
                    "boardId": {
                        "type": "integer",
                        "description": "게시판 ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "게시판 제목"
                    },
                    "content": {
                        "type": "string",
                        "description": "게시판 내용"
                    },
                    "author": {
                        "type": "string",
                        "description": "작성자"
                    },
                    "createdAt": {
                        "type": "string",
                        "format": "date-time",
                        "description": "작성 일시"
                    }
                }
            },
            "Todo": {
                "type": "object",
                "properties": {
                    "todoId": {
                        "type": "integer",
                        "description": "할 일 ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "할 일 제목"
                    },
                    "completed": {
                        "type": "boolean",
                        "description": "완료 여부"
                    },
                    "userId": {
                        "type": "integer",
                        "description": "사용자 ID"
                    },
                    "createdAt": {
                        "type": "string",
                        "format": "date-time",
                        "description": "작성 일시"
                    }
                }
            }
        }
    }
    
    # 각 모듈의 API 문서 통합
    accounts_paths = get_accounts_swagger().get("paths", {})
    boards_paths = get_boards_swagger().get("paths", {})
    todos_paths = get_todos_swagger().get("paths", {})
    
    # paths 병합
    swagger_template["paths"].update(accounts_paths)
    swagger_template["paths"].update(boards_paths)
    swagger_template["paths"].update(todos_paths)
    
    return swagger_template