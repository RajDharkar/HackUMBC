<html>
    
</html>from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    names = ["ishaan", "rajveer"]
    return render_template("index.html", names=names)

if __name__ == '__main__':
    app.run(debug=True)