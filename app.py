from flask import Flask, render_template, request
import random

app = Flask(__name__)

takimlar = [
    "Amedspor",
    "Çorumspor",
    "Alanyaspor",
    "Beşiktaş",
    "Rizespor",
    "Erzurumspor",
    "Eyüpspor",
    "Fenerbahçe",
    "Galatasaray",
    "Gaziantep FK",
    "Gençlerbirliği",
    "Göztepe",
    "Başakşehir FK",
    "Kasımpaşa",
    "Kocaelispor",
    "Samsunspor",
    "Trabzonspor",
    "Konyaspor"
]


@app.route("/", methods=["GET", "POST"])
def ana_sayfa():

    sonuc = ""

    if request.method == "POST":

        takim1 = request.form["takim1"]
        takim2 = request.form["takim2"]

        if takim1 == takim2:
            sonuc = "Aynı takım kendisiyle oynayamaz!"

        else:
            gol1 = random.randint(0, 5)
            gol2 = random.randint(0, 5)

            if gol1 > gol2:
                kazanan = takim1 + " kazandı!"

            elif gol2 > gol1:
                kazanan = takim2 + " kazandı!"

            else:
                kazanan = "Berabere!"

            sonuc = f"{takim1} {gol1} - {gol2} {takim2} | {kazanan}"

    return render_template(
        "index.html",
        takimlar=takimlar,
        sonuc=sonuc
    )


@app.route("/fikstur")
def fikstur():
    return render_template("fikstur.html")

@app.route("/mac")
def mac():
    return render_template("mac.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)