from flask import Flask, request, render_template, jsonify, send_file
import db
import llm
from Usecase import analysis_Usecase
import asyncio

app = Flask(__name__)


@app.route('/')
def hello():  # put application's code here
    return render_template('index.html')


@app.route('/analysis')
def analysis():
    comic_title = request.args.get('title', default='', type=str)

    analysis_Usecase(comic_title) #서버에서 동기 실행시 주석 제거할 부분

    return render_template('analysis.html', title=comic_title)


@app.route("/delete_webtoon", methods=['DELETE'])
def delete_webtoon():
    data = request.json
    record_id = data.get('id')

    result = db.delete_webtoon(record_id)
    return jsonify({"success": True, "message": "delete 성공"})


# 웹툰 목록
@app.route("/webtoons")
def webtoons():
    records = db.get_webtoons()
    return records


# 웹툰 1개
@app.route("/webtoon_one")
def one_webtoon():
    title = request.args.get('title')

    result = db.get_one_webtoons(title)
    return result


@app.route("/webtoon_all")
def all_webtoon():
    result = db.get_all_webtoons()
    return result


@app.route("/new_webtoon", methods=['GET', 'POST'])
def new_webtoon():
    if request.method == 'POST':
        data = request.json
        title = data.get('title')
        url = data.get('url')
        if title and url:
            result = db.create_webtoon(title, url)
            return {"message": "Webtoon added successfully"}
        else:
            return {"error": "Title and URL are required fields"}, 400
    else:
        return {"error": "Method not allowed"}, 405

@app.route('/get_emotion_data/<titleId>/<episodeNumber>')
def get_emotion_data(titleId, episodeNumber):
    filename = f'Webtoon_emotion_nlp_{titleId}/emotion_comments_{titleId}_{episodeNumber}.txt'
    return send_file(filename, mimetype='text/plain')


if __name__ == '__main__':
    app.run()