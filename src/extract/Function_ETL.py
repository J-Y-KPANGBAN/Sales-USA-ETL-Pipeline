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
def transform(data):

    # ================================
    # Nettoyage
    # ================================
    data.columns = [
        "Order_ID",
        "Product",
        "Quantity_Ordered",
        "Price_Each",
        "Order_Date",
        "Purchase_Address"
    ]

    data["Order_ID"] = pd.to_numeric(data["Order_ID"], errors="coerce")
    data["Quantity_Ordered"] = pd.to_numeric(data["Quantity_Ordered"], errors="coerce")
    data["Price_Each"] = pd.to_numeric(data["Price_Each"], errors="coerce")
    data["Order_Date"] = pd.to_datetime(data["Order_Date"], format="%m/%d/%y %H:%M", errors="coerce")

    data.dropna(inplace=True)
    data = data.reset_index(drop=True)

    # ================================
    # DIM PRODUCT
    # ================================
    dim_product = data[["Product", "Price_Each"]].drop_duplicates().reset_index(drop=True)
    dim_product["id_product"] = dim_product.index + 1

    # ================================
    # DIM DATE
    # ================================
    dim_date = pd.DataFrame()
    dim_date["order_date"] = data["Order_Date"]
    dim_date["year"] = data["Order_Date"].dt.year
    dim_date["month"] = data["Order_Date"].dt.month
    dim_date["day"] = data["Order_Date"].dt.day
    dim_date["hour"] = data["Order_Date"].dt.hour

    dim_date = dim_date.drop_duplicates().reset_index(drop=True)
    dim_date["id_date"] = dim_date.index + 1

    # ================================
    # DIM REGION
    # ================================
    split_addr = data["Purchase_Address"].str.split(",", expand=True)

    dim_region = pd.DataFrame()
    dim_region["street"] = split_addr[0].str.strip()
    dim_region["city"] = split_addr[1].str.strip()
    dim_region["state"] = split_addr[2].str.strip().str.split(" ").str[0]
    dim_region["zip_code"] = split_addr[2].str.strip().str.split(" ").str[1]

    dim_region = dim_region.drop_duplicates().reset_index(drop=True)
    dim_region["id_adresse"] = dim_region.index + 1

    # ================================
    # FACT TABLE
    # ================================

    # Merge avec produit
    fact_sales = data.merge(dim_product, on=["Product", "Price_Each"], how="left")

    # Merge avec date
    fact_sales = fact_sales.merge(dim_date, left_on="Order_Date", right_on="order_date", how="left")

    # Merge avec région
    temp_region = dim_region.copy()
    fact_sales["street"] = split_addr[0].str.strip()
    fact_sales["city"] = split_addr[1].str.strip()
    fact_sales["state"] = split_addr[2].str.strip().str.split(" ").str[0]
    fact_sales["zip_code"] = split_addr[2].str.strip().str.split(" ").str[1]

    fact_sales = fact_sales.merge(temp_region, on=["street", "city", "state", "zip_code"], how="left")

    # Construire fact
    fact_sales = fact_sales[[
        "Order_ID",
        "id_product",
        "id_date",
        "id_adresse",
        "Quantity_Ordered",
        "Price_Each"
    ]]

    fact_sales["id_fact"] = fact_sales.index + 1
    fact_sales["revenue"] = fact_sales["Quantity_Ordered"] * fact_sales["Price_Each"]

    fact_sales.rename(columns={
        "Quantity_Ordered": "quantity",
        "Price_Each": "price"
    }, inplace=True)

    log.info("Transformation OK (Star Schema propre)")

    return dim_date, dim_region, dim_product, fact_sales
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
#teste