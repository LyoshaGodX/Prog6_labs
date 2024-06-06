from flask import Flask

import utils
from utils import factorial_cashe, factorial_no_cashe, factorial_cashe_copy

app = Flask(__name__)


@app.route("/")
def hello_world():
    return (f'<h2>Ссылки:</h2>'
            f'<h2><a href="/about">Об авторе</a></h2>'
            f'<h2><a href="/calc/factorial/69">Факториал 69</a></h2>'
            f'<h2><a href="/calc/factorial_cashe/69">Факториал 69 (с кэшем)</a></h2>'
            f'<h2><a href="/calc/factorial_cashe2/69"> Посмотреть факториал с загруженным кэшем</a></h2>')


@app.route("/about")
def author():
    return ("<h1><p>Лёха! (Клементьев Алексей)</p></h1>"
            "<h2><a href='/'>Главная</a></h2>")

@app.route("/save_to_cache/<string:func>")
def save_to_cache(func):
    if func == "factorial_cashe":
        utils.save_cache(utils.get_cache(factorial_cashe), 'cache.json')
        res = (f'<h2>Кэш сохранен</h2>'
               f'<h2><a href="/">Главная</a></h2>'
               f'<h2><a href="/load_from_cache/factorial_cashe2">Загрузить кэш в factorial_cashe2</a></h2>')
    else:
        res = "<h2>Unknown function</h2>"

    return str(res)

@app.route("/load_from_cache/<string:func>")
def load_from_cache(func):
    if func == "factorial_cashe2":
        utils.load_cache('cache.json', factorial_cashe_copy)
        res = (f'<h2>Кэш загружен. На страничке калькулейта функции можно его чекнуть</h2>'
               f'<h2><a href="/">Главная</a></h2>')
    else:
        res = "<h2>Unknown function</h2>"

    return str(res)


@app.route("/calc/<string:func>/<int:number>")
def calculate(func, number):
    if func == "factorial":
        temp = factorial_no_cashe(number)
        res = (f'<h2>{temp[0]} (с кэшем)</h2>'
               f'<h2>Время выполнения: {temp[1]} мс</h2><br><br>'
               f'<h2><a href="/">Главная</a></h2>')
    elif func == "factorial_cashe":
        temp = factorial_cashe(number)
        res = (f'<h2>{temp[0]} (с кэшем)</h2>'
               f'<h2>Время выполнения: {temp[1]} мс</h2>'
               f'<h2>Кэш: {utils.get_cache(factorial_cashe)}</h2><br><br>'
               f'<h2><a href="/save_to_cache/factorial_cashe">Сохранить кэш</a> | <a href="/load_from_cache/factorial_cashe2">Загрузить кэш в factorial_cashe2</a> | <a href="/">Главная</a></h2>')
    elif func == "factorial_cashe2":
        res = (f'<h2>{utils.get_cache(factorial_cashe_copy)}</h2>'
               f'<h2><a href="/">Главная</a></h2>')
    else:
        res = "<h2>Unknown function</h2>"

    return str(res)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
