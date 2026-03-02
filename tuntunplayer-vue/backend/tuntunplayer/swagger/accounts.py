# backend/tuntunplayer/swagger/accounts.py

def get_accounts_swagger():
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
                                        "$ref": "#/definitions/User"
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
                                        "$ref": "#/definitions/User"
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
            }
        }
    }