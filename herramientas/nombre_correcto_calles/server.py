from flask import Flask, render_template, request

app = Flask(__name__)


def get_data():
    """

    """
    nombre_calle = "hola"

    distance_1 = ['hola', 'hola2', 'hola3', 'hola4', 'hola5']
    distance_2 = ['hol6', 'hola9', 'hola13', 'hola2', 'hola51']
    distance_3 = ['hol7', 'hola8', 'hola12', 'hola14', 'hola15']

    return nombre_calle, distance_1, distance_2, distance_3


@app.route("/")
def home():

    nombre_calle, d1, d2, d3 = get_data()

    return render_template('index.html',
                           nombre_calle=nombre_calle,
                           distance_1=d1, distance_2=d2, distance_3=d3)


@app.route("/submit", methods=['POST'])
def submit():
    form = request.form
    print(form)

    return home()


app.run(debug=True)
