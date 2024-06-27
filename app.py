import os
import time
from flask import Flask, request, render_template

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

def count_chars(s, t):
    count_s = {char: t.count(char) for char in s}
    total_chars = len(t)
    freq_s = {char: count / total_chars for char, count in count_s.items()}
    return count_s, freq_s

@app.route('/task10a', methods=['POST'])
def task10a():
    string_s = request.form['string_s']
    text_t = request.form['text_t']
    
    start_time = time.time()
    count_s, freq_s = count_chars(string_s, text_t)
    query_time = time.time() - start_time

    return render_template('index.html', result_10a=True, count_s=count_s, freq_s=freq_s, query_time=query_time)

@app.route('/task10b', methods=['POST'])
def task10b():
    string_s = request.form['string_s']
    text_t = request.form['text_t']
    char_c = request.form['char_c']
    
    start_time = time.time()
    replaced_t = text_t
    for char in string_s:
        replaced_t = replaced_t.replace(char, char_c)
    query_time = time.time() - start_time

    return render_template('index.html', result_10b=True, replaced_t=replaced_t, query_time=query_time)

@app.route('/task10c', methods=['POST'])
def task10c():
    # 功能实现和返回结果逻辑
    pass

@app.route('/task11a', methods=['POST'])
def task11a():
    text_t = request.form['text_t']
    
    start_time = time.time()
    word_count = len(text_t.split())
    query_time = time.time() - start_time

    return render_template('index.html', result_11a=True, word_count=word_count, query_time=query_time)

@app.route('/task11b', methods=['POST'])
def task11b():
    string_s = request.form['string_s']
    text_t = request.form['text_t']
    
    start_time = time.time()
    words = text_t.split()
    words_by_char = {char: [word for word in words if word.startswith(char)] for char in string_s}
    query_time = time.time() - start_time

    return render_template('index.html', result_11b=True, words_by_char=words_by_char, query_time=query_time)

@app.route('/task12a', methods=['POST'])
def task12a():
    text_t = request.form['text_t']
    stop_words = request.form['stop_words'].split(',')
    
    start_time = time.time()
    words = text_t.split()
    remaining_words = [word for word in words if word not in stop_words]
    removed_count = len(words) - len(remaining_words)
    remaining_text = ' '.join(remaining_words)
    query_time = time.time() - start_time

    return render_template('index.html', result_12a=True, removed_count=removed_count, remaining_text=remaining_text, query_time=query_time)

@app.route('/task12b', methods=['POST'])
def task12b():
    string_s = request.form['string_s']
    text_t = request.form['text_t']
    stop_words = request.form['stop_words'].split(',')
    
    start_time = time.time()
    words = text_t.split()
    remaining_words = [word for word in words if word not in stop_words]
    bigrams = []

    for i, word in enumerate(remaining_words):
        if word[0] in string_s:
            if i > 0:
                bigrams.append((remaining_words[i-1], word))
            if i < len(remaining_words) - 1:
                bigrams.append((word, remaining_words[i+1]))
    query_time = time.time() - start_time

    return render_template('index.html', result_12b=True, bigrams=bigrams, query_time=query_time)

if __name__ == '__main__':
    app.run(debug=True)