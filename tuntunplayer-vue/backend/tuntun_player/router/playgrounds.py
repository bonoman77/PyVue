import openai
import tuntun_player.dbconns as conn
from flask import Blueprint, current_app, request, session, render_template, redirect, flash, url_for, jsonify
from tuntun_player.enums import RouteKind, ProductKind, ContentGroup
from tuntun_player.utils.page_handler import paged_list
from tuntun_player.utils.auth_handler import login_required, admin_required

bp = Blueprint('playgrounds', __name__)

# Initialize OpenAI API key
# openai.api_key = current_app.config.get('OPENAI_API_KEY')
openai.api_key = "asdfasdfasdfasdf"

# Function to interact with ChatGPT
def chat_with_gpt(prompt):
    response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "I'm Gyuri!"},
                {"role": "system", "content": "I'm a little dragon."},
                {"role": "system", "content": "I'm eight years old."},
                {"role": "system", "content": "I only speak English."},
                {"role": "system", "content": "I'm a character from a fairy tale book."},
                {"role": "system", "content": "I was born in Korea"},
                {"role": "system", "content": "My house is in Seoul."},
                {"role": "system", "content": "My house is in a place called TuntunEnglish in Seoul."},
                {"role": "system", "content": "I love drawing"},
                {"role": "system", "content": "My color is green."},
                {"role": "system", "content": "I speak English at an elementary school level."},
                {"role": "system", "content": "I love giving compliments."},
                {"role": "system", "content": "I like to joke, but I'm not rude."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
    return response.choices[0].message.content.strip()


@bp.route('/chat_room')
def chat_room():
    return render_template('playgrounds/chat_room.html')


@bp.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']

    gpt_response = chat_with_gpt(user_input)
    response = {"type": "chatgpt", "data": gpt_response}

    return jsonify(response)
