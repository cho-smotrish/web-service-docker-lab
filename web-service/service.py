from flask import Flask, jsonify, request

app = Flask(__name__)

cocktails = [
    {"name": "Мохито", "base": "Ром", "ingredients": "Белый ром; лайм; мята; содовая; сахарный сироп", "preparation": "Смешать ром, лайм, мяту и сироп со льдом, добавить содовую", "price": 420},
    {"name": "Маргарита", "base": "Текила", "ingredients": "Текила; апельсиновый ликёр; сок лайма", "preparation": "Встряхнуть все ингредиенты со льдом и перелить в охлаждённый бокал", "price": 460},
    {"name": "Негрони", "base": "Джин", "ingredients": "Джин; красный вермут; кампари", "preparation": "Перемешать ингредиенты со льдом и украсить долькой апельсина", "price": 480},
    {"name": "Космополитен", "base": "Водка", "ingredients": "Водка; клюквенный сок; апельсиновый ликёр; лайм", "preparation": "Встряхнуть ингредиенты со льдом и процедить в бокал", "price": 440},
    {"name": "Пина Колада", "base": "Ром", "ingredients": "Белый ром; кокосовые сливки; ананасовый сок", "preparation": "Взбить ингредиенты со льдом до однородной текстуры", "price": 450},
    {"name": "Виски сауэр", "base": "Виски", "ingredients": "Виски; лимонный сок; сахарный сироп; белок", "preparation": "Встряхнуть без льда, затем со льдом и процедить", "price": 470},
    {"name": "Джин-тоник", "base": "Джин", "ingredients": "Джин; тоник; лайм", "preparation": "Наполнить бокал льдом, добавить джин и тоник", "price": 390},
    {"name": "Московский мул", "base": "Водка", "ingredients": "Водка; имбирное пиво; сок лайма", "preparation": "Собрать напиток в кружке со льдом и перемешать", "price": 430},
    {"name": "Дайкири", "base": "Ром", "ingredients": "Белый ром; сок лайма; сахарный сироп", "preparation": "Встряхнуть ингредиенты со льдом и процедить", "price": 410},
    {"name": "Апероль шприц", "base": "Ликёр", "ingredients": "Апероль; просекко; содовая; апельсин", "preparation": "Налить просекко, апероль и содовую в бокал со льдом", "price": 400}
]


@app.get("/search")
def search():
    query = request.args.get("query", "").lower().strip()
    result = [
        cocktail for cocktail in cocktails
        if query in cocktail["name"].lower() or query in cocktail["base"].lower()
    ]
    return jsonify(result)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
