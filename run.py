from flask import Flask
from flask import request
from flask import redirect
from flask import render_template

from parser import Parser

app = Flask(__name__)


@app.route("/")
def root():
	return redirect("/search")

@app.route("/search", methods=["GET"])
def search():
	results	= None
	query 	= request.args.get('query')
	if query:
		parser	= Parser(query)
		results	= parser.suggestions()

	return render_template('search.html', query=query, results=results)

@app.route("/timeline", methods=["GET"])
def timeline():
	data = None
	query = request.args.get('query')
	if query:
		parser = Parser(query)
		data = parser.results()

	return render_template('timeline.html', data=data)

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
