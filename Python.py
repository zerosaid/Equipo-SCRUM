import firebase_admin
from firebase_admin import credentials, db
from rich.console import Console
from rich.table import Table
from getpass import getpass
import json
import os

# Ruta del archivo de credenciales
CREDENCIALES_PATH = "credenciales.json"

# Verificar si el archivo de credenciales existe
if not os.path.exists(CREDENCIALES_PATH):
    credenciales_default = {
        "type": "service_account",
        "project_id": "tu-proyecto-id",
        "private_key_id": "xxxxx",
        "private_key": "-----BEGIN PRIVATE KEY-----\nXXXXXX\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-xxxxx@tu-proyecto-id.iam.gserviceaccount.com",
        "client_id": "xxxxx"
    }
    with open(CREDENCIALES_PATH, "w") as f:
        json.dump(credenciales_default, f, indent=4)
    print("[!] Se creó un archivo de credenciales por defecto. Reemplázalo con tus credenciales reales.")
    exit(1)

# URL de Firebase Realtime Database
DATABASE_URL = "https://scrumo-adf20-default-rtdb.firebaseio.com/"

# Inicializar Firebase
try:
    cred = credentials.Certificate(CREDENCIALES_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': DATABASE_URL
    })
except Exception as e:
    print(f"[!] Error al inicializar Firebase: {e}")
    exit(1)

console = Console()

# Función para registrar un usuario
def registrar_usuario():
    console.print("[bold green]Registro de Usuario[/bold green]")
    nombre = input("Nombre: ")
    usuario = input("Usuario: ")
    contraseña = getpass("Contraseña: ")
    ref = db.reference('usuarios')
    if ref.child(usuario).get():
        console.print("[red]El usuario ya existe.[/red]")
        return
    ref.child(usuario).set({
        'nombre': nombre,
        'contraseña': contraseña
    })
    console.print("[green]Registro exitoso![/green]")

# Función para iniciar sesión
def iniciar_sesion():
    console.print("[bold blue]Inicio de Sesión[/bold blue]")
    usuario = input("Usuario: ")
    contraseña = getpass("Contraseña: ")
    ref = db.reference(f'usuarios/{usuario}')
    datos = ref.get()
    if datos and datos.get('contraseña') == contraseña:
        console.print(f"[green]Bienvenido {datos['nombre']}![/green]")
        return usuario
    console.print("[red]Credenciales incorrectas.[/red]")
    return None

# Función para publicar un mensaje
def publicar_mensaje(usuario):
    console.print("[bold cyan]Publicar Mensaje[/bold cyan]")
    mensaje = input("Escribe tu mensaje: ")
    ref = db.reference('publicaciones')
    nueva_pub = ref.push()
    nueva_pub.set({
        'usuario': usuario,
        'mensaje': mensaje,
        'likes': 0,
        'comentarios': []
    })
    console.print("[green]Mensaje publicado![/green]")

# Función para dar like a una publicación
def dar_like():
    ver_publicaciones()
    pub_id = input("Ingresa el ID de la publicación para dar like: ")
    ref = db.reference(f'publicaciones/{pub_id}/likes')
    likes = ref.get() or 0
    ref.set(likes + 1)
    console.print("[green]¡Like agregado![/green]")

# Función para comentar en una publicación
def comentar():
    ver_publicaciones()
    pub_id = input("Ingresa el ID de la publicación para comentar: ")
    comentario = input("Escribe tu comentario: ")
    ref = db.reference(f'publicaciones/{pub_id}/comentarios')
    comentarios = ref.get() or []
    comentarios.append(comentario)
    ref.set(comentarios)
    console.print("[green]¡Comentario agregado![/green]")

# Función para ver publicaciones
def ver_publicaciones():
    console.print("[bold yellow]Publicaciones[/bold yellow]")
    ref = db.reference('publicaciones')
    publicaciones = ref.get()
    if not publicaciones:
        console.print("[red]No hay publicaciones aún.[/red]")
        return
    table = Table(title="Publicaciones")
    table.add_column("ID", style="white")
    table.add_column("Usuario", style="cyan")
    table.add_column("Mensaje", style="magenta")
    table.add_column("Likes", style="green")
    
    for key, datos in publicaciones.items():
        usuario = datos.get('usuario', 'Desconocido')
        mensaje = datos.get('mensaje', 'Sin mensaje')
        likes = str(datos.get('likes', 0))
        table.add_row(key, usuario, mensaje, likes)
    
    console.print(table)

# Menú principal
def menu():
    while True:
        console.print("\n[bold]1.[/] Registrar usuario")
        console.print("[bold]2.[/] Iniciar sesión")
        console.print("[bold]3.[/] Salir")
        opcion = input("Selecciona una opción: ")
        if opcion == '1':
            registrar_usuario()
        elif opcion == '2':
            usuario = iniciar_sesion()
            if usuario:
                menu_usuario(usuario)
        elif opcion == '3':
            break
        else:
            console.print("[red]Opción no válida.[/red]")

# Menú para usuarios autenticados
def menu_usuario(usuario):
    while True:
        console.print("\n[bold]1.[/] Publicar mensaje")
        console.print("[bold]2.[/] Ver publicaciones")
        console.print("[bold]3.[/] Dar like a una publicación")
        console.print("[bold]4.[/] Comentar una publicación")
        console.print("[bold]5.[/] Cerrar sesión")
        opcion = input("Selecciona una opción: ")
        if opcion == '1':
            publicar_mensaje(usuario)
        elif opcion == '2':
            ver_publicaciones()
        elif opcion == '3':
            dar_like()
        elif opcion == '4':
            comentar()
        elif opcion == '5':
            break
        else:
            console.print("[red]Opción no válida.[/red]")

if __name__ == "__main__":
    menu()