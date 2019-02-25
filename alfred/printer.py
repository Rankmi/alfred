
def print_issue(fields):
    print("-------------------------------------")
    print("[" + fields['project'] + "-" + fields['numberInProject']
          + "] Creado por: " + fields['reporter']
          + " el " + fields['created'])
    print(fields['summary'])
    print("[" + fields['State'] + "]", "[" + fields['Priority'] + "]")
    print("Puedes revisarlo aqui: https://rankmi.myjetbrains.com/youtrack/issue/"
          + fields['project'] + "-" + fields['numberInProject'])
    print("-------------------------------------")

    print("Descripcion:")
    print(fields['description'])
    print("-------------------------------------")

    print("Asignados:")
    for field in fields["assignees"]:
        print("- "+ field +":", fields["assignees"][field])
    print("-------------------------------------")
