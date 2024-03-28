import numpy as np
import pandas as pd
from pandas import DataFrame
import os


def append_data_singular(df: DataFrame) -> DataFrame:
    # Append new data to the existing data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    postals = pd.read_csv(os.path.join(current_dir, "src", "zipcodes.csv"))
    # Appends Municipality to the DataFrame
    postalcode = df["Postal Code"].values[
        0
    ]  # Access the "Postal Code" column correctly
    municipality = postals[postals["Postcode"] == postalcode]["Provincie"]
    # Appends Province to the DataFrame. Utilizes a smart fill method to fill in the province, if it is not found in the csv file.
    # Same as the above case.
    if not municipality.empty:
        df.loc[df["Postal Code"] == postalcode, "Province"] = municipality.values[0]
    return df


def convert_non_numeric_singular(df: DataFrame) -> DataFrame:
    building_state = {
        "TO_RESTORE": 0,
        "TO_RENOVATE": 1,
        "TO_BE_DONE_UP": 2,
        "GOOD": 3,
        "JUST_RENOVATED": 4,
        "AS_NEW": 5,
    }
    df["State of Building"] = (
        df["State of Building"].map(building_state).fillna(df["State of Building"])
    )

    energy_ratings = {
        "G": 8,
        "F": 7,
        "E": 6,
        "D": 5,
        "C": 4,
        "B": 3,
        "A": 2,
        "A+": 1,
        "A++": 0,
    }
    df["EPC"] = df["EPC"].map(energy_ratings).fillna(df["EPC"])

    kitchen_types = {
        "NOT_INSTALLED": 0,
        "USA_UNINSTALLED": 0,
        "SEMI_EQUIPPED": 1,
        "USA_SEMI_EQUIPPED": 1,
        "INSTALLED": 2,
        "USA_INSTALLED": 2,
        "HYPER_EQUIPPED": 3,
        "USA_HYPER_EQUIPPED": 3,
    }
    df["Kitchen Type"] = (
        df["Kitchen Type"].map(kitchen_types).fillna(df["Kitchen Type"])
    )

    if df["Type"].values[0] == "APARTMENT":
        df["Type_APARTMENT"] = 1
        df["Type_HOUSE"] = 0
    else:
        df["Type_APARTMENT"] = 0
        df["Type_HOUSE"] = 1
    df.drop("Type", axis=1, inplace=True)
    boolean = {False: 0, True: 1}
    df["Openfire"] = df["Openfire"].map(boolean).fillna(df["Openfire"])
    df["Furnished"] = df["Furnished"].map(boolean).fillna(df["Furnished"])
    return df


def fill_missing_values(df: DataFrame) -> DataFrame:
    features = [
        "Kitchen Type",
        "Garden Surface",
        "Habitable Surface",
        "Terrace Surface",
        "Furnished",
        "Openfire",
        "State of Building",
        "EPC",
        "Swimming Pool",
        "Type_APARTMENT",
        "Type_HOUSE",
        "Province_ANTWERPEN",
        "Province_BRUSSEL",
        "Province_HENEGOUWEN",
        "Province_LIMBURG",
        "Province_LUIK",
        "Province_LUXEMBURG",
        "Province_NAMEN",
        "Province_OOST-VLAANDEREN",
        "Province_VLAAMS-BRABANT",
        "Province_WAALS-BRABANT",
        "Province_WEST-VLAANDEREN",
        "Region_Brussels",
        "Region_Flanders",
        "Region_Wallonia",
    ]
    for feature in features:
        if feature not in df.columns:
            df[feature] = 0
    return df


def province_to_region(province):
    # This function takes a province as input and returns the region it belongs to
    if province in [
        "LUIK",
        "LIMBURG",
        "WAALS-BRABANT",
        "LUXEMBURG",
        "NAMEN",
        "HENEGOUWEN",
    ]:
        return "Wallonia"
    elif province == "BRUSSEL":
        return "Brussels"
    elif province in [
        "OOST-VLAANDEREN",
        "ANTWERPEN",
        "VLAAMS-BRABANT",
        "WEST-VLAANDEREN",
    ]:
        return "Flanders"
    else:
        return "Unknown"  # For any province value not listed above
