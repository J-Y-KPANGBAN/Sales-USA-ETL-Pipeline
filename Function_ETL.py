 #*****************start 02-Fev-2025 *******

import pandas as pd
import logging
import sqlalchemy
import glob

# =====================================================
# CONFIG LOGGING
# =====================================================
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%d-%m-%y %H:%M:%S',
    handlers=[
        logging.FileHandler(
            "C:/Users/Jean-YvesDG/Downloads/MES_PROJETS_REALISES/MES_PROJETS_REALISES/VENTE_USA/Fichier_logs.log",
            mode='a',
            encoding='utf-8'
        ),
        logging.StreamHandler()
    ]
)

log = logging.getLogger(__name__)

# =====================================================
# AUTOMATISATION FICHIERS CSV
# =====================================================
def generate_sales_file_paths(base_path):
    """Récupère tous les fichiers Sales_*.csv automatiquement"""
    return glob.glob(f"{base_path}Sales_*.csv")

# =====================================================
# EXTRACT
# =====================================================
def extract(file_list):
    """Lit tous les fichiers CSV et les concatène"""
    dfs = []
    for file in file_list:
        df = pd.read_csv(file)
        dfs.append(df)
        log.info(f"Lecture réussie : {file}")
    return pd.concat(dfs, ignore_index=True)

# =====================================================
# TRANSFORM
# =====================================================
def transform(data):
    """Nettoyage + création du Star Schema + IDs pour ventes"""

    # Normalisation colonnes
    data.columns = [
        "Order_ID",
        "Product",
        "Quantity_Ordered",
        "Price_Each",
        "Order_Date",
        "Purchase_Address"
    ]

    # Conversion types
    data["Order_ID"] = pd.to_numeric(data["Order_ID"], errors="coerce")
    data["Quantity_Ordered"] = pd.to_numeric(data["Quantity_Ordered"], errors="coerce")
    data["Price_Each"] = pd.to_numeric(data["Price_Each"], errors="coerce")
    data["Order_Date"] = pd.to_datetime(data["Order_Date"], format="%m/%d/%y %H:%M", errors="coerce")

    # Supprimer lignes invalides
    data.dropna(inplace=True)
    data = data.reset_index(drop=True)

    # =================================================
    # DIM DATE
    # =================================================
    dim_date = pd.DataFrame()
    dim_date["Order_Date"] = data["Order_Date"]
    dim_date["Date"] = data["Order_Date"].dt.date
    dim_date["Heure"] = data["Order_Date"].dt.time
    dim_date["Annee"] = data["Order_Date"].dt.year
    dim_date["Mois"] = data["Order_Date"].dt.month
    dim_date["Jour"] = data["Order_Date"].dt.day
    dim_date["ID_Date"] = range(1, len(dim_date)+1)

    # =================================================
    # DIM ADRESSE
    # =================================================
    split_addr = data["Purchase_Address"].str.split(",", expand=True)
    dim_adresse = pd.DataFrame()
    dim_adresse["Adresse"] = split_addr[0].str.strip()
    dim_adresse["Ville"] = split_addr[1].str.strip()
    dim_adresse["Etat"] = split_addr[2].str.strip().str.split(" ").str[0]
    dim_adresse["Code_postal"] = split_addr[2].str.strip().str.split(" ").str[1]
    dim_adresse["ID_Adresse"] = range(1, len(dim_adresse)+1)

    # =================================================
    # DIM COMMANDE
    # =================================================
    dim_commande = data[["Order_ID", "Product", "Quantity_Ordered"]].copy()
    dim_commande["ID_Commande"] = range(1, len(dim_commande)+1)

    # =================================================
    # TABLE VENTES
    # =================================================
    ventes = pd.DataFrame()
    ventes["ID_Vente"] = range(1, len(data)+1)
    ventes["ID_Commande"] = dim_commande["ID_Commande"]
    ventes["Order_Date"] = dim_date["Date"]
    ventes["Quantity_Ordered"] = data["Quantity_Ordered"]
    ventes["Price_Each"] = data["Price_Each"]
    ventes["Total_Revenue"] = ventes["Price_Each"] * ventes["Quantity_Ordered"]


    log.info("Transformation terminée (Star Schema + IDs ajoutés)")

    return dim_date, dim_adresse, dim_commande, ventes

# =====================================================
# LOAD
# =====================================================
def load_new_db(df, table_name):
    """Charge un DataFrame dans PostgreSQL"""
    engine = sqlalchemy.create_engine(
        "postgresql+psycopg2://postgres:ROOT@localhost:5432/sales_v4"
    )

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",  # remplace la table existante
        index=False
    )

    log.info(f"Table {table_name} chargée dans PostgreSQL")

    #*****************END 22-june-2025 *******