# coding = utf-8

from .textometry import load_lexique

question_meta_data = {
    "160": 'QUXVlc3Rpb246MTYw - Quel est aujourd\'hui pour vous le problème concret le plus important dans le domaine de l\'environnement ?',
    "161": 'QUXVlc3Rpb246MTYx - Que faudrait-il faire selon vous pour apporter des réponses à ce problème ?',
    "146": "QUXVlc3Rpb246MTQ2 - Diriez-vous que votre vie quotidienne est aujourd'hui touchée par le changement climatique ?",
    "147": "QUXVlc3Rpb246MTQ3 - Si oui, de quelle manière votre vie quotidienne est-elle touchée par le changement climatique ?",
    "148": "QUXVlc3Rpb246MTQ4 - À titre personnel, pensez-vous pouvoir contribuer à protéger l'environnement ?",
    "149": "QUXVlc3Rpb246MTQ5 - Si oui, que faites-vous aujourd'hui pour protéger l'environnement et/ou que pourriez-vous faire ?",
    "150": "QUXVlc3Rpb246MTUw - Qu'est-ce qui pourrait vous inciter à changer vos comportements comme par exemple mieux entretenir et régler votre chauffage, modifier votre manière de conduire ou renoncer à prendre votre véhicule pour de très petites distances ?",
    "151": "QUXVlc3Rpb246MTUx - Quelles seraient pour vous les solutions les plus simples et les plus supportables sur un plan financier pour vous inciter à changer vos comportements ?",
    "152": "QUXVlc3Rpb246MTUy - Par rapport à votre mode de chauffage actuel, pensez-vous qu'il existe des solutions alternatives plus écologiques ?",
    "153": "QUXVlc3Rpb246MTUz - Si oui, que faudrait-il faire pour vous convaincre ou vous aider à changer de mode de chauffage ?",
    "154": "QUXVlc3Rpb246MTU0 - Avez-vous pour vos déplacements quotidiens la possibilité de recourir à des solutions de mobilité alternatives à la voiture individuelle comme les transports en commun, le covoiturage, l'auto-partage, le transport à la demande, le vélo, etc. ?",
    "155": "QUXVlc3Rpb246MTU1 - Si oui, que faudrait-il faire pour vous convaincre ou vous aider à utiliser ces solutions alternatives ?",
    "207": "QUXVlc3Rpb246MjA3 - Si non, quelles sont les solutions de mobilité alternatives que vous souhaiteriez pouvoir utiliser ?",
    "157": "QUXVlc3Rpb246MTU3 - Et qui doit selon vous se charger de vous proposer ce type de solutions alternatives ?",
    "158": "QUXVlc3Rpb246MTU4 - Que pourrait faire la France pour faire partager ses choix en matière d'environnement au niveau européen et international ?",
    "159": "QUXVlc3Rpb246MTU5 - Y a-t-il d'autres points sur la transition écologique sur lesquels vous souhaiteriez vous exprimer ?"
}
question_code = {q:int(c) for c,q in question_meta_data.items()}
question_ids = list(question_code.values())


# Catégorie indiquant que la réponse traite de la thématique du transport
transport_cat = [
    "Transports doux ou moins nombreux",
    "Déménagement ou changement travail",
    "Télétravail",
    "Pistes cyclables",
    "Transports en commun meilleurs",
    "Transports en commun moins chers",
    "Taxer les gros pollueurs",
    "Commerce de proximité, circuit-court",
    "Transport commun gratuit",
    "Pistes cyclables, sécurisées",
    "Obligation, incitation au transport collectif",
    "Transport commun plus fiable, rapide",
    "Transport commun moins cher",
    "Télétravail, horaires flexibles",
    "Transport commun plus proche",
    "Transport commun plus fréquent",
    "Covoiturage, auto-partage, stop",
    "Transport commun plus sûr",
    "Parkings (vélo, auto) à proximité des gares",
    "Développer le réseau ferroviaire",
    "Ramassage scolaire",
    "Voiture électrique",
    "Marche à pied",
    "Train",
    "Vélo, trottinette (électrique)",
    "Voiture plus propre",
    "Voiture autonome",
    "Transports en commun (bus, tram)",
    "Voiture à hydrogène",
    "Voiture hybride",
    "Biocarburant (E85, ...)",
    "A Déplaçons-nous moins",
    "Transport fluvial",
    "Transport à la demande"
]


###### LEXICAL RESSOURCES DATA AND META-DATA
lexiques = {
    "transport_term": load_lexique("resources/lexiques/dico_transport.txt"),
    "change_verb":load_lexique("resources/lexiques/dico_verbe_changement.txt"),
    "deplacement_verb":load_lexique("resources/lexiques/dico_verbe_déplacement.txt"),
    "attribut":load_lexique("resources/lexiques/dico_attribut_transport.txt")
}

lexique_titles = {
    "transport_term":"Vocabulaire du Transport",
    "change_verb":"Verbes de changement",
    "deplacement_verb":"Verbes de déplacement",
    "attribut":"Attribut"
}

lexique_class_labels = {
    "transport_term":{"ML":"Moyen de locomotion","I":"Infrastructure","E":"Entreprise","P":"Pratiques","C":"Carburant","N":"Autres"},
    "change_verb":{"P":"Positif","N":"Negatif","M":"Neutre","C":"Création"},
    "deplacement_verb":None,# No class for now
    "attribut":{"financier":"Financier","quantité":"Quantité","temps":"Temps"}
}

lexiques_style_classe={
    "transport_term":"transport",
    "change_verb":"changement",
    "deplacement_verb":"deplacement",
    "attribut":"attribut"
}

analysed_questions  = {
    "transition_eco":[
    """QUXVlc3Rpb246MTYx - Que faudrait-il faire selon vous pour apporter des réponses à ce problème ?""",
    """QUXVlc3Rpb246MTQ3 - Si oui, de quelle manière votre vie quotidienne est-elle touchée par le changement climatique ?""",
    """QUXVlc3Rpb246MTUw - Qu'est-ce qui pourrait vous inciter à changer vos comportements comme par exemple mieux entretenir et régler votre chauffage, modifier votre manière de conduire ou renoncer à prendre votre véhicule pour de très petites distances ?""",
    """QUXVlc3Rpb246MTUx - Quelles seraient pour vous les solutions les plus simples et les plus supportables sur un plan financier pour vous inciter à changer vos comportements ?""",
    """QUXVlc3Rpb246MTU1 - Si oui, que faudrait-il faire pour vous convaincre ou vous aider à utiliser ces solutions alternatives ?""",
    """QUXVlc3Rpb246MjA3 - Si non, quelles sont les solutions de mobilité alternatives que vous souhaiteriez pouvoir utiliser ?"""
],
    "fiscalite_et_depense":[
"QUXVlc3Rpb246MTYy - Quelles sont toutes les choses qui pourraient être faites pour améliorer l'information des citoyens sur l'utilisation des impôts ?",
    'QUXVlc3Rpb246MTYz - Que faudrait-il faire pour rendre la fiscalité plus juste et plus efficace ?',
    "QUXVlc3Rpb246MTY0 - Quels sont selon vous les impôts qu'il faut baisser en priorité ?",
    'QUXVlc3Rpb246MjA2 - Afin de financer les dépenses sociales, faut-il selon vous...',
    "QUXVlc3Rpb246MjA1 - S'il faut selon vous revoir les conditions d'attribution de certaines aides sociales, lesquelles doivent être concernées ?",
    'QUXVlc3Rpb246MTY1 - Quels sont les domaines prioritaires où notre protection sociale doit être renforcée ?',
    "QUXVlc3Rpb246MTY2 - Pour quelle(s) politique(s) publique(s) ou pour quels domaines d'action publique, seriez-vous prêts à payer plus d'impôts ?",
    "QUXVlc3Rpb246MTY3 - Y a-t-il d'autres points sur les impôts et les dépenses sur lesquels vous souhaiteriez vous exprimer ?"
    ]
}