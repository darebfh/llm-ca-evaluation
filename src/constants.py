QAP_LIMIT = None
QA_ENDPOINT = "https://dmia.public.medinflab.ti.bfh.ch/answer"

QAP_DEFINITIONS_FILE = "data/input/qa_content.csv"
QAP_VARIATIONS_OUTPUT_FOLDER = "data/output/variations/"
QA_ANSWERS_OUTPUT_FOLDER = "data/output/qa_answers/"
EVALUATION_RESULTS_OUTPUT_FOLDER = "data/output/metrics/"
NEW_QUESTIONS_OUTPUT_FOLDER = "data/output/new_questions/"

SEED = 42


ROLES = {
    "high_literacy": {
        "description": "Du bist eine gebildete Patientin bzw. ein Patient mit hoher Gesundheitskompetenz. Du verwendest Fachbegriffe und drückst dich in komplizierter Sprache aus. Dir "
        "steht eine Mammographie bevor.",
        "example_question": "Was ist eine Mammographie?",
        "example_answer": """
1. Könnten Sie mir bitte exakt erläutern, was eine Mammografie ist und welche diagnostischen Prinzipien dieser bildgebenden Technik zugrunde liegen?
2. Würden Sie mir freundlicherweise eine umfassende Definition der Mammografie bereitstellen, einschließlich der angewandten Röntgenstrahlung und der damit verbundenen radiologischen Evaluation der weiblichen Brust?
3. Möchte ich Ihre Expertise in Anspruch nehmen, um eine erschöpfende Erklärung über die Mammografie zu erhalten, wobei insbesondere die Detektion von Veränderungen im Brustgewebe im Kontext dieser bildgebenden Modalität von Interesse ist.
4. Könnten Sie mir in möglichst detaillierter Form erörtern, was unter dem Terminus Mammografie zu verstehen ist, einschließlich der technologischen Aspekte und der präventiven Charakteristik, die diesem Verfahren im Bereich der Brustgesundheit zugeschrieben wird?
5. Ich würde gerne von Ihnen erfahren, inwiefern die Mammografie als radiologisches Verfahren zur Visualisierung der Brustanatomie und Identifikation potenzieller Pathologien dient, wobei eine klinische Kontextualisierung der diagnostischen Effizienz von Bedeutung ist.
6. Könnten Sie mir mit Ihrer profunden Fachkenntnis darlegen, welche spezifischen Protokolle und Methoden bei der Durchführung einer Mammografie Anwendung finden und wie diese in der präventiven Medizin zur Früherkennung von Brustkrankheiten beitragen?
7. Würde es Ihnen möglich sein, mir eine elaborierte Beschreibung bezüglich der Mammografie zu geben, indem Sie auf die strahlentechnischen Grundlagen, die Bildrekonstruktion sowie die klinische Validität dieses diagnostischen Instruments eingehen?
8. Könnten Sie mich bitte über die Mammografie in Kenntnis setzen, unter Berücksichtigung der räumlichen Auflösung, Kontrastempfindlichkeit und anderer radiologischer Parameter, die bei der Erfassung von pathologischen Veränderungen im Brustgewebe eine signifikante Rolle spielen?
9. Würden Sie mir bitte eine ausführliche Erläuterung darüber zukommen lassen, wie die Mammografie als modalitätsübergreifende Technik, die sowohl in der Screening- als auch Diagnostikphase Anwendung findet, einen Beitrag zur Prävention und Früherkennung von Brustkrankheiten leistet?
10. Ich wäre Ihnen außerordentlich dankbar, wenn Sie mir in fachlich fundierter Weise darlegen könnten, welchen Stellenwert die Mammografie in der gegenwärtigen evidenzbasierten Medizin einnimmt und wie ihre Ergebnisse zur weiteren Abklärung und Therapieplanung genutzt werden.""",
    },
    "low_literacy": {
        "description": "Du bist eine Patientin bzw. ein Patient mit geringer Gesundheitskompetenz und kennst "
        "dich im Gesundheitswesen kaum aus. Du verwendest einfache Sprache und verstehst komplizierte medizinische Begriffe nicht. Dir steht eine Mammographie bevor.",
        "example_question": "Was ist eine Mammographie?",
        "example_answer": """
1. Was bedeutet das Wort "Mammografie"? Ich hab das noch nie gehört.
2. Kannst du mir bitte erklären, was eine Mammografie ist? Ich kenne mich nicht so gut aus.
3. Ich habe demnächst eine Untersuchung namens Mammografie. Was passiert da eigentlich?
4. Kannst du mir auf einfache Weise sagen, was bei einer Mammografie gemacht wird?
5. Mir wurde gesagt, dass ich eine Mammografie machen soll. Was genau heißt das?
6. Kannst du mir bitte sagen, was ich mir unter einer Mammografie vorstellen soll?
7. Ich hab einen Termin für eine Mammografie. Was erwartet mich da?
8. Das Wort Mammografie ist für mich neu. Kannst du es mir bitte erklären, ohne Fachbegriffe zu verwenden?
9. Ich bin unsicher, was bei einer Mammografie passiert. Könntest du es mir in einfachen Worten erklären?
10. Habe demnächst eine Mammografie, aber weiß nicht, was das ist. Kannst du es mir so erklären, dass es leicht verständlich ist?
        """,
    },
    "poor_german": {
        "description": "Du bist eine Patientin bzw. ein Patient und lernst erst seit ein wenigen Wochen Deutsch. "
        "Deine Deutschkentnisse sind deswegen noch sehr gering. Du kannst nur einfache Sätze in gebrochenem Deutsch formulieren. Dir steht eine Mammographie bevor.",
        "example_question": "Was ist eine Mammographie?",
        "example_answer": """
1. Was machen Mammografie?
2. Ich verstehen nicht, Mammografie. Was das?
3. Können Sie erklären, bitte? Mammografie, was das bedeutet?
4. Ich hören über Mammografie. Was passieren da?
5. Entschuldigung, ich nicht verstehen. Mammografie, was es tun?
6. Kannst du mir erklären, was Mammografie ist?
7. Mammografie, das was? Können Sie einfach sagen?
8. Ich neu hier und wissen nicht. Was tun bei Mammografie?
9. Mammografie, wie funktioniert das? Ich unsicher.
10. Kannst du mir bitte sagen, was Mammografie bedeutet?
        """,
    },
}

TASK = (
    "Definiere anhand folgender Frage zehn möglichst unterschiedliche Versionen dieser Frage. Passe deine "
    "Wortwahl an deine Gesundheitskompetenz und dein Sprachniveau an. Gib jeweils nur die Frage getrennt "
    "durch einen Zeilenumbruch (\n) zurück."
)

TASK_NEW_QUESTIONS = (
    "Definiere anhand folgender Beschreibung zehn möglichst unterschiedliche Fragen an deinen Arzt bzw. deine Ärztin. Passe deine "
    "Wortwahl an deine Gesundheitskompetenz und dein Sprachniveau an. Gib jeweils nur die Frage getrennt "
    "durch einen Zeilenumbruch (\n) zurück."
)
