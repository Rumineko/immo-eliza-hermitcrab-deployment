from __future__ import annotations
from fastapi import FastAPI, status
import pickle
from pydantic import BaseModel, Field, ConfigDict
import pandas as pd
from preprocess import (
    append_data_singular,
    convert_non_numeric_singular,
    fill_missing_values,
    province_to_region,
)
from sklearn.preprocessing import OneHotEncoder

app = FastAPI()


class Model(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    Habitable_Surface: float = Field(alias="Habitable Surface")
    Kitchen_Type: str = Field(alias="Kitchen Type")
    Terrace_Surface: float = Field(alias="Terrace Surface")
    Garden_Surface: float = Field(alias="Garden Surface")
    EPC: str
    Type: str
    Postal_Code: int = Field(alias="Postal Code")
    Furnished: bool
    Openfire: bool
    State_of_Building: str = Field(alias="State of Building")


price_model = pickle.load(open("model_imputed.pkl", "rb"))

ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False).set_output(
    transform="pandas"
)


@app.post("/")
async def price_prediction(input_parameters: Model):
    try:
        df = pd.DataFrame(
            [list(input_parameters.model_dump().values())],
            columns=input_parameters.dict().keys(),
        )
        print(df)
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
        df3 = pd.concat([df3, ohetransform], axis=1).drop(
            ["Region", "Province"], axis=1
        )
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
        return {"predicted_price": prediction[0], "status_code": status.HTTP_200_OK}
    except Exception as e:
        return {"error": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}
