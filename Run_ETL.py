import logging
from Function_ETL import (
    extract,
    transform,
    generate_sales_file_paths,
    load_new_db
)


# Configuration logging basique
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%d-%m-%y %H:%M:%S'
)

BASE_PATH = "C:/Users/Jean-YvesDG/Downloads/MES_PROJETS_REALISES/MES_PROJETS_REALISES/VENTE_USA/Donnees_csv_base/"

def run_etl():
    files = generate_sales_file_paths(BASE_PATH)
    raw_data = extract(files)

    dim_date, dim_adresse, dim_commande, ventes = transform(raw_data)

    load_new_db(dim_date, "dim_date")
    load_new_db(dim_adresse, "dim_adresse")
    load_new_db(dim_commande, "dim_commande")
    load_new_db(ventes, "ventes")

    logging.info("ETL terminé avec succès")

run_etl()
