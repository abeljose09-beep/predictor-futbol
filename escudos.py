"""
Módulo de escudos — mapeado completo con los nombres exactos del dataset.
"""

import requests
from functools import lru_cache

ESCUDOS_CACHE = {
    # Premier League
    "Arsenal":          "https://www.thesportsdb.com/images/media/team/badge/a1af2i1557005128.png",
    "Aston Villa":      "https://www.thesportsdb.com/images/media/team/badge/sq4sss1547234388.png",
    "Bournemouth":      "https://www.thesportsdb.com/images/media/team/badge/vuturv1421791335.png",
    "Brentford":        "https://www.thesportsdb.com/images/media/team/badge/qfpvtq1656082851.png",
    "Brighton":         "https://www.thesportsdb.com/images/media/team/badge/svq3t51448813018.png",
    "Burnley":          "https://www.thesportsdb.com/images/media/team/badge/xpxpwy1421791341.png",
    "Chelsea":          "https://www.thesportsdb.com/images/media/team/badge/yvwvtu1448813215.png",
    "Crystal Palace":   "https://www.thesportsdb.com/images/media/team/badge/qpxtqp1547236143.png",
    "Everton":          "https://www.thesportsdb.com/images/media/team/badge/uuqyxy1421791381.png",
    "Fulham":           "https://www.thesportsdb.com/images/media/team/badge/xpwpwq1421791456.png",
    "Ipswich":          "https://www.thesportsdb.com/images/media/team/badge/rkqxtt1421791467.png",
    "Leicester":        "https://www.thesportsdb.com/images/media/team/badge/nstxwt1671280403.png",
    "Liverpool":        "https://www.thesportsdb.com/images/media/team/badge/xzqdr11598744967.png",
    "Luton":            "https://www.thesportsdb.com/images/media/team/badge/tttttt1421791473.png",
    "Man City":         "https://www.thesportsdb.com/images/media/team/badge/vwpizy1548859054.png",
    "Man United":       "https://www.thesportsdb.com/images/media/team/badge/xzqdr11548859378.png",
    "Newcastle":        "https://www.thesportsdb.com/images/media/team/badge/uvuswu1421791546.png",
    "Nott'm Forest":    "https://www.thesportsdb.com/images/media/team/badge/twwvxy1421791570.png",
    "Sheffield United": "https://www.thesportsdb.com/images/media/team/badge/xqxuts1421791588.png",
    "Southampton":      "https://www.thesportsdb.com/images/media/team/badge/uquyvx1421791501.png",
    "Tottenham":        "https://www.thesportsdb.com/images/media/team/badge/rwopxy1471630789.png",
    "West Ham":         "https://www.thesportsdb.com/images/media/team/badge/ya4rti1437743276.png",
    "Wolves":           "https://www.thesportsdb.com/images/media/team/badge/vwpizy1421791512.png",
    "Watford":          "https://www.thesportsdb.com/images/media/team/badge/uurrwx1421791507.png",
    "Norwich":          "https://www.thesportsdb.com/images/media/team/badge/xuxpyu1421791549.png",
    "Leeds":            "https://www.thesportsdb.com/images/media/team/badge/xqxqxv1421791469.png",

    # La Liga
    "Real Madrid":      "https://www.thesportsdb.com/images/media/team/badge/xvuwtw1473504001.png",
    "Barcelona":        "https://www.thesportsdb.com/images/media/team/badge/uyhbfe1612467562.png",
    "Ath Madrid":       "https://www.thesportsdb.com/images/media/team/badge/xzuzsv1421791228.png",
    "Sevilla":          "https://www.thesportsdb.com/images/media/team/badge/pstvwt1421791257.png",
    "Valencia":         "https://www.thesportsdb.com/images/media/team/badge/vwwqrx1421791263.png",
    "Villarreal":       "https://www.thesportsdb.com/images/media/team/badge/twxxuq1421791267.png",
    "Sociedad":         "https://www.thesportsdb.com/images/media/team/badge/xzszts1421791249.png",
    "Ath Bilbao":       "https://www.thesportsdb.com/images/media/team/badge/xwuqtq1421791222.png",
    "Betis":            "https://www.thesportsdb.com/images/media/team/badge/uturtu1421791246.png",
    "Osasuna":          "https://www.thesportsdb.com/images/media/team/badge/ttsyxu1421791238.png",
    "Girona":           "https://www.thesportsdb.com/images/media/team/badge/xstuts1660929741.png",
    "Las Palmas":       "https://www.thesportsdb.com/images/media/team/badge/b4z2me1697731321.png",
    "Mallorca":         "https://www.thesportsdb.com/images/media/team/badge/rtppwt1421791232.png",
    "Vallecano":        "https://www.thesportsdb.com/images/media/team/badge/twqyvx1421791244.png",
    "Celta":            "https://www.thesportsdb.com/images/media/team/badge/yvvtqs1421791226.png",
    "Getafe":           "https://www.thesportsdb.com/images/media/team/badge/uptvts1421791229.png",
    "Leganes":          "https://www.thesportsdb.com/images/media/team/badge/3gkzwd1729773526.png",
    "Espanol":          "https://www.thesportsdb.com/images/media/team/badge/qvwyvq1421791227.png",
    "Alaves":           "https://www.thesportsdb.com/images/media/team/badge/sqxttv1421791223.png",
    "Valladolid":       "https://www.thesportsdb.com/images/media/team/badge/vxuvru1421791264.png",
    "Almeria":          "https://www.thesportsdb.com/images/media/team/badge/xpspwv1421791224.png",
    "Cadiz":            "https://www.thesportsdb.com/images/media/team/badge/yxvxvy1421791225.png",
    "Granada":          "https://www.thesportsdb.com/images/media/team/badge/uxtvts1421791230.png",
    "Elche":            "https://www.thesportsdb.com/images/media/team/badge/rtspws1421791228.png",
    "Huesca":           "https://www.thesportsdb.com/images/media/team/badge/qwqyxt1421791231.png",
    "Eibar":            "https://www.thesportsdb.com/images/media/team/badge/sqwuvs1421791227.png",
    "Levante":          "https://www.thesportsdb.com/images/media/team/badge/uturts1421791233.png",
    "Oviedo":           "https://www.thesportsdb.com/images/media/team/badge/sqtsst1421791237.png",

    # Serie A
    "Juventus":         "https://www.thesportsdb.com/images/media/team/badge/xvuwtw1421791046.png",
    "Inter":            "https://www.thesportsdb.com/images/media/team/badge/puutws1421791043.png",
    "Milan":            "https://www.thesportsdb.com/images/media/team/badge/xpvpwv1421791040.png",
    "Napoli":           "https://www.thesportsdb.com/images/media/team/badge/xvspvs1421791055.png",
    "Roma":             "https://www.thesportsdb.com/images/media/team/badge/squuus1421791058.png",
    "Lazio":            "https://www.thesportsdb.com/images/media/team/badge/uqxsxq1421791048.png",
    "Atalanta":         "https://www.thesportsdb.com/images/media/team/badge/xzussz1421791035.png",
    "Fiorentina":       "https://www.thesportsdb.com/images/media/team/badge/rwqxpx1421791042.png",
    "Torino":           "https://www.thesportsdb.com/images/media/team/badge/xzustt1421791062.png",
    "Bologna":          "https://www.thesportsdb.com/images/media/team/badge/qvvxuy1421791037.png",
    "Udinese":          "https://www.thesportsdb.com/images/media/team/badge/uxuxuu1421791063.png",
    "Empoli":           "https://www.thesportsdb.com/images/media/team/badge/ssqvvt1421791041.png",
    "Sassuolo":         "https://www.thesportsdb.com/images/media/team/badge/sqwust1421791059.png",
    "Genoa":            "https://www.thesportsdb.com/images/media/team/badge/rwvpxp1421791042.png",
    "Lecce":            "https://www.thesportsdb.com/images/media/team/badge/rttwss1421791049.png",
    "Monza":            "https://www.thesportsdb.com/images/media/team/badge/8h2zik1659472875.png",
    "Verona":           "https://www.thesportsdb.com/images/media/team/badge/yxwxwx1421791065.png",
    "Salernitana":      "https://www.thesportsdb.com/images/media/team/badge/xssvts1421791058.png",
    "Spezia":           "https://www.thesportsdb.com/images/media/team/badge/ptpwts1421791060.png",
    "Venezia":          "https://www.thesportsdb.com/images/media/team/badge/ywvyvw1421791064.png",
    "Cagliari":         "https://www.thesportsdb.com/images/media/team/badge/svqvrs1421791038.png",
    "Frosinone":        "https://www.thesportsdb.com/images/media/team/badge/tqtvst1421791042.png",
    "Parma":            "https://www.thesportsdb.com/images/media/team/badge/xwxpwv1421791056.png",
    "Como":             "https://www.thesportsdb.com/images/media/team/badge/vqvust1421791039.png",
    "Cremonese":        "https://www.thesportsdb.com/images/media/team/badge/uwuvws1421791040.png",
    "Benevento":        "https://www.thesportsdb.com/images/media/team/badge/sqsrrs1421791036.png",
    "Crotone":          "https://www.thesportsdb.com/images/media/team/badge/sqstrs1421791040.png",
    "Sampdoria":        "https://www.thesportsdb.com/images/media/team/badge/sqstss1421791059.png",
    "Pisa":             "https://www.thesportsdb.com/images/media/team/badge/sqsvvs1421791057.png",

    # Bundesliga
    "Bayern Munich":    "https://www.thesportsdb.com/images/media/team/badge/uvuswu1421791844.png",
    "Dortmund":         "https://www.thesportsdb.com/images/media/team/badge/xqvvqx1421791846.png",
    "RB Leipzig":       "https://www.thesportsdb.com/images/media/team/badge/klq4bm1677840373.png",
    "Leverkusen":       "https://www.thesportsdb.com/images/media/team/badge/sqtwqv1421791850.png",
    "M'gladbach":       "https://www.thesportsdb.com/images/media/team/badge/sqtwqv1421791848.png",
    "Ein Frankfurt":    "https://www.thesportsdb.com/images/media/team/badge/upwqyq1421791853.png",
    "Wolfsburg":        "https://www.thesportsdb.com/images/media/team/badge/wqvvut1421791869.png",
    "Stuttgart":        "https://www.thesportsdb.com/images/media/team/badge/xtsqtq1421791864.png",
    "Freiburg":         "https://www.thesportsdb.com/images/media/team/badge/vsvust1421791854.png",
    "Hoffenheim":       "https://www.thesportsdb.com/images/media/team/badge/sqtwvt1421791856.png",
    "Mainz":            "https://www.thesportsdb.com/images/media/team/badge/xqwqwx1421791858.png",
    "Augsburg":         "https://www.thesportsdb.com/images/media/team/badge/sqtqst1421791843.png",
    "Union Berlin":     "https://www.thesportsdb.com/images/media/team/badge/c5b5dq1571244392.png",
    "Hertha":           "https://www.thesportsdb.com/images/media/team/badge/sqvwvt1421791855.png",
    "Werder Bremen":    "https://www.thesportsdb.com/images/media/team/badge/tsvswt1421791870.png",
    "Bochum":           "https://www.thesportsdb.com/images/media/team/badge/ssqvvr1421791844.png",
    "Schalke 04":       "https://www.thesportsdb.com/images/media/team/badge/twwwvv1421791862.png",
    "Hamburg":          "https://www.thesportsdb.com/images/media/team/badge/vsvqvt1421791855.png",
    "Heidenheim":       "https://www.thesportsdb.com/images/media/team/badge/9bqe591685009785.png",
    "St Pauli":         "https://www.thesportsdb.com/images/media/team/badge/rppsrp1421791863.png",
    "Holstein Kiel":    "https://www.thesportsdb.com/images/media/team/badge/d5f5pq1718978718.png",
    "Darmstadt":        "https://www.thesportsdb.com/images/media/team/badge/4f1zce1685010521.png",
    "Bielefeld":        "https://www.thesportsdb.com/images/media/team/badge/sqsrrs1421791844.png",
    "Greuther Furth":   "https://www.thesportsdb.com/images/media/team/badge/sqstrs1421791854.png",
    "FC Koln":          "https://www.thesportsdb.com/images/media/team/badge/sqstss1421791848.png",

    # Ligue 1
    "Paris SG":         "https://www.thesportsdb.com/images/media/team/badge/xvuwtw1421791647.png",
    "Lyon":             "https://www.thesportsdb.com/images/media/team/badge/puuvrs1421791640.png",
    "Marseille":        "https://www.thesportsdb.com/images/media/team/badge/xvstst1421791641.png",
    "Monaco":           "https://www.thesportsdb.com/images/media/team/badge/vtstpt1421791642.png",
    "Lille":            "https://www.thesportsdb.com/images/media/team/badge/qtstrt1421791638.png",
    "Nice":             "https://www.thesportsdb.com/images/media/team/badge/uxttus1421791643.png",
    "Rennes":           "https://www.thesportsdb.com/images/media/team/badge/sqtsst1421791649.png",
    "Lens":             "https://www.thesportsdb.com/images/media/team/badge/vuxuuv1421791637.png",
    "Strasbourg":       "https://www.thesportsdb.com/images/media/team/badge/xvuvtv1421791652.png",
    "Montpellier":      "https://www.thesportsdb.com/images/media/team/badge/rwsrsr1421791642.png",
    "Nantes":           "https://www.thesportsdb.com/images/media/team/badge/xvstts1421791643.png",
    "Reims":            "https://www.thesportsdb.com/images/media/team/badge/tsvtsv1421791648.png",
    "Brest":            "https://www.thesportsdb.com/images/media/team/badge/sqtsrs1421791632.png",
    "Lorient":          "https://www.thesportsdb.com/images/media/team/badge/xstuts1421791639.png",
    "Toulouse":         "https://www.thesportsdb.com/images/media/team/badge/xvuvuv1421791653.png",
    "Metz":             "https://www.thesportsdb.com/images/media/team/badge/xvstss1421791641.png",
    "Troyes":           "https://www.thesportsdb.com/images/media/team/badge/tvutus1421791654.png",
    "Angers":           "https://www.thesportsdb.com/images/media/team/badge/sqsrss1421791630.png",
    "Dijon":            "https://www.thesportsdb.com/images/media/team/badge/tstsst1421791634.png",
    "Clermont":         "https://www.thesportsdb.com/images/media/team/badge/1ngtnn1623146735.png",
    "Le Havre":         "https://www.thesportsdb.com/images/media/team/badge/e5n5hn1689444822.png",
    "St Etienne":       "https://www.thesportsdb.com/images/media/team/badge/xvstst1421791651.png",
    "Ajaccio":          "https://www.thesportsdb.com/images/media/team/badge/srrsrs1421791629.png",
    "Nimes":            "https://www.thesportsdb.com/images/media/team/badge/xvsuts1421791644.png",
    "Bordeaux":         "https://www.thesportsdb.com/images/media/team/badge/sqsrrs1421791631.png",
    "Paris FC":         "https://www.thesportsdb.com/images/media/team/badge/c1e1be1729856063.png",
    "Auxerre":          "https://www.thesportsdb.com/images/media/team/badge/sqrsrr1421791630.png",

    # Eredivisie
    "Ajax":             "https://www.thesportsdb.com/images/media/team/badge/sxpxpx1421791462.png",
    "PSV Eindhoven":    "https://www.thesportsdb.com/images/media/team/badge/xqxqxv1421791464.png",
    "Feyenoord":        "https://www.thesportsdb.com/images/media/team/badge/qvxvqw1421791462.png",
    "AZ Alkmaar":       "https://www.thesportsdb.com/images/media/team/badge/qvvqxv1421791461.png",
    "Twente":           "https://www.thesportsdb.com/images/media/team/badge/xvvqxv1421791465.png",
    "Utrecht":          "https://www.thesportsdb.com/images/media/team/badge/vvuxvx1421791465.png",
    "Heerenveen":       "https://www.thesportsdb.com/images/media/team/badge/sqtvut1421791462.png",
    "Groningen":        "https://www.thesportsdb.com/images/media/team/badge/sqtsst1421791462.png",
    "Heracles":         "https://www.thesportsdb.com/images/media/team/badge/sqsrrs1421791462.png",
    "Sparta Rotterdam": "https://www.thesportsdb.com/images/media/team/badge/sqstts1421791465.png",
    "Go Ahead Eagles":  "https://www.thesportsdb.com/images/media/team/badge/sqstss1421791462.png",
    "Almere City":      "https://www.thesportsdb.com/images/media/team/badge/e3w3dk1683711351.png",
    "NAC Breda":        "https://www.thesportsdb.com/images/media/team/badge/sqtsts1421791463.png",
    "Vitesse":          "https://www.thesportsdb.com/images/media/team/badge/vxuvuv1421791466.png",
    "For Sittard":      "https://www.thesportsdb.com/images/media/team/badge/ssqrrs1421791461.png",
    "Excelsior":        "https://www.thesportsdb.com/images/media/team/badge/sqsrss1421791461.png",
    "Nijmegen":         "https://www.thesportsdb.com/images/media/team/badge/sqstrs1421791463.png",
    "Waalwijk":         "https://www.thesportsdb.com/images/media/team/badge/sqstst1421791466.png",
    "Willem II":        "https://www.thesportsdb.com/images/media/team/badge/sqstts1421791466.png",
    "Volendam":         "https://www.thesportsdb.com/images/media/team/badge/sqsvvs1421791466.png",
    "Zwolle":           "https://www.thesportsdb.com/images/media/team/badge/sqsvts1421791467.png",
    "Telstar":          "https://www.thesportsdb.com/images/media/team/badge/sqsvst1421791464.png",

    # Portugal
    "Porto":            "https://www.thesportsdb.com/images/media/team/badge/upwxuv1421791413.png",
    "Benfica":          "https://www.thesportsdb.com/images/media/team/badge/qvtsts1421791407.png",
    "Sp Lisbon":        "https://www.thesportsdb.com/images/media/team/badge/vvwvtq1421791416.png",
    "Sp Braga":         "https://www.thesportsdb.com/images/media/team/badge/sqtsst1421791415.png",
    "Guimaraes":        "https://www.thesportsdb.com/images/media/team/badge/sqtsrs1421791409.png",
    "Boavista":         "https://www.thesportsdb.com/images/media/team/badge/sqsrrs1421791406.png",
    "Estoril":          "https://www.thesportsdb.com/images/media/team/badge/sqstrs1421791408.png",
    "Famalicao":        "https://www.thesportsdb.com/images/media/team/badge/sqstss1421791408.png",
    "Gil Vicente":      "https://www.thesportsdb.com/images/media/team/badge/sqsvvs1421791409.png",
    "Moreirense":       "https://www.thesportsdb.com/images/media/team/badge/sqsvts1421791411.png",
    "Casa Pia":         "https://www.thesportsdb.com/images/media/team/badge/sqsvst1421791407.png",
    "Chaves":           "https://www.thesportsdb.com/images/media/team/badge/sqsrst1421791407.png",
    "Rio Ave":          "https://www.thesportsdb.com/images/media/team/badge/sqstts1421791414.png",
    "Tondela":          "https://www.thesportsdb.com/images/media/team/badge/sqsvvt1421791416.png",
    "Portimonense":     "https://www.thesportsdb.com/images/media/team/badge/sqstss1421791413.png",
    "Nacional":         "https://www.thesportsdb.com/images/media/team/badge/sqstrs1421791411.png",
    "Arouca":           "https://www.thesportsdb.com/images/media/team/badge/sqsrrs1421791406.png",
    "Vizela":           "https://www.thesportsdb.com/images/media/team/badge/sqsvts1421791417.png",

    # Escocia
    "Celtic":           "https://www.thesportsdb.com/images/media/team/badge/tuxuux1421791569.png",
    "Rangers":          "https://www.thesportsdb.com/images/media/team/badge/sqwuqw1421791571.png",
    "Hearts":           "https://www.thesportsdb.com/images/media/team/badge/sqtsst1421791570.png",
    "Hibernian":        "https://www.thesportsdb.com/images/media/team/badge/sqtsrs1421791570.png",
    "Aberdeen":         "https://www.thesportsdb.com/images/media/team/badge/sqsrrs1421791568.png",
    "Dundee":           "https://www.thesportsdb.com/images/media/team/badge/sqsrss1421791569.png",
    "Dundee United":    "https://www.thesportsdb.com/images/media/team/badge/sqstrs1421791569.png",
    "Kilmarnock":       "https://www.thesportsdb.com/images/media/team/badge/sqstrs1421791570.png",
    "Motherwell":       "https://www.thesportsdb.com/images/media/team/badge/sqstss1421791570.png",
    "Ross County":      "https://www.thesportsdb.com/images/media/team/badge/sqsvvs1421791571.png",
    "St Johnstone":     "https://www.thesportsdb.com/images/media/team/badge/sqsvts1421791572.png",
    "St Mirren":        "https://www.thesportsdb.com/images/media/team/badge/sqsvst1421791572.png",
    "Livingston":       "https://www.thesportsdb.com/images/media/team/badge/sqstts1421791570.png",
    "Falkirk":          "https://www.thesportsdb.com/images/media/team/badge/sqstss1421791569.png",

    # Championship
    "Middlesbrough":    "https://www.thesportsdb.com/images/media/team/badge/sqtsst1421791536.png",
    "Coventry":         "https://www.thesportsdb.com/images/media/team/badge/sqsrrs1421791356.png",
    "Preston":          "https://www.thesportsdb.com/images/media/team/badge/sqstrs1421791582.png",
    "Hull":             "https://www.thesportsdb.com/images/media/team/badge/sqstss1421791464.png",
    "Millwall":         "https://www.thesportsdb.com/images/media/team/badge/sqsvvs1421791537.png",
    "Sheffield Weds":   "https://www.thesportsdb.com/images/media/team/badge/vwxvwx1421791590.png",
    "Blackburn":        "https://www.thesportsdb.com/images/media/team/badge/sqsrrs1421791327.png",
    "Swansea":          "https://www.thesportsdb.com/images/media/team/badge/sqsvts1421791606.png",
    "Cardiff":          "https://www.thesportsdb.com/images/media/team/badge/sqsrss1421791348.png",
    "Stoke":            "https://www.thesportsdb.com/images/media/team/badge/sqstrs1421791601.png",
    "West Brom":        "https://www.thesportsdb.com/images/media/team/badge/sqstts1421791618.png",
    "Bristol City":     "https://www.thesportsdb.com/images/media/team/badge/sqstst1421791337.png",
    "QPR":              "https://www.thesportsdb.com/images/media/team/badge/sqstss1421791583.png",
    "Plymouth":         "https://www.thesportsdb.com/images/media/team/badge/sqsvvs1421791579.png",
    "Birmingham":       "https://www.thesportsdb.com/images/media/team/badge/sqsrrs1421791324.png",
    "Sunderland":       "https://www.thesportsdb.com/images/media/team/badge/sqsvts1421791605.png",
    "Oxford":           "https://www.thesportsdb.com/images/media/team/badge/sqstrs1421791573.png",
    "Portsmouth":       "https://www.thesportsdb.com/images/media/team/badge/sqstss1421791580.png",
    "Derby":            "https://www.thesportsdb.com/images/media/team/badge/sqsrss1421791370.png",
    "Charlton":         "https://www.thesportsdb.com/images/media/team/badge/sqsrrs1421791350.png",
    "Wrexham":          "https://www.thesportsdb.com/images/media/team/badge/sqsvst1421791622.png",
}


@lru_cache(maxsize=256)
def buscar_escudo_api(nombre_equipo: str) -> str:
    """Busca escudo via TheSportsDB API como último recurso."""
    try:
        url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={nombre_equipo}"
        resp = requests.get(url, timeout=4)
        data = resp.json()
        if data.get("teams"):
            badge = data["teams"][0].get("strBadge", "")
            if badge:
                return badge + "/preview"
    except Exception:
        pass
    return ""


def get_escudo(nombre_equipo: str) -> str:
    """
    Retorna URL del escudo. Busca primero en cache local, luego en API.
    Si no encuentra nada, retorna string vacío (el HTML mostrará ⚽).
    """
    if nombre_equipo in ESCUDOS_CACHE:
        return ESCUDOS_CACHE[nombre_equipo]

    nombre_lower = nombre_equipo.lower()
    for equipo, url in ESCUDOS_CACHE.items():
        if equipo.lower() == nombre_lower:
            return url

    for equipo, url in ESCUDOS_CACHE.items():
        if nombre_lower in equipo.lower() or equipo.lower() in nombre_lower:
            return url

    return buscar_escudo_api(nombre_equipo)
