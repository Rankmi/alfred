
def print_issue(issue):
    print("-------------------------------------")
    print("[" + issue.project + "-" + issue.numberInProject
          + "] Creado por: " + issue.reporter
          + " el " + issue.created)
    print(issue.summary)
    print("Puedes revisarlo aqui: https://rankmi.myjetbrains.com/youtrack/issue/"
          + issue.project + "-" + issue.numberInProject)
    print("-------------------------------------")

    print("Descripcion:")
    print(issue.description)
    print("-------------------------------------")