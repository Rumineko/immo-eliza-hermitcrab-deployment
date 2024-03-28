from __future__ import annotations
from fastapi import FastAPI, status
from pydantic import BaseModel, Field, ConfigDict
import pandas as pd
from api.predict import predict

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


@app.get("/")
async def root():
    return {"alive"}


@app.post("/predict")
async def price_prediction(input_parameters: Model):
    try:
        df = pd.DataFrame(
            [list(input_parameters.model_dump().values())],
            columns=input_parameters.dict().keys(),
        )
        prediction = predict(df)
        return {"predicted_price": prediction[0], "status_code": status.HTTP_200_OK}
    except Exception as e:
        return {"error": str(e), "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR}
