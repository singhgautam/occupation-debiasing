from flask import Flask, render_template, request, jsonify
import json
import bias_checker
import extract_SVOs


def is_occupation(occ):
	fh = open("data/result.txt")
	for line in fh:
		toks = line.split(",")
		words = [tok.strip().lower() for tok in toks]
		if words[0] == occ.lower().strip():
			fh.close()
			return words[2]
	fh.close()
	return False


app = Flask(__name__)


@app.route("/")
def home():
	return render_template("home.html")

@app.route("/index.html")
def demo():
	return render_template("index.html")

@app.route("/api/bias-checker", methods=['POST', 'GET'])
def handle():

	tf = int(request.form['from'])
	tt = int(request.form['to'])
	country = str(request.form['place'])
	sentence = str(request.form['query'])

	biased, triplets = bias_checker.check_for_bias(sentence)
	occ_triplets = [trp for trp in triplets if is_occupation(trp[2])]
	for i in range(len(occ_triplets)):
		occ_triplets[i] = (occ_triplets[i][0].capitalize(), occ_triplets[i][1], occ_triplets[i][2])

	resp, occ_triplets = bias_checker.output(biased, tf, tt, country, occ_triplets)
	print(occ_triplets)
	return jsonify(response=[resp, occ_triplets])


if __name__ == '__main__':
   app.run(host = "0.0.0.0", port="8080", debug = True)
