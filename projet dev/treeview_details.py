# affichage d'un répertoire dans une fenêtre tkinter
# Antoine Jaccard
# Librairies importées: plattform, socket, psutil, getpass

import tkinter as tk
from tkinter import ttk # pour le treeview
from tkinter import filedialog # boite dialogue pour chercher un répertoire
from pathlib import Path # fonctions de répertoire
from datetime import datetime
import os
import platform
import socket
import psutil
import getpass


node_paths = {} #garder les chemins complets

# afficher des détails sur un fihcier


def display_file_info(event):
    global txt_name, txt_permissions, txt_modified, txt_size, txt_type, tkt_path
    selected_nodes = tree.selection() #fichier sélectionné
    if not selected_nodes:
        return
    file_path = node_paths[selected_nodes[0]]
    if not file_path.is_file():
        return
    file_info = file_path.stat()

    txt_name.delete("1.0", tk.END)
    txt_name.insert("1.0",file_path.name)
    txt_path.delete( "1.0", tk.END)
    txt_path.insert("1.0", file_path)
    txt_type.delete("1.0", tk.END)
    txt_type.insert("1.0", file_path.suffix or "sans extension")
    txt_size.delete("1.0", tk.END)
    txt_size.insert("1.0",f"{file_info.st_size} octets")
    txt_modified.delete("1.0", tk.END)
    txt_modified.insert("1.0", datetime.fromtimestamp(file_info.st_mtime))
    txt_permissions.delete("1.0", tk.END)
    if os.access(file_path, os.W_OK):
        txt_permissions.insert("1.0", "Read / Write")
    else:
        txt_permissions.insert("1.0", "Read Only")



# afficher un répertoire
def display_directory():
    tree.delete(*tree.get_children()) # vider le treeview
    node_paths.clear()
    root_folder = Path(filedialog.askdirectory()) # demander un répertoire

    # insérer le noeud racine (déjà ouvert)
    root_node = tree.insert("","end", text=f"📁 {root_folder.resolve()}",open=True )
    # garder l'info du chemin complet
    node_paths[root_node] = root_folder

    # appeler la recherche des noeuds enfants
    populate_tree(tree, root_node, root_folder)

    # afficher le tableau des node
    for node, path in node_paths.items():
        print(node, ":", path)

# recherche des noeuds enfants (récursif)
def populate_tree(tree, parent, folder):
    # pour tous les noeuds enfants du folder
    for item in folder.iterdir():
        item_name = f"📁 {item.name}" if item.is_dir() else f"🗎 {item.name}"
        node = tree.insert(parent, "end", text=item_name)
        node_paths[node] = item # garder l'info du chemin complet
        if item.is_dir():
            # cas d'un répertoire, rappeler les enfants de l'enfant (peut être long)
            populate_tree(tree,node,item)


def get_ip(): # foction générée par IA
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip=s.getsockname()[0]
    finally:
        s.close()
    return ip
def update_pc_info():
    global txt_cpu_used, txt_disk, txt_ram
    txt_cpu_used.delete("1.0",tk.END)
    txt_cpu_used.insert("1.0", f"{psutil.cpu_percent(interval=1)}%")
    txt_ram.delete("1.0", tk.END)
    txt_ram.insert("1.0", f"{psutil.virtual_memory().percent}%")
    txt_disk.delete("1.0", tk.END)
    txt_disk.insert("1.0",f"{psutil.disk_usage('/').percent}%")
# Fenêtre principale appelée window
window = tk.Tk()
window.title("File Explorer Antoine Jaccard")
window.geometry("1200x800")
window.configure(bg="lightblue")

# configuration de 2 colonnes dans window, la seconde plus large
window.columnconfigure(0, weight=1, uniform="col")
window.columnconfigure(1, weight=1, uniform="col")
window.columnconfigure(2,weight=1, uniform="col")
window.rowconfigure(0, weight=1) # une ligne (pour le treeview)
# création du menu principal
menu_bar = tk.Menu(window)
file_menu = tk.Menu(menu_bar, tearoff=False) # menu non détachable
file_menu.add_command(label="display directory", command=display_directory)
file_menu.add_separator()
file_menu.add_command(label="Ecrire Hello", command=lambda : print("hello"))
file_menu.add_command(label="Quit", command=window.destroy)
menu_bar.add_cascade(label="File", menu=file_menu) #ajouter File au menu
window.config(menu=menu_bar)

# création d'une frame pour le treeview
tree_frame = ttk.Frame(window)
tree_frame.grid(row=0, column=0, sticky="nsew") # placement s'étire dans toutes direction
tree_frame.rowconfigure(0, weight=1) # ligne du treeview
tree_frame.columnconfigure(0, weight=1) # première colonne de la frame
style = ttk.Style() #pour mettre un Style au ttkvieux
style.configure(
    "Treeview",
    font=("Arial", 14),
    rowheight=28,
    background="lightyellow", #couleur du fond
    #fieldbackground="lightgreen",
    foreground="green" #couleur d'écriture
)
# création du treeview et placement
tree = ttk.Treeview(tree_frame)
tree.heading("#0", text="Affichage d'un répertoire")
tree.grid(row=0, column=0, sticky="nsew") # placement, s'étire partout

# Quand on sélectionne un fichier, on appelle display_file_info
tree.bind("<<TreeviewSelect>>", display_file_info) 
# création de la frame de détails
details_frame = tk.Frame(window, bg="lightblue")
details_frame.grid(row=0, column=1, sticky="nsew")
details_frame.columnconfigure(0,weight=1)

lbl_name=tk.Label(details_frame,text="Name")
lbl_name.grid(row=0, column=0, sticky="ew")
txt_name=tk.Text(details_frame, height=2)
txt_name.grid(row=1, column=0, sticky="ew")
lbl_path=tk.Label(details_frame, text="Path")
lbl_path.grid(row=2, column=0, sticky="ew")
txt_path=tk.Text(details_frame, height=3)
txt_path.grid(row=3, column=0, sticky="ew")
lbl_type=tk.Label(details_frame, text="Type")
lbl_type.grid(row=4,column=0, sticky="ew")
txt_type=tk.Text(details_frame, height=1)
txt_type.grid(row=5, column=0, sticky="ew")
lbl_size=tk.Label(details_frame, text="Size")
lbl_size.grid(row=6,column=0, sticky="ew")
txt_size=tk.Text(details_frame, height=1)
txt_size.grid(row=7, column=0, sticky="ew")
lbl_modified=tk.Label(details_frame, text="Modified")
lbl_modified.grid(row=8,column=0, sticky="ew")
txt_modified=tk.Text(details_frame, height=1)
txt_modified.grid(row=9, column=0, sticky="ew")
lbl_permissions=tk.Label(details_frame, text="Permissions")
lbl_permissions.grid(row=10,column=0, sticky="ew")
txt_permissions=tk.Text(details_frame, height=1)
txt_permissions.grid(row=11, column=0, sticky="ew")

# création de la frame de personnalisation

perso_frame=tk.Frame(window, bg="Lightblue")
perso_frame.grid(row=0, column=2, sticky="nsew")
perso_frame.columnconfigure(0, weight=1)
# création des widgets d'informations dur l'ordinateur
lbl_information=tk.Label(perso_frame, text="Informations sur l'ordinateur")
lbl_information.grid(row=0, column=0, sticky="new")
lbl_user_name=tk.Label(perso_frame, text="Nom d'Utilisateur")
lbl_user_name.grid(row=1, column=0, sticky="ew")
txt_user_name=tk.Text(perso_frame, height=1)
txt_user_name.grid(row=2, column=0, sticky="ew")
lbl_computer_name = tk.Label(perso_frame, text="Nom de l'ordinateur")
lbl_computer_name.grid(row=3, column=0, sticky="ew")
txt_computer_name = tk.Text(perso_frame, height=1)
txt_computer_name.grid(row=4, column=0, sticky="ew")
lbl_ipconfig = tk.Label(perso_frame, text="Adresse IP")
lbl_ipconfig.grid(row=5, column=0, sticky="ew")
txt_ipconfig=tk.Text(perso_frame, height=1)
txt_ipconfig.grid(row=6, column=0, sticky="ew")
lbl_os = tk.Label(perso_frame, text="Système d'exploitation")
lbl_os.grid(row=7, column=0, sticky="ew")
txt_os = tk.Text(perso_frame, height=1)
txt_os.grid(row=8, column=0, sticky="ew")
lbl_os_version=tk.Label(perso_frame, text="Version du système d'exploitation")
lbl_os_version.grid(row=9, column=0, sticky="ew")
txt_os_version=tk.Text(perso_frame, height=1)
txt_os_version.grid(row=10, column=0, sticky="ew")
lbl_architecture=tk.Label(perso_frame, text="architechture")
lbl_architecture.grid(row=11, column=0, sticky="ew")
txt_architecture=tk.Text(perso_frame, height=1)
txt_architecture.grid(row=12, column=0, sticky="ew")
lbl_cpu = tk.Label(perso_frame, text="prosseceur")
lbl_cpu.grid(row=13, column=0, sticky="ew")
txt_cpu=tk.Text(perso_frame, height=2)
txt_cpu.grid(row=14, column=0, sticky="ew")
lbl_resources = tk.Label(perso_frame, text="utilisations des ressources")
lbl_resources.grid(row=15, column=0, sticky="ew")
lbl_cpu_used=tk.Label(perso_frame, text="utilisation du CPU")
lbl_cpu_used.grid(row=16, column=0, sticky="ew")
txt_cpu_used=tk.Text(perso_frame, height=1)
txt_cpu_used.grid(row=17, column=0, sticky="ew")
lbl_ram=tk.Label(perso_frame, text="Utilisation de la RAM")
lbl_ram.grid(row=18, column=0, sticky="ew")
txt_ram=tk.Text(perso_frame, height=1)
txt_ram.grid(row=19, column=0, sticky="ew")
lbl_disk=tk.Label(perso_frame,text="utilisation du disque")
lbl_disk.grid(row=20, column=0, sticky="ew")
txt_disk=tk.Text(perso_frame, height=1)
txt_disk.grid(row=21, column=0, sticky="ew")
btn_update_pc_info=tk.Button(perso_frame, text="mettre à jour l'utilisation des ressources", command=update_pc_info)
btn_update_pc_info.grid(row=22, column=0, sticky="ew")
# insertion des informations sur l'ordinateur utilisation de l'IA pour les librairies et les commandes autres que tkinter
# nom d'utilisateur
txt_user_name.insert("1.0",getpass.getuser())
# nom de l'ordinateur
txt_computer_name.insert("1.0", socket.gethostname())
# adresse IP
txt_ipconfig.insert("1.0", get_ip())
# OS
txt_os.insert("1.0", platform.system())
# version de l'OS
txt_os_version.insert("1.0", platform.release())
# Architechture
txt_architecture.insert("1.0", platform.architecture()[0])
# processeur
txt_cpu.insert("1.0", platform.processor())
# utilisation du CPU
txt_cpu_used.insert("1.0", f"{psutil.cpu_percent(interval=1)}%")
# Utilisation de la RAM
txt_ram.insert("1.0",f" {psutil.virtual_memory().percent} %")
# utilisation du disque
txt_disk.insert("1.0",f"{psutil.disk_usage('/').percent}%")
# lancement du prog principal
window.mainloop()