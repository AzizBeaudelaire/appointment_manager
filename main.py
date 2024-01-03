from interface import InterfaceUtilisateur
import sys

def main():
    try:
        if len(sys.argv) > 1:
            print("\033[91mErreur : Option pas encore opérationnelle\033[0m")
            sys.exit(1)
        
        # Modifiez cette ligne
        interface = InterfaceUtilisateur(fichier_db='rendez_vousdb')
        interface.menu_principal()
    except FileNotFoundError as fnfe:
        print("\033[91mErreur : Fichier introuvable - {}\033[0m".format(str(fnfe)))
        sys.exit(1)
    except Exception as e:
        print("\033[91mErreur lors de l'exécution du programme : {}\033[0m".format(str(e)))
        sys.exit(1)

if __name__ == "__main__":
    main()
