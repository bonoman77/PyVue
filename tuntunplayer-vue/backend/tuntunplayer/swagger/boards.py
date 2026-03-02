def get_boards_swagger():
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
                "name": "boards",
                "description": "게시판 관련 API"
            }
        ],
        "paths": {
            "/boards": {
                "get": {
                    "tags": ["boards"],
                    "summary": "게시판 목록 조회",
                    "description": "모든 게시판 목록을 조회합니다.",
                    "parameters": [
                        {
                            "name": "page",
                            "in": "query",
                            "type": "integer",
                            "required": False,
                            "description": "페이지 번호 (기본값: 1)"
                        },
                        {
                            "name": "per_page",
                            "in": "query",
                            "type": "integer",
                            "required": False,
                            "description": "페이지당 항목 수 (기본값: 10)"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "게시판 목록 조회 성공",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "boards": {
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/definitions/Board"
                                        }
                                    },
                                    "total": {
                                        "type": "integer",
                                        "description": "전체 게시판 수"
                                    },
                                    "page": {
                                        "type": "integer",
                                        "description": "현재 페이지"
                                    },
                                    "pages": {
                                        "type": "integer",
                                        "description": "전체 페이지 수"
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["boards"],
                    "summary": "게시판 생성",
                    "description": "새 게시판을 생성합니다.",
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
                                        "example": "게시판 제목"
                                    },
                                    "content": {
                                        "type": "string",
                                        "example": "게시판 내용"
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "게시판 생성 성공",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "게시판이 생성되었습니다."
                                    },
                                    "boardId": {
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
            "/boards/{boardId}": {
                "get": {
                    "tags": ["boards"],
                    "summary": "게시판 상세 조회",
                    "description": "특정 게시판의 상세 정보를 조회합니다.",
                    "parameters": [
                        {
                            "name": "boardId",
                            "in": "path",
                            "type": "integer",
                            "required": True,
                            "description": "조회할 게시판 ID"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "게시판 조회 성공",
                            "schema": {
                                "$ref": "#/definitions/Board"
                            }
                        },
                        "404": {
                            "description": "게시판을 찾을 수 없음",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "해당 ID의 게시판을 찾을 수 없습니다."
                                    }
                                }
                            }
                        }
                    }
                },
                "put": {
                    "tags": ["boards"],
                    "summary": "게시판 수정",
                    "description": "특정 게시판의 정보를 수정합니다.",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": True,
                            "description": "Bearer 토큰"
                        },
                        {
                            "name": "boardId",
                            "in": "path",
                            "type": "integer",
                            "required": True,
                            "description": "수정할 게시판 ID"
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
                                        "example": "수정된 제목"
                                    },
                                    "content": {
                                        "type": "string",
                                        "example": "수정된 내용"
                                    }
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "게시판 수정 성공",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "게시판이 수정되었습니다."
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
                                        "example": "해당 게시판을 수정할 권한이 없습니다."
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "게시판을 찾을 수 없음",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "해당 ID의 게시판을 찾을 수 없습니다."
                                    }
                                }
                            }
                        }
                    }
                },
                "delete": {
                    "tags": ["boards"],
                    "summary": "게시판 삭제",
                    "description": "특정 게시판을 삭제합니다.",
                    "parameters": [
                        {
                            "name": "Authorization",
                            "in": "header",
                            "type": "string",
                            "required": True,
                            "description": "Bearer 토큰"
                        },
                        {
                            "name": "boardId",
                            "in": "path",
                            "type": "integer",
                            "required": True,
                            "description": "삭제할 게시판 ID"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "게시판 삭제 성공",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "게시판이 삭제되었습니다."
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
                                        "example": "해당 게시판을 삭제할 권한이 없습니다."
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "게시판을 찾을 수 없음",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "message": {
                                        "type": "string",
                                        "example": "해당 ID의 게시판을 찾을 수 없습니다."
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "definitions": {
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
                    }
                }
            }
        }
    }