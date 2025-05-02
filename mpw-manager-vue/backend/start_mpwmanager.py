# import os 
# os.environ['FLASK_ENV'] = 'production'

# from절을 호출하는 순간 해당 프로젝트의 __init__은 자동실행됨.
from mpw_manager import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=4000)
