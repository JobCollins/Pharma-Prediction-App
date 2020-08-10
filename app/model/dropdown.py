from flask import Flask, render_template, request
from processing import readFile



app = Flask(__name__)
app.debug = True



new_data, date = readFile()

products = list(new_data.columns)
products_copy = products.copy()


@app.route('/', methods=['GET'])
def dropdown():
    choices = list(zip(products, products_copy))
    return render_template('test.html', choices=choices)

if __name__ == "__main__":
    app.run()