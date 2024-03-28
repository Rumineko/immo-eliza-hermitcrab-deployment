from pandas.core.frame import DataFrame
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from pickle import load
from api.preprocess import (
    append_data_singular,
    convert_non_numeric_singular,
    fill_missing_values,
    province_to_region,
)
import os


def predict(df: DataFrame):
    ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False).set_output(
        transform="pandas"
    )
    current_dir = os.path.dirname(os.path.abspath(__file__))
    price_model = load(open(f"{current_dir}/model_imputed.pkl", "rb"))
    df["Postal Code"] = df["Postal_Code"]
    df.drop("Postal_Code", axis=1, inplace=True)
    df["Habitable Surface"] = df["Habitable_Surface"]
    df.drop("Habitable_Surface", axis=1, inplace=True)
    df["Kitchen Type"] = df["Kitchen_Type"]
    df.drop("Kitchen_Type", axis=1, inplace=True)
    df["Terrace Surface"] = df["Terrace_Surface"]
    df.drop("Terrace_Surface", axis=1, inplace=True)
    df["Garden Surface"] = df["Garden_Surface"]
    df.drop("Garden_Surface", axis=1, inplace=True)
    df["State of Building"] = df["State_of_Building"]
    df.drop("State_of_Building", axis=1, inplace=True)
    df1 = append_data_singular(df)
    df2 = convert_non_numeric_singular(df1)
    ohetransform = ohe.fit_transform(df2[["Province"]])
    df3 = pd.concat([df2, ohetransform], axis=1)
    df3["Region"] = df3["Province"].apply(province_to_region)
    ohetransform = ohe.fit_transform(df3[["Region"]])
    df3 = pd.concat([df3, ohetransform], axis=1).drop(["Region", "Province"], axis=1)
    df3.drop(["Postal Code"], axis=1, inplace=True)
    df4 = fill_missing_values(df3)
    list_final_features = [
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
    final_df = df4[list_final_features].copy()
    prediction = price_model.predict(final_df)
    return prediction
