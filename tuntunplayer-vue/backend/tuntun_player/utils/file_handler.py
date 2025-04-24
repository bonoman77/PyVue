import os
import random
from flask import current_app, send_file, request


def file_download():
    file_path = request.args.get("file_path")
    file_name = request.args.get("file_name")
    download_yn = bool(int(request.args.get("download_yn")))

    return send_file(os.path.join(file_path, file_name), as_attachment=download_yn)


def file_format_check(file_name):
    if '.' not in file_name:
        return False

    extension = file_name.split('.')[-1]
    return extension in current_app.config['UPLOAD_EXTENSIONS']


class FileHandler:
    def __init__(self, upload_path):
        self.upload_path = upload_path

    def file_upload(self, upload_files):

        if not os.path.exists(self.upload_path):
            os.makedirs(self.upload_path)

        file_name_list = []
        for upload_file in upload_files:
            if upload_file.filename != '' and file_format_check(upload_file.filename):
                # file_name = secure_filename(upload_file.filename)
                file_name = upload_file.filename.replace("..", "")  # 인젝션 방어
                unique_file_name = self.file_duplicate_handle(file_name)
                file_path = os.path.join(self.upload_path, unique_file_name)
                with open(file_path, 'wb') as f:
                    for chunk in upload_file.stream:
                        f.write(chunk)
                file_name_list.append(unique_file_name)

        return "||".join(file_name_list)

    def file_duplicate_handle(self, file_name):
        alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
        max_attempts = 10
        attempts = 0

        while os.path.exists(os.path.join(self.upload_path, file_name)) and attempts < max_attempts:
            choice_val = "_" + "".join(random.choice(alphabet) for _ in range(4))
            file_name, extension = os.path.splitext(file_name)
            file_name += choice_val + extension
            attempts += 1

        return file_name


