TEST_LIMIT = 3
QA_ENDPOINT = "https://dmia.public.medinflab.ti.bfh.ch/answer"

ROLES = {
    "high_literacy": "Du bist eine gebildete Patientin bzw. ein Patient mit hoher Gesundheitskompetenz. Dir "
    "steht eine Mammographie bevor.",
    "low_literacy": "Du bist eine Patientin bzw. ein Patient mit geringer Gesundheitskompetenz und kennst "
    "dich im Gesundheitswesen kaum aus. Dir steht eine Mammographie bevor.",
    "poor_german": "Du bist eine Patientin bzw. ein Patient und lernst erst seit ein wenigen Wochen Deutsch. "
    "Deine Deutschkentnisse sind deswegen noch sehr gering. Dir steht eine Mammographie bevor.",
}

TASK = (
    "Definiere anhand folgender Antwort zehn möglichst unterschiedliche Versionen einer Frage. Passe deine "
    "Wortwahl an deine Gesundheitskompetenz und deine Sprachniveau an. Gib jeweils nur die Formulierung getrennt "
    "durch einen Zeilenumbruch (\n) zurück."
)
