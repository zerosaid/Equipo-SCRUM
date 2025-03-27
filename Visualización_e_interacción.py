import json
import os

DATA_FILE = "publicaciones.json"

def cargar_publicaciones():
    if os.path.exists(DATA_FILE):  
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def guardar_publicaciones(publicaciones):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(publicaciones, file, indent=4, ensure_ascii=False)

def ver_publicaciones():
    publicaciones = cargar_publicaciones()
    if not publicaciones:
        print("No hay publicaciones disponibles.\n")
        return

    print("\n--- Publicaciones ---")
    for idx, pub in enumerate(publicaciones):
        print(f"{idx + 1}. {pub['autor']}: {pub['contenido']} ({pub['likes']} Me gusta)")
        
        if "respuestas" in pub and pub["respuestas"]:
            for r_idx, respuesta in enumerate(pub["respuestas"]):
                print(f"   └ {r_idx + 1}. {respuesta['autor']}: {respuesta['contenido']} ({respuesta['likes']} Me gusta)")
    print()

def dar_me_gusta():
    publicaciones = cargar_publicaciones()
    if not publicaciones:
        print("No hay publicaciones para dar 'Me gusta'.\n")
        return

    ver_publicaciones()
    try:
        indice_pub = int(input("Selecciona el numero de la publicacion: ")) - 1
        if 0 <= indice_pub < len(publicaciones):
            opcion = input("Quieres dar 'Me gusta' a la (P)ublicacion o a una (R)espuesta? ").strip().lower()

            if opcion == "p":
                publicaciones[indice_pub]["likes"] += 1
                print("Has dado 'Me gusta' a la publicacion!\n")

            elif opcion == "r" and publicaciones[indice_pub]["respuestas"]:
                indice_resp = int(input("Selecciona el numero de la respuesta: ")) - 1
                if 0 <= indice_resp < len(publicaciones[indice_pub]["respuestas"]):
                    publicaciones[indice_pub]["respuestas"][indice_resp]["likes"] += 1
                    print("Has dado 'Me gusta' a la respuesta!\n")
                else:
                    print("Numero de respuesta invalido.\n")
            else:
                print("Opcion invalida o la publicacion no tiene respuestas.\n")

            guardar_publicaciones(publicaciones)
        else:
            print("Numero invalido.\n")
    except ValueError:
        print("Entrada no valida.\n")

def agregar_publicacion():
    publicaciones = cargar_publicaciones()
    autor = input("Ingresa tu nombre: ")
    contenido = input("Escribe tu publicacion: ")

    nueva_publicacion = {
        "autor": autor,
        "contenido": contenido,
        "likes": 0,
        "respuestas": []
    }
    
    publicaciones.append(nueva_publicacion)
    guardar_publicaciones(publicaciones)
    print("Publicacion agregada con exito.\n")

def responder_publicacion():
    publicaciones = cargar_publicaciones()
    if not publicaciones:
        print("No hay publicaciones para responder.\n")
        return

    ver_publicaciones()
    try:
        indice = int(input("Selecciona el numero de la publicacion para responder: ")) - 1
        if 0 <= indice < len(publicaciones):
            opcion = input("Quieres responder a la (P)ublicacion o a una (R)espuesta? ").strip().lower()

            if opcion == "p":
                autor = input("Ingresa tu nombre: ")
                contenido = input("Escribe tu respuesta: ")

                nueva_respuesta = {
                    "autor": autor,
                    "contenido": contenido,
                    "likes": 0
                }
                publicaciones[indice]["respuestas"].append(nueva_respuesta)
                print("Respuesta agregada con exito.\n")

            elif opcion == "r" and publicaciones[indice]["respuestas"]:
                indice_resp = int(input("Selecciona el numero de la respuesta a la que quieres responder: ")) - 1
                if 0 <= indice_resp < len(publicaciones[indice]["respuestas"]):
                    autor = input("Ingresa tu nombre: ")
                    contenido = input("Escribe tu respuesta: ")

                    nueva_respuesta = {
                        "autor": autor,
                        "contenido": contenido,
                        "likes": 0
                    }
                    publicaciones[indice]["respuestas"].insert(indice_resp + 1, nueva_respuesta)
                    print("Respuesta agregada con exito.\n")
                else:
                    print("Numero de respuesta invalido.\n")
            else:
                print("Opcion invalida o la publicacion no tiene respuestas.\n")

            guardar_publicaciones(publicaciones)
        else:
            print("Numero invalido.\n")
    except ValueError:
        print("Entrada no valida.\n")

def menu():
    while True:
        print("1. Ver Publicaciones")
        print("2. Dar 'Me gusta'")
        print("3. Agregar Publicacion")
        print("4. Responder Publicacion o Respuesta")
        print("5. Salir")

        opcion = input("Selecciona una opcion: ")

        if opcion == "1":
            ver_publicaciones()
        elif opcion == "2":
            dar_me_gusta()
        elif opcion == "3":
            agregar_publicacion()
        elif opcion == "4":
            responder_publicacion()
        elif opcion == "5":
            print("Saliendo :D")
            break
        else:
            print("Opcion no valida, intenta de nuevo.\n")

if __name__ == "__main__":
    menu()
