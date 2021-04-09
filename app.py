from flask import Flask, render_template
import Client


app = Flask(__name__)


@app.route("/")
def template_test():
    elements = Client.run()
    print(elements)
    return render_template('template.html', my_string="Weather data", my_list=elements)


if __name__ == '__main__':
    app.run(debug=True)
