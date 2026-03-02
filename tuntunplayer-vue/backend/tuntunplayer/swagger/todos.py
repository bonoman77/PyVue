# backend/tuntunplayer/swagger.py

def get_todos_swagger():
    return {
        "swagger": "2.0",
        "info": {
            "title": "TuntunPlayer API",
            "description": "TuntunPlayer 백엔드 API 문서",
            "version": "1.0"
        },
        "basePath": "/",
        "schemes": ["http", "https"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "tags": [
            {
                "name": "accounts",
                "description": "사용자 계정 관련 API"
            },
            {
                "name": "todos",
                "description": "할 일 관련 API"
            }
        ],
        "paths": {
            "/accounts/login": {
                "post": {
                    "tags": ["accounts"],
                    "summary": "사용자 로그인",
                    "description": "이메일과 비밀번호로 로그인합니다.",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "userEmail": {
                                        "type": "string",
                                        "example": "user@example.com"
                                    },
                                    "password": {
                                        "type": "string",
                                        "example": "password123"
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "로그인 성공",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "token": {"type": "string"},
                                    "user": {
                                        "type": "object",
                                        "properties": {
                                            "userId": {"type": "integer"},
                                            "userName": {"type": "string"},
                                            "userEmail": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        },
                        "401": {
                            "description": "인증 실패",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "로그인 실패: 잘못된 사용자 정보"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/accounts/register": {
                "post": {
                    "tags": ["accounts"],
                    "summary": "사용자 회원가입",
                    "description": "새로운 사용자를 등록합니다.",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "userName": {
                                        "type": "string",
                                        "example": "홍길동"
                                    },
                                    "userEmail": {
                                        "type": "string",
                                        "example": "user@example.com"
                                    },
                                    "password": {
                                        "type": "string",
                                        "example": "password123"
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "회원가입 성공",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "회원가입 성공"
                                    },
                                    "userId": {"type": "integer"}
                                }
                            }
                        },
                        "400": {
                            "description": "잘못된 요청",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "이미 등록된 이메일입니다."
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/accounts/verify-token": {
                "post": {
                    "tags": ["accounts"],
                    "summary": "토큰 검증",
                    "description": "JWT 토큰의 유효성을 검증합니다.",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": True,
                            "description": "Bearer 토큰"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "유효한 토큰",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "valid": {
                                        "type": "boolean",
                                        "example": True
                                    },
                                    "user": {
                                        "type": "object",
                                        "properties": {
                                            "userId": {"type": "integer"},
                                            "userName": {"type": "string"},
                                            "userEmail": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        },
                        "401": {
                            "description": "유효하지 않은 토큰",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "valid": {
                                        "type": "boolean",
                                        "example": False
                                    },
                                    "message": {
                                        "type": "string",
                                        "example": "유효하지 않은 토큰입니다."
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/accounts/reset-password": {
                "post": {
                    "tags": ["accounts"],
                    "summary": "비밀번호 재설정 요청",
                    "description": "이메일을 통해 비밀번호 재설정 링크를 요청합니다.",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "userEmail": {
                                        "type": "string",
                                        "example": "user@example.com"
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "이메일 전송 성공",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "비밀번호 재설정 이메일이 전송되었습니다."
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "사용자를 찾을 수 없음",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "해당 이메일의 사용자를 찾을 수 없습니다."
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/todos": {
                "get": {
                    "tags": ["todos"],
                    "summary": "할 일 목록 조회",
                    "description": "사용자의 할 일 목록을 조회합니다.",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": True,
                            "description": "Bearer 토큰"
                        },
                        {
                            "name": "completed",
                            "in": "query",
                            "type": "boolean",
                            "required": False,
                            "description": "완료 상태로 필터링 (true/false)"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "할 일 목록 조회 성공",
                            "schema": {
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/Todo"
                                }
                            }
                        },
                        "401": {
                            "description": "인증 실패",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "인증이 필요합니다."
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["todos"],
                    "summary": "할 일 생성",
                    "description": "새 할 일을 생성합니다.",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": True,
                            "description": "Bearer 토큰"
                        },
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "title": {
                                        "type": "string",
                                        "example": "할 일 제목"
                                    },
                                    "completed": {
                                        "type": "boolean",
                                        "example": False
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "할 일 생성 성공",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "할 일이 생성되었습니다."
                                    },
                                    "todoId": {
                                        "type": "integer"
                                    }
                                }
                            }
                        },
                        "401": {
                            "description": "인증 실패",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "인증이 필요합니다."
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/todos/{todoId}": {
                "get": {
                    "tags": ["todos"],
                    "summary": "할 일 상세 조회",
                    "description": "특정 할 일의 상세 정보를 조회합니다.",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": True,
                            "description": "Bearer 토큰"
                        },
                        {
                            "name": "todoId",
                            "in": "path",
                            "type": "integer",
                            "required": True,
                            "description": "조회할 할 일 ID"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "할 일 조회 성공",
                            "schema": {
                                "$ref": "#/definitions/Todo"
                            }
                        },
                        "401": {
                            "description": "인증 실패",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "인증이 필요합니다."
                                    }
                                }
                            }
                        },
                        "403": {
                            "description": "권한 없음",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "해당 할 일에 접근할 권한이 없습니다."
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "할 일을 찾을 수 없음",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "해당 ID의 할 일을 찾을 수 없습니다."
                                    }
                                }
                            }
                        }
                    }
                },
                "put": {
                    "tags": ["todos"],
                    "summary": "할 일 수정",
                    "description": "특정 할 일의 정보를 수정합니다.",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": True,
                            "description": "Bearer 토큰"
                        },
                        {
                            "name": "todoId",
                            "in": "path",
                            "type": "integer",
                            "required": True,
                            "description": "수정할 할 일 ID"
                        },
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "title": {
                                        "type": "string",
                                        "example": "수정된 할 일 제목"
                                    },
                                    "completed": {
                                        "type": "boolean",
                                        "example": True
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "할 일 수정 성공",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "할 일이 수정되었습니다."
                                    }
                                }
                            }
                        },
                        "401": {
                            "description": "인증 실패",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "인증이 필요합니다."
                                    }
                                }
                            }
                        },
                        "403": {
                            "description": "권한 없음",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "해당 할 일을 수정할 권한이 없습니다."
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "할 일을 찾을 수 없음",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "해당 ID의 할 일을 찾을 수 없습니다."
                                    }
                                }
                            }
                        }
                    }
                },
                "delete": {
                    "tags": ["todos"],
                    "summary": "할 일 삭제",
                    "description": "특정 할 일을 삭제합니다.",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": True,
                            "description": "Bearer 토큰"
                        },
                        {
                            "name": "todoId",
                            "in": "path",
                            "type": "integer",
                            "required": True,
                            "description": "삭제할 할 일 ID"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "할 일 삭제 성공",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "할 일이 삭제되었습니다."
                                    }
                                }
                            }
                        },
                        "401": {
                            "description": "인증 실패",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "인증이 필요합니다."
                                    }
                                }
                            }
                        },
                        "403": {
                            "description": "권한 없음",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "해당 할 일을 삭제할 권한이 없습니다."
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "할 일을 찾을 수 없음",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "해당 ID의 할 일을 찾을 수 없습니다."
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
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
                        "description": "완료 상태"
                    }
                }
            }
        }
    }