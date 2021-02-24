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

question_patterns = {
    "transition_eco":{
        "QUXVlc3Rpb246MTYw - Quel est aujourd'hui pour vous le problème concret le plus important dans le domaine de "
        "l'environnement ?": [1],
        'QUXVlc3Rpb246MTYx - Que faudrait-il faire selon vous pour apporter des réponses à ce problème ?': [2],
        'QUXVlc3Rpb246MTQ3 - Si oui, de quelle manière votre vie quotidienne est-elle touchée par le changement climatique ?': [1],
        "QUXVlc3Rpb246MTQ5 - Si oui, que faites-vous aujourd'hui pour protéger l'environnement et/ou que pourriez-vous faire ?": [2],
        "QUXVlc3Rpb246MTUw - Qu'est-ce qui pourrait vous inciter à changer vos comportements comme par exemple mieux entretenir et" \
        + "régler votre chauffage, modifier votre manière de conduire ou renoncer à prendre votre véhicule pour de très petites distances ?": [2],
        "QUXVlc3Rpb246MTUx - Quelles seraient pour vous les solutions les plus simples et les plus supportables" \
        + " sur un plan financier pour vous inciter à changer vos comportements ?": [2],
        'QUXVlc3Rpb246MTUz - Si oui, que faudrait-il faire pour vous convaincre ou vous aider à changer de mode de chauffage ?': [2],
        'QUXVlc3Rpb246MTU1 - Si oui, que faudrait-il faire pour vous convaincre ou vous aider à utiliser ces solutions alternatives ?': [2],
        'QUXVlc3Rpb246MjA3 - Si non, quelles sont les solutions de mobilité alternatives que vous souhaiteriez pouvoir utiliser ?': [2],
        'QUXVlc3Rpb246MTU3 - Et qui doit selon vous se charger de vous proposer ce type de solutions alternatives ?': [2],
        "QUXVlc3Rpb246MTU4 - Que pourrait faire la France pour faire partager ses choix en matière d'environnement au niveau européen et international ?": [2],
        "QUXVlc3Rpb246MTU5 - Y a-t-il d'autres points sur la transition écologique sur lesquels vous souhaiteriez vous exprimer ?": [1, 2]
    },
    "fiscalite_et_depense":{
        "QUXVlc3Rpb246MTYy - Quelles sont toutes les choses qui pourraient être faites pour améliorer l'information des citoyens sur l'utilisation des impôts ?":[2],
        "QUXVlc3Rpb246MTYz - Que faudrait-il faire pour rendre la fiscalité plus juste et plus efficace ?":[2],
        "QUXVlc3Rpb246MTY0 - Quels sont selon vous les impôts qu'il faut baisser en priorité ?":[3],
        "QUXVlc3Rpb246MjA2 - Afin de financer les dépenses sociales, faut-il selon vous...":[2],
        "QUXVlc3Rpb246MjA1 - S'il faut selon vous revoir les conditions d'attribution de certaines aides sociales, lesquelles doivent être concernées ?":[1,3],
        "QUXVlc3Rpb246MTY1 - Quels sont les domaines prioritaires où notre protection sociale doit être renforcée ?":[1,3],
        "QUXVlc3Rpb246MTY2 - Pour quelle(s) politique(s) publique(s) ou pour quels domaines d'action publique, seriez-vous prêts à payer plus d'impôts ?":[1],
        "QUXVlc3Rpb246MTY3 - Y a-t-il d'autres points sur les impôts et les dépenses sur lesquels vous souhaiteriez vous exprimer ?":[1,2]
    }
    ,"demo_et_citoy":{
        "QUXVlc3Rpb246MTA3 - En qui faites-vous le plus confiance pour vous faire représenter dans la société et pourquoi ?":[1,3],
        "QUXVlc3Rpb246MTA4 - En dehors des élus politiques, faut-il donner un rôle plus important aux associations et aux organisations syndicales et professionnelles ?":[3],
        "QUXVlc3Rpb246MTA5 - Si oui, à quel type d'associations ou d'organisations ? Et avec quel rôle ?":[2],
        "QUXVlc3Rpb246MTEw - Que faudrait-il faire pour renouer le lien entre les citoyens et les élus qui les représentent ?":[2],
        "QUXVlc3Rpb246MTEx - Le non-cumul des mandats instauré en 2017 pour les parlementaires (députés et sénateurs) est :":[3],
        "QUXVlc3Rpb246MTEy - Pourquoi ?":[1],
        "QUXVlc3Rpb246MTEz - Que faudrait-il faire pour mieux représenter les différentes sensibilités politiques ?":[2],
        "QUXVlc3Rpb246MTE1 - Si oui, lesquels ?":[3],
        "QUXVlc3Rpb246MTE2 - Que pensez-vous de la participation des citoyens aux élections et comment les inciter à y participer davantage ?":[1],
        "QUXVlc3Rpb246MTE4 - Si oui, de quelle manière ?":[2],
        "QUXVlc3Rpb246MTE5 - Que faudrait-il faire aujourd'hui pour mieux associer les citoyens aux grandes orientations et à la décision publique ? Comment mettre en place une démocratie plus participative ?":[2],
        "QUXVlc3Rpb246MTIx - Si oui, comment ?":[2],
        "QUXVlc3Rpb246MTIy - Que faudrait-il faire pour consulter plus directement les citoyens sur l'utilisation de l'argent public, par l'Etat et les collectivités ?":[2],
        "QUXVlc3Rpb246MTIz - Quel rôle nos assemblées, dont le Sénat et le Conseil économique, social et environnemental, doivent-elles jouer pour représenter nos territoires et la société civile ?":[3],
        "QUXVlc3Rpb246MTI1 - Si oui, comment ?":[2],
        "QUXVlc3Rpb246MTI3 - Que proposez-vous pour renforcer les principes de la laïcité dans le rapport entre l'Etat et les religions de notre pays ?":[2],
        "QUXVlc3Rpb246MTI4 - Comment garantir le respect par tous de la compréhension réciproque et des valeurs intangibles de la République ?":[2],
        "QUXVlc3Rpb246MTI5 - Que faudrait-il faire aujourd'hui pour renforcer l'engagement citoyen dans la société ?":[2],
        "QUXVlc3Rpb246MTMw - Quels sont les comportements civiques qu'il faut promouvoir dans notre vie quotidienne ou collective ?":[3],
        "QUXVlc3Rpb246MTMx - Que faudrait-il faire pour favoriser le développement de ces comportements civiques et par quels engagements concrets chacun peut-il y participer ?":[2],
        "QUXVlc3Rpb246MTMy - Que faudrait-il faire pour valoriser l'engagement citoyen dans les parcours de vie, dans les relations avec l'administration et les pouvoirs publics ?":[2],
        "QUXVlc3Rpb246MTMz - Quelles sont les incivilités les plus pénibles dans la vie quotidienne et que faudrait-il faire pour lutter contre ces incivilités ?":[3],
        "QUXVlc3Rpb246MTM0 - Que peuvent et doivent faire les pouvoirs publics pour répondre aux incivilités ?":[2],
        "QUXVlc3Rpb246MTM1 - Quel pourrait être le rôle de chacun pour faire reculer les incivilités dans la société ?":[2],
        "QUXVlc3Rpb246MTM2 - Quelles sont les discriminations les plus répandues dont vous êtes témoin ou victime ?":[1],
        "QUXVlc3Rpb246MTM3 - Que faudrait-il faire pour lutter contre ces discriminations et construire une société plus solidaire et plus tolérante ?":[2],
        "QUXVlc3Rpb246MTM5 - Si oui, lesquelles ?":[3],
        "QUXVlc3Rpb246MTQx - Que pensez-vous de la situation de l'immigration en France aujourd'hui et de la politique migratoire ? Quelles sont, selon vous, les critères à mettre en place pour définir la politique migratoire ?":[1,2],
        "QUXVlc3Rpb246MTQz - Que proposez-vous afin de répondre à ce défi qui va durer ?":[2],
        "QUXVlc3Rpb246MTQ0 - Quelles sont, selon vous, les modalités d'intégration les plus efficaces et les plus justes à mettre en place aujourd'hui dans la société ?":[3],
        "QUXVlc3Rpb246MTQ1 - Y a-t-il d'autres points sur la démocratie et la citoyenneté sur lesquels vous souhaiteriez vous exprimer ?":[1,2],
    },
    "org_etat_et_services_publics":{
        "QUXVlc3Rpb246MTY5 - Que pensez-vous de l'organisation de l'Etat et des administrations en France ? De quelle manière cette organisation devrait-elle évoluer ?":[1,2],
        "QUXVlc3Rpb246MTcx - Si oui, lesquelles ?":[3],
        "QUXVlc3Rpb246MTcy - Si non, quels types de services publics vous manquent dans votre territoire et qu'il est nécessaire de renforcer ?":[1,3],
        "QUXVlc3Rpb246MTc0 - Quels nouveaux services ou quelles démarches souhaitez-vous voir développées sur Internet en priorité ?":[3],
        "QUXVlc3Rpb246MTc3 - Quelles améliorations préconiseriez-vous ?":[2],
        "QUXVlc3Rpb246MTc4 - Quand vous pensez à l'évolution des services publics au cours des dernières années, quels sont ceux qui ont évolué de manière positive ?":[1],
        "QUXVlc3Rpb246MTc5 - Quels sont les services publics qui doivent le plus évoluer selon vous ?":[3],
        "QUXVlc3Rpb246MTgy - Si oui, à quelle occasion en avez-vous fait usage ?":[3],
        "QUXVlc3Rpb246MTgz - Pouvez-vous identifier des règles que l'administration vous a déjà demandé d'appliquer et que vous avez jugées inutiles ou trop complexes ?":[3],
        "QUXVlc3Rpb246MTg1 - Si oui, comment ?":[2],
        "QUXVlc3Rpb246MTg3 - Si oui, comment ?":[2],
        "QUXVlc3Rpb246MTg4 - Comment l'Etat et les collectivités territoriales peuvent-ils s'améliorer pour mieux répondre aux défis de nos territoires les plus en difficulté ?":[2],
        "QUXVlc3Rpb246MTkx - Si vous avez été amené à chercher une formation, pouvez-vous indiquer les éléments de "
        "satisfaction et/ou les difficultés rencontrés en précisant, pour chaque point, l'administration concernée "
        ":":[1,4],
        "QUXVlc3Rpb246MTky - Si vous avez été amené à scolariser votre enfant, pouvez-vous indiquer les éléments de "
        "satisfaction et/ou les difficultés rencontrés en précisant, pour chaque point, l'administration concernée "
        ":":[1,4],
        "QUXVlc3Rpb246MTkz - Si vous avez été amené à chercher un emploi, pouvez-vous indiquer les éléments de "
        "satisfaction et/ou les difficultés rencontrés en précisant, pour chaque point, l'administration concernée "
        ":":[1,4],
        "QUXVlc3Rpb246MTk0 - Si vous avez été amené à préparer votre retraite, pouvez-vous indiquer les éléments de "
        "satisfaction et/ou les difficultés rencontrés en précisant, pour chaque point, l'administration concernée "
        ":":[1,4],
        "QUXVlc3Rpb246MTk1 - Si vous avez été amené à demander un remboursement de soins de santé, pouvez-vous "
        "indiquer les éléments de satisfaction et/ou les difficultés rencontrés en précisant, pour chaque point, "
        "l'administration concernée :":[1,4],
        "QUXVlc3Rpb246MTk2 - Si vous avez été amené à faire une demande d'aide pour une situation de handicap, "
        "pouvez-vous indiquer les éléments de satisfaction et/ou les difficultés rencontrés en précisant, pour chaque "
        "point, l'administration concernée :":[1,4],
        "QUXVlc3Rpb246MTk4 - Si vous avez été amené à créer une entreprise, pouvez-vous indiquer les éléments de "
        "satisfaction et/ou les difficultés rencontrés en précisant, pour chaque point, l'administration concernée "
        ":":[1,4],
        "QUXVlc3Rpb246MTk5 - Si vous avez été amené à recruter du personnel, pouvez-vous indiquer les éléments de "
        "satisfaction et/ou les difficultés rencontrés en précisant, pour chaque point, l'administration concernée "
        ":":[1,4],
        "QUXVlc3Rpb246MjAw - Si vous avez été amené à former du personnel, pouvez-vous indiquer les éléments de "
        "satisfaction et/ou les difficultés rencontrés en précisant, pour chaque point, l'administration concernée "
        ":":[1,4],
        "QUXVlc3Rpb246MjAx - Si vous avez été amené à rémunérer du personnel, pouvez-vous indiquer les éléments de "
        "satisfaction et/ou les difficultés rencontrés en précisant, pour chaque point, l'administration concernée "
        ":":[1,4],
        "QUXVlc3Rpb246MjAy - Si vous avez été amené à mettre fin à votre activité, pouvez-vous indiquer les éléments "
        "de satisfaction et/ou les difficultés rencontrés en précisant, pour chaque point, l'administration concernée "
        ":":[1,4],
        "QUXVlc3Rpb246MjAz - Si vous avez été amené à recruter une personne portant un handicap, pouvez-vous indiquer "
        "les éléments de satisfaction et/ou les difficultés rencontrés en précisant, pour chaque point, "
        "l'administration concernée :":[1,4],
        "QUXVlc3Rpb246MTg5 - Y a-t-il d'autres points sur l'organisation de l'Etat et des services publics sur "
        "lesquels vous souhaiteriez vous exprimer ?":[1,2],
        }
}