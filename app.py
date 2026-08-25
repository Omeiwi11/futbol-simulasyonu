from flask import Flask, render_template, request
import random
import requests
from bs4 import BeautifulSoup
import re


app = Flask(__name__)



# TAKIMLAR


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



# 2026-2027 İLK DEVRE


ilk_devre = [

    # 1
    [
        ("Galatasaray", "Çorumspor"),
        ("Konyaspor", "Rizespor"),
        ("Gaziantep FK", "Alanyaspor"),
        ("Gençlerbirliği", "Fenerbahçe"),
        ("Kasımpaşa", "Trabzonspor"),
        ("Beşiktaş", "Eyüpspor"),
        ("Amedspor", "Erzurumspor"),
        ("Başakşehir FK", "Kocaelispor"),
        ("Samsunspor", "Göztepe")
    ],

    # 2
    [
        ("Erzurumspor", "Galatasaray"),
        ("Rizespor", "Samsunspor"),
        ("Fenerbahçe", "Konyaspor"),
        ("Çorumspor", "Kasımpaşa"),
        ("Eyüpspor", "Gaziantep FK"),
        ("Trabzonspor", "Başakşehir FK"),
        ("Alanyaspor", "Beşiktaş"),
        ("Göztepe", "Gençlerbirliği"),
        ("Kocaelispor", "Amedspor")
    ],

    # 3
    [
        ("Gençlerbirliği", "Erzurumspor"),
        ("Konyaspor", "Kocaelispor"),
        ("Galatasaray", "Göztepe"),
        ("Gaziantep FK", "Rizespor"),
        ("Eyüpspor", "Alanyaspor"),
        ("Başakşehir FK", "Kasımpaşa"),
        ("Samsunspor", "Fenerbahçe"),
        ("Amedspor", "Trabzonspor"),
        ("Beşiktaş", "Çorumspor")
    ],

    # 4
    [
        ("Başakşehir FK", "Galatasaray"),
        ("Çorumspor", "Eyüpspor"),
        ("Erzurumspor", "Konyaspor"),
        ("Fenerbahçe", "Beşiktaş"),
        ("Göztepe", "Gaziantep FK"),
        ("Kasımpaşa", "Amedspor"),
        ("Kocaelispor", "Samsunspor"),
        ("Rizespor", "Alanyaspor"),
        ("Trabzonspor", "Gençlerbirliği")
    ],

    # 5
    [
        ("Alanyaspor", "Göztepe"),
        ("Amedspor", "Başakşehir FK"),
        ("Beşiktaş", "Erzurumspor"),
        ("Eyüpspor", "Rizespor"),
        ("Galatasaray", "Kocaelispor"),
        ("Gaziantep FK", "Fenerbahçe"),
        ("Gençlerbirliği", "Kasımpaşa"),
        ("Konyaspor", "Trabzonspor"),
        ("Samsunspor", "Çorumspor")
    ],

    # 6
    [
        ("Amedspor", "Beşiktaş"),
        ("Başakşehir FK", "Gençlerbirliği"),
        ("Çorumspor", "Alanyaspor"),
        ("Erzurumspor", "Samsunspor"),
        ("Fenerbahçe", "Eyüpspor"),
        ("Göztepe", "Rizespor"),
        ("Kasımpaşa", "Konyaspor"),
        ("Kocaelispor", "Gaziantep FK"),
        ("Trabzonspor", "Galatasaray")
    ],

    # 7
    [
        ("Alanyaspor", "Erzurumspor"),
        ("Beşiktaş", "Kocaelispor"),
        ("Eyüpspor", "Göztepe"),
        ("Galatasaray", "Kasımpaşa"),
        ("Gaziantep FK", "Çorumspor"),
        ("Gençlerbirliği", "Amedspor"),
        ("Konyaspor", "Başakşehir FK"),
        ("Rizespor", "Fenerbahçe"),
        ("Samsunspor", "Trabzonspor")
    ],

    # 8
    [
        ("Amedspor", "Konyaspor"),
        ("Başakşehir FK", "Gaziantep FK"),
        ("Çorumspor", "Rizespor"),
        ("Erzurumspor", "Eyüpspor"),
        ("Fenerbahçe", "Alanyaspor"),
        ("Gençlerbirliği", "Galatasaray"),
        ("Kasımpaşa", "Samsunspor"),
        ("Kocaelispor", "Göztepe"),
        ("Trabzonspor", "Beşiktaş")
    ],

    # 9
    [
        ("Alanyaspor", "Kocaelispor"),
        ("Beşiktaş", "Başakşehir FK"),
        ("Eyüpspor", "Kasımpaşa"),
        ("Galatasaray", "Fenerbahçe"),
        ("Gaziantep FK", "Erzurumspor"),
        ("Göztepe", "Çorumspor"),
        ("Konyaspor", "Gençlerbirliği"),
        ("Rizespor", "Trabzonspor"),
        ("Samsunspor", "Amedspor")
    ],

    # 10
    [
        ("Amedspor", "Eyüpspor"),
        ("Başakşehir FK", "Samsunspor"),
        ("Erzurumspor", "Çorumspor"),
        ("Fenerbahçe", "Göztepe"),
        ("Gençlerbirliği", "Alanyaspor"),
        ("Kasımpaşa", "Beşiktaş"),
        ("Kocaelispor", "Rizespor"),
        ("Konyaspor", "Galatasaray"),
        ("Trabzonspor", "Gaziantep FK")
    ],

    # 11
    [
        ("Alanyaspor", "Trabzonspor"),
        ("Beşiktaş", "Gençlerbirliği"),
        ("Çorumspor", "Fenerbahçe"),
        ("Eyüpspor", "Kocaelispor"),
        ("Galatasaray", "Amedspor"),
        ("Gaziantep FK", "Kasımpaşa"),
        ("Göztepe", "Başakşehir FK"),
        ("Rizespor", "Erzurumspor"),
        ("Samsunspor", "Konyaspor")
    ],

    # 12
    [
        ("Amedspor", "Rizespor"),
        ("Başakşehir FK", "Çorumspor"),
        ("Erzurumspor", "Göztepe"),
        ("Galatasaray", "Samsunspor"),
        ("Gençlerbirliği", "Gaziantep FK"),
        ("Kasımpaşa", "Alanyaspor"),
        ("Kocaelispor", "Fenerbahçe"),
        ("Konyaspor", "Beşiktaş"),
        ("Trabzonspor", "Eyüpspor")
    ],

    # 13
    [
        ("Alanyaspor", "Konyaspor"),
        ("Beşiktaş", "Galatasaray"),
        ("Çorumspor", "Kocaelispor"),
        ("Eyüpspor", "Başakşehir FK"),
        ("Fenerbahçe", "Erzurumspor"),
        ("Gaziantep FK", "Amedspor"),
        ("Göztepe", "Trabzonspor"),
        ("Rizespor", "Kasımpaşa"),
        ("Samsunspor", "Gençlerbirliği")
    ],

    # 14
    [
        ("Amedspor", "Alanyaspor"),
        ("Başakşehir FK", "Fenerbahçe"),
        ("Beşiktaş", "Samsunspor"),
        ("Erzurumspor", "Kocaelispor"),
        ("Galatasaray", "Rizespor"),
        ("Gençlerbirliği", "Eyüpspor"),
        ("Kasımpaşa", "Göztepe"),
        ("Konyaspor", "Gaziantep FK"),
        ("Trabzonspor", "Çorumspor")
    ],

    # 15
    [
        ("Alanyaspor", "Samsunspor"),
        ("Çorumspor", "Amedspor"),
        ("Erzurumspor", "Kasımpaşa"),
        ("Eyüpspor", "Galatasaray"),
        ("Fenerbahçe", "Trabzonspor"),
        ("Gaziantep FK", "Beşiktaş"),
        ("Göztepe", "Konyaspor"),
        ("Kocaelispor", "Gençlerbirliği"),
        ("Rizespor", "Başakşehir FK")
    ],

    # 16
    [
        ("Amedspor", "Göztepe"),
        ("Başakşehir FK", "Erzurumspor"),
        ("Beşiktaş", "Rizespor"),
        ("Galatasaray", "Alanyaspor"),
        ("Gençlerbirliği", "Çorumspor"),
        ("Kasımpaşa", "Fenerbahçe"),
        ("Konyaspor", "Eyüpspor"),
        ("Samsunspor", "Gaziantep FK"),
        ("Trabzonspor", "Kocaelispor")
    ],

    # 17
    [
        ("Alanyaspor", "Başakşehir FK"),
        ("Çorumspor", "Konyaspor"),
        ("Erzurumspor", "Trabzonspor"),
        ("Eyüpspor", "Samsunspor"),
        ("Fenerbahçe", "Amedspor"),
        ("Gaziantep FK", "Galatasaray"),
        ("Göztepe", "Beşiktaş"),
        ("Kocaelispor", "Kasımpaşa"),
        ("Rizespor", "Gençlerbirliği")
    ]
]



# 306 MAÇI OLUŞTUR


fiksturlar = []


for hafta, maclar in enumerate(
    ilk_devre,
    start=1
):

    for takim1, takim2 in maclar:

        fiksturlar.append({
            "hafta": hafta,
            "ev_sahibi": takim1,
            "deplasman": takim2,
            "skor": None
        })


for hafta, maclar in enumerate(
    ilk_devre,
    start=18
):

    for takim1, takim2 in maclar:

        fiksturlar.append({
            "hafta": hafta,
            "ev_sahibi": takim2,
            "deplasman": takim1,
            "skor": None
        })



# TFF TAKIM İSİMLERİ


TFF_TAKIM_ESLESMELERI = {

    "GALATASARAY A.Ş.": "Galatasaray",

    "ARCA ÇORUM FK": "Çorumspor",

    "TÜMOSAN KONYASPOR": "Konyaspor",

    "ÇAYKUR RİZESPOR A.Ş.": "Rizespor",

    "GAZİANTEP FUTBOL KULÜBÜ A.Ş.":
        "Gaziantep FK",

    "CORENDON ALANYASPOR":
        "Alanyaspor",

    "GENÇLERBİRLİĞİ":
        "Gençlerbirliği",

    "FENERBAHÇE A.Ş.":
        "Fenerbahçe",

    "KASIMPAŞA A.Ş.":
        "Kasımpaşa",

    "TRABZONSPOR A.Ş.":
        "Trabzonspor",

    "BEŞİKTAŞ A.Ş.":
        "Beşiktaş",

    "EYÜPSPOR":
        "Eyüpspor",

    "AMED SPORTİF FAALİYETLER":
        "Amedspor",

    "ERZURUMSPOR FK":
        "Erzurumspor",

    "İSTANBUL BAŞAKŞEHİR FK":
        "Başakşehir FK",

    "KOCAELİSPOR":
        "Kocaelispor",

    "SAMSUNSPOR A.Ş.":
        "Samsunspor",

    "GÖZTEPE A.Ş.":
        "Göztepe"
}



# TFF TAKIM ADINI DÜZELT


def takim_adi_duzelt(takim):

    takim = takim.strip().upper()

    if takim in TFF_TAKIM_ESLESMELERI:

        return TFF_TAKIM_ESLESMELERI[takim]

    return None





def tff_skorlarini_getir():

    adres = "https://www.tff.org/default.aspx?pageID=198"

    try:

        cevap = requests.get(
            adres,
            headers={
                "User-Agent":
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/151.0.0.0 Safari/537.36"
            },
            timeout=20
        )

        cevap.raise_for_status()

        soup = BeautifulSoup(
            cevap.content,
            "html.parser"
        )


        # SADECE FİKSTÜR LİSTESİNİ BUL


        metin = soup.get_text(
            " ",
            strip=True
        )

        # Gereksiz boşlukları temizle
        metin = re.sub(
            r"\s+",
            " ",
            metin
        )


        # 1.Hafta / 2.Hafta / ...


        hafta_eslesmeleri = list(
            re.finditer(
                r"(\d{1,2})\s*\.\s*Hafta",
                metin,
                re.IGNORECASE
            )
        )

        bulunan = []


        # HER HAFTAYI AYRI AYRI İNCELE


        for i, hafta_eslesme in enumerate(
            hafta_eslesmeleri
        ):

            hafta = int(
                hafta_eslesme.group(1)
            )

            # 34'ten büyük şeyleri alma
            if hafta < 1 or hafta > 34:
                continue

            baslangic = (
                hafta_eslesme.end()
            )

            if i + 1 < len(
                hafta_eslesmeleri
            ):

                bitis = (
                    hafta_eslesmeleri[
                        i + 1
                    ].start()
                )

            else:

                bitis = len(metin)

            hafta_metni = metin[
                baslangic:bitis
            ]


            # TAKIM İSİMLERİNİ REGEX'E HAZIRLA


            tff_isimleri = sorted(
                TFF_TAKIM_ESLESMELERI.keys(),
                key=len,
                reverse=True
            )

            takim_regex = "|".join(
                re.escape(x)
                for x in tff_isimleri
            )


            # MAÇ SATIRI
            #
            # Takım - skor - takım
            # veya
            # Takım skor - skor takım

            desen = re.compile(
                r"("
                + takim_regex +
                r")"
                r"\s+"
                r"(?:"
                r"(\d+)\s*-\s*(\d+)"
                r"\s+"
                r")?"
                r"("
                + takim_regex +
                r")"
            )

            mac_eslesmeleri = desen.finditer(
                hafta_metni
            )

            for mac in mac_eslesmeleri:

                takim1_tff = mac.group(1)
                gol1 = mac.group(2)
                gol2 = mac.group(3)
                takim2_tff = mac.group(4)

                takim1 = takim_adi_duzelt(
                    takim1_tff
                )

                takim2 = takim_adi_duzelt(
                    takim2_tff
                )

                if not takim1 or not takim2:
                    continue


                # SKOR


                if (
                    gol1 is not None
                    and
                    gol2 is not None
                ):

                    skor = (
                        f"{gol1} - {gol2}"
                    )

                else:

                    skor = None

                bulunan.append({

                    "hafta": hafta,

                    "ev_sahibi":
                        takim1,

                    "deplasman":
                        takim2,

                    "skor":
                        skor

                })

    
        # TEKRARLARI TEMİZLE
    

        benzersiz = {}

        for mac in bulunan:

            anahtar = (

                mac["hafta"],

                mac["ev_sahibi"],

                mac["deplasman"]

            )

            # Aynı maç tekrar geldiyse
            # skorlu olanı sakla

            if anahtar not in benzersiz:

                benzersiz[anahtar] = mac

            else:

                eski = benzersiz[anahtar]

                if (
                    eski["skor"] is None
                    and
                    mac["skor"] is not None
                ):

                    benzersiz[anahtar] = mac

        bulunan = list(
            benzersiz.values()
        )


        # KONTROL


        print()
        print(
            "================================"
        )

        print(
            "TFF'DEN BULUNAN MAÇLAR"
        )

        print(
            "Toplam:",
            len(bulunan)
        )

        print(
            "================================"
        )

        for mac in bulunan:

            print(
                mac["hafta"],
                ". Hafta:",
                mac["ev_sahibi"],
                "-",
                mac["deplasman"],
                ":",
                mac["skor"] or "-"
            )

        print(
            "================================"
        )

        return bulunan

    except Exception as hata:

        print(
            "TFF verisi alınamadı:",
            hata
        )

        return []



# 306 FİKSTÜRÜN SKORLARINI GÜNCELLE


def skorları_guncelle():

    tff_maclari = (
        tff_skorlarini_getir()
    )

    bulunan_skor = 0

    # Önce temizle
    for mac in fiksturlar:

        mac["skor"] = None


    # HAFTA + TAKIMLARLA EŞLEŞTİR


    for mac in fiksturlar:

        for tff_mac in tff_maclari:

            if (

                mac["hafta"]
                ==
                tff_mac["hafta"]

                and

                mac["ev_sahibi"]
                ==
                tff_mac["ev_sahibi"]

                and

                mac["deplasman"]
                ==
                tff_mac["deplasman"]

            ):

                if tff_mac["skor"]:

                    mac["skor"] = (
                        tff_mac["skor"]
                    )

                    bulunan_skor += 1

                break

    print()
    print(
        "================================"
    )

    print(
        "SKOR EŞLEŞTİRME"
    )

    print(
        "Toplam fikstür:",
        len(fiksturlar)
    )

    print(
        "Skoru bulunan maç:",
        bulunan_skor
    )

    print(
        "Skoru bulunmayan maç:",
        len(fiksturlar)
        - bulunan_skor
    )

    print(
        "================================"
    )



# ANA SAYFA


@app.route("/")
def ana_sayfa():

    return render_template(
        "index.html",
        takimlar=takimlar
    )



# FİKSTÜR

@app.route("/fikstur")
def fikstur():

    # TFF'den güncel skorları çek
    skorları_guncelle()

    return render_template(
        "fikstur.html",
        fiksturlar=fiksturlar
    )


# PUAN DURUMU

@app.route("/puan-durumu")
def puan_durumu():
    # TFF'den güncel skorları çek
    skorları_guncelle()

    puanlar = {}

    # Önce normal takım listesini oluştur
    for takim in takimlar:
        puanlar[takim] = {
            "oynanan": 0,
            "galibiyet": 0,
            "beraberlik": 0,
            "maglubiyet": 0,
            "attigi": 0,
            "yedigi": 0,
            "averaj": 0,
            "puan": 0
        }

    # Fikstürde olup takım listesinde olmayan takım varsa
    # otomatik olarak ekle
    for mac in fiksturlar:
        ev = mac["ev_sahibi"]
        deplasman = mac["deplasman"]

        if ev not in puanlar:
            puanlar[ev] = {
                "oynanan": 0,
                "galibiyet": 0,
                "beraberlik": 0,
                "maglubiyet": 0,
                "attigi": 0,
                "yedigi": 0,
                "averaj": 0,
                "puan": 0
            }

        if deplasman not in puanlar:
            puanlar[deplasman] = {
                "oynanan": 0,
                "galibiyet": 0,
                "beraberlik": 0,
                "maglubiyet": 0,
                "attigi": 0,
                "yedigi": 0,
                "averaj": 0,
                "puan": 0
            }

    # OYNANMIŞ MAÇLARI HESAPLA

    for mac in fiksturlar:

        if mac.get("skor") is None:
            continue

        skor = mac["skor"]

        try:
            gol1, gol2 = skor.split("-")
            gol1 = int(gol1.strip())
            gol2 = int(gol2.strip())
        except:
            continue

        ev = mac["ev_sahibi"]
        deplasman = mac["deplasman"]

        # Oynanan maç sayısı
        puanlar[ev]["oynanan"] += 1
        puanlar[deplasman]["oynanan"] += 1

        # Atılan goller
        puanlar[ev]["attigi"] += gol1
        puanlar[deplasman]["attigi"] += gol2

        # Yenilen goller
        puanlar[ev]["yedigi"] += gol2
        puanlar[deplasman]["yedigi"] += gol1

        # EV SAHİBİ KAZANDI
        if gol1 > gol2:

            puanlar[ev]["galibiyet"] += 1
            puanlar[ev]["puan"] += 3
            puanlar[deplasman]["maglubiyet"] += 1

        # DEPLASMAN KAZANDI
        elif gol2 > gol1:

            puanlar[deplasman]["galibiyet"] += 1
            puanlar[deplasman]["puan"] += 3
            puanlar[ev]["maglubiyet"] += 1

        # BERABERE
        else:

            puanlar[ev]["beraberlik"] += 1
            puanlar[deplasman]["beraberlik"] += 1
            puanlar[ev]["puan"] += 1
            puanlar[deplasman]["puan"] += 1

    # AVERAJ HESAPLA

    for takim in puanlar:
        puanlar[takim]["averaj"] = (
            puanlar[takim]["attigi"]
            -
            puanlar[takim]["yedigi"]
        )

    # SIRALAMA

    siralama = sorted(
        puanlar.keys(),
        key=lambda takim: (
            puanlar[takim]["puan"],
            puanlar[takim]["averaj"],
            puanlar[takim]["attigi"]
        ),
        reverse=True
    )

    return render_template(
        "puan_durumu.html",
        siralama=siralama,
        puanlar=puanlar
    )


# MAÇ SİMÜLASYONU


@app.route(
    "/mac",
    methods=["GET", "POST"]
)
def mac():

    sonuc = ""

    if request.method == "POST":

        takim1 = request.form["takim1"]

        takim2 = request.form["takim2"]

        if takim1 == takim2:

            sonuc = (
                "Aynı takım kendisiyle "
                "oynayamaz!"
            )

        else:

            gol1 = random.randint(
                0,
                5
            )

            gol2 = random.randint(
                0,
                5
            )

            if gol1 > gol2:

                kazanan = (
                    takim1 +
                    " kazandı!"
                )

            elif gol2 > gol1:

                kazanan = (
                    takim2 +
                    " kazandı!"
                )

            else:

                kazanan = "Berabere!"

            sonuc = (
                f"{takim1} "
                f"{gol1} - {gol2} "
                f"{takim2} | "
                f"{kazanan}"
            )

    return render_template(
        "mac.html",
        takimlar=takimlar,
        sonuc=sonuc
    )



# BAŞLAT


if __name__ == "__main__":

    print()
    print(
        "================================"
    )

    print(
        "2026-2027 TFF FİKSTÜRÜ"
    )

    print(
        "Toplam fikstür:",
        len(fiksturlar)
    )

    print(
        "================================"
    )

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

