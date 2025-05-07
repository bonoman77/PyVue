import os
import time
import threading
import pymysql
import logging
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

import base64
# MariaDB 연결 설정
server = 'localhost'
database = 'smpw'
username = os.environ.get("db_user", "root")
password = os.environ.get("db_password", "")
port = 3306  # MariaDB 기본 포트

def _convert_bytes(obj):
    """딕셔너리/리스트 내 bytes 타입을 base64 문자열로 변환"""
    if isinstance(obj, dict):
        return {k: _convert_bytes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_bytes(item) for item in obj]
    elif isinstance(obj, bytes):
        return base64.b64encode(obj).decode('utf-8')
    else:
        return obj

class ConnectionPool:
    """데이터베이스 연결 풀 클래스"""
    
    def __init__(self, min_connections=2, max_connections=10):
        self.min_connections = min_connections
        self.max_connections = max_connections
        self.pool = []
        self.in_use = {}
        self.lock = threading.RLock()
        self.initialize_pool()
    
    def initialize_pool(self):
        """초기 연결 풀 생성"""
        with self.lock:
            for _ in range(self.min_connections):
                try:
                    conn = self._create_connection()
                    self.pool.append(conn)
                except Exception as e:
                    logger.error(f"연결 풀 초기화 중 오류: {str(e)}")
    
    def _create_connection(self):
        """새 데이터베이스 연결 생성"""
        try:
            conn = pymysql.connect(
                host=server,
                user=username,
                password=password,
                database=database,
                port=port,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            return conn
        except Exception as e:
            logger.error(f"데이터베이스 연결 생성 중 오류: {str(e)}")
            raise
    
    def get_connection(self, timeout=5):
        """풀에서 연결 가져오기"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            with self.lock:
                if self.pool:
                    conn = self.pool.pop(0)
                    
                    # 연결 유효성 검사
                    try:
                        cursor = conn.cursor()
                        cursor.execute("SELECT 1")
                        cursor.close()
                    except:
                        # 연결이 끊어진 경우 새 연결 생성
                        try:
                            conn = self._create_connection()
                        except Exception as e:
                            logger.error(f"손상된 연결 재생성 중 오류: {str(e)}")
                            if len(self.pool) + len(self.in_use) < self.min_connections:
                                continue  # 최소 연결 수 유지를 위해 재시도
                            raise
                    
                    # 사용 중인 연결 추적
                    self.in_use[id(conn)] = conn
                    return conn
                
                # 최대 연결 수에 도달하지 않았다면 새 연결 생성
                if len(self.in_use) < self.max_connections:
                    try:
                        conn = self._create_connection()
                        self.in_use[id(conn)] = conn
                        return conn
                    except Exception as e:
                        logger.error(f"새 연결 생성 중 오류: {str(e)}")
                        raise
            
            # 연결을 얻지 못했다면 잠시 대기 후 재시도
            time.sleep(0.1)
        
        # 타임아웃 발생
        raise TimeoutError("데이터베이스 연결을 얻는 데 시간이 초과되었습니다.")
    
    def release_connection(self, conn):
        """연결을 풀로 반환"""
        with self.lock:
            conn_id = id(conn)
            if conn_id in self.in_use:
                del self.in_use[conn_id]
                
                # 연결 유효성 검사
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT 1")
                    cursor.close()
                    
                    # 풀 크기가 최소 연결 수보다 작으면 연결 유지
                    if len(self.pool) < self.min_connections:
                        self.pool.append(conn)
                    else:
                        conn.close()
                except:
                    # 연결이 손상된 경우 닫기
                    try:
                        conn.close()
                    except:
                        pass
                    
                    # 최소 연결 수 유지
                    if len(self.pool) + len(self.in_use) < self.min_connections:
                        try:
                            new_conn = self._create_connection()
                            self.pool.append(new_conn)
                        except Exception as e:
                            logger.error(f"연결 풀 재생성 중 오류: {str(e)}")
    
    def close_all(self):
        """모든 연결 닫기"""
        with self.lock:
            # 풀에 있는 연결 닫기
            for conn in self.pool:
                try:
                    conn.close()
                except:
                    pass
            self.pool.clear()
            
            # 사용 중인 연결 닫기
            for conn_id, conn in list(self.in_use.items()):
                try:
                    conn.close()
                except:
                    pass
            self.in_use.clear()

# 전역 연결 풀 생성
connection_pool = ConnectionPool()

@contextmanager
def get_db_connection():
    """데이터베이스 연결을 안전하게 획득하고 반환하는 컨텍스트 매니저"""
    conn = None
    try:
        conn = connection_pool.get_connection()
        yield conn
    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except:
                pass
        logger.error(f"데이터베이스 연결 사용 중 오류: {str(e)}")
        raise
    finally:
        if conn:
            try:
                connection_pool.release_connection(conn)
            except Exception as e:
                logger.error(f"연결 반환 중 오류: {str(e)}")

def execute_without_return(query, params=None):
    """쿼리 실행 (반환값 없음)"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
    except Exception as e:
        logger.error(f"쿼리 실행 중 오류 (반환값 없음): {str(e)}")
        raise

def execute_return(query, params=None):
    """쿼리 실행 (단일 결과 반환)"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                result = cursor.fetchone()
                return _convert_bytes(result)
    except Exception as e:
        logger.error(f"쿼리 실행 중 오류 (단일 결과): {str(e)}")
        raise

def execute_return_all(query, params=None):
    """쿼리 실행 (모든 결과 반환)"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                results = cursor.fetchall()
                return _convert_bytes(results)
    except Exception as e:
        logger.error(f"쿼리 실행 중 오류 (모든 결과): {str(e)}")
        raise

def callproc_without_return(proc_name, params=None):
    """프로시저 실행 (반환값 없음)"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc(proc_name, params or [])
                conn.commit()
    except Exception as e:
        logger.error(f"프로시저 실행 중 오류 (반환값 없음): {str(e)}")
        raise

def callproc_return(proc_name, params=None):
    """프로시저 실행 (단일 결과 반환)"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc(proc_name, params or [])
                result = cursor.fetchone()
                return _convert_bytes(result)
    except Exception as e:
        logger.error(f"프로시저 실행 중 오류 (단일 결과): {str(e)}")
        raise

def callproc_return_all(proc_name, params=None):
    """프로시저 실행 (모든 결과 반환)"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc(proc_name, params or [])
                results = cursor.fetchall()
                return _convert_bytes(results)
    except Exception as e:
        logger.error(f"프로시저 실행 중 오류 (모든 결과): {str(e)}")
        raise

# 애플리케이션 종료 시 모든 연결 정리
import atexit
atexit.register(connection_pool.close_all)