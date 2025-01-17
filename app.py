from flask import Flask, render_template


from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/resume')
def get_resume():
    return render_template("resume.html", page_title="Моє резюме")

if __name__ == '__main__':
    app.run(debug=True)