# affichage d'un répertoire dans une fenêtre tkinter
# Antoine Jaccard

import tkinter
import tkinter as tk
from tkinter import ttk # pour le treeview
from tkinter import filedialog # boite dialogue pour chercher un répertoire
from pathlib import Path # fonctions de répertoire
from datetime import datetime
import os

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


    print("Fichier:", file_path)
    print("Taille:", file_info.st_size, "octets")
    print("Date:", datetime.fromtimestamp(file_info.st_mtime))
    print("Type:", file_path.suffix or "sans extension")


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
#création de la frame de détails
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

#création de la frame de personnalisation

perso_frame=tk.Frame(window)
perso_frame.grid(row=0, column=2, sticky="nsew")
perso_frame.columnconfigure(0, weight=1)
perso_frame.rowconfigure(0, weight=1)
lbl_test=tk.Label(perso_frame, text="test")
lbl_test.pack()
# lancement du prog principal
window.mainloop()