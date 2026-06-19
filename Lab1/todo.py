import sys


def main():
    tasks = []
    next_id = 1

    print("TODO — aplicație de sarcini")
    print("Comenzi: add <task>, done <id>, delete <id>, list, exit")
    print()

    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            print()
            break

        if not line:
            continue

        cmd, *args = line.split(" ", 1)
        cmd = cmd.lower()

        if cmd == "exit":
            break

        elif cmd == "add":
            if not args:
                print("Eroare: specificați descrierea sarcinii.")
                continue
            tasks.append({"id": next_id, "desc": args[0], "done": False})
            print(f"Sarcina #{next_id} a fost adăugată.")
            next_id += 1

        elif cmd == "done":
            if not args or not args[0].isdigit():
                print("Eroare: specificați un ID valid.")
                continue
            tid = int(args[0])
            found = False
            for t in tasks:
                if t["id"] == tid:
                    if t["done"]:
                        print(f"Sarcina #{tid} este deja marcată ca rezolvată.")
                    else:
                        t["done"] = True
                        print(f"Sarcina #{tid} a fost marcată ca rezolvată.")
                    found = True
                    break
            if not found:
                print(f"Eroare: sarcina #{tid} nu există.")

        elif cmd == "delete":
            if not args or not args[0].isdigit():
                print("Eroare: specificați un ID valid.")
                continue
            tid = int(args[0])
            for i, t in enumerate(tasks):
                if t["id"] == tid:
                    tasks.pop(i)
                    print(f"Sarcina #{tid} a fost ștearsă.")
                    break
            else:
                print(f"Eroare: sarcina #{tid} nu există.")

        elif cmd == "list":
            if not tasks:
                print("Nu există sarcini.")
                continue
            print(f"{'ID':>3}  {'Stare':<6}  Descriere")
            print("-" * 40)
            for t in tasks:
                status = "✓ făcut" if t["done"] else "○ de făcut"
                print(f"{t['id']:>3}  {status:<8}  {t['desc']}")

        else:
            print(f"Comenză necunoscută: {cmd}")


if __name__ == "__main__":
    main()
