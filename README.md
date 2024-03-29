# Hermit Crab / Model Deployment (MVP)

[![forthebadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

By team **Hermit Crab** member, [Alice](https://www.linkedin.com/in/alice-edcm/)

## 📖 Description

This program uses FastAPI to create an API we can feed data into, and outputs the predicted property price, after using the prediction model included.
It also contains a Streamlit version to use in combination with the FastAPI for a frontend option, for those that are not familiar with using APIs.

## 🛠️ Setup & Installation

- create a new virtual environment by executing this command in your terminal:
  `python3 -m venv crab-api`
- activate the environment by executing this command in your terminal:
  `source crab-api/bin/activate`
- install the required dependencies by executing this command in your terminal:
  `pip install -r requirements.txt`

## 👩‍💻 Usage

To run the program, clone this repo on your local machine, navigate to its directory in your terminal, make sure you have first executed your requirements.txt, then execute:

```
uvicorn api.api:app
```

That will launch the API, if you wish to run the Frontend as well, you can run the following command:

```
cd streamlit
python3 streamlit.py
```

## 🗂️ File Structure

```
.
├── api/
│   ├── src/
│   │   └── zipcodes.csv
│   ├── api.py
│   ├── Dockerfile
│   ├── model_imputed.pkl
│   ├── predict.py
│   ├── preprocess.py
│   └── requirements.txt
├── streamlit/
│   ├── src/
│   │   └── zipcodes.csv
│   ├── api.py
│   ├── Dockerfile
│   ├── model_imputed.pkl
│   ├── predict.py
│   ├── preprocess.py
│   ├── requirements.txt
│   └── streamlit.py
├── .gitattributes
├── .gitignore
├── README.md
└── requirements.txt
```

## Program output

The output would technically be the possibility to host the model yourself to make a prediction of the price of a property in Belgium.
Otherwise, you may want to check out the [Frontend ](https://immo-eliza-hermitcrab-deployment.onrender.com/)and [Backend ](https://price-prediction-model-2.onrender.com)that were created from this project.

## 📂 Project background & timeline

This scraping project was done as part of the BeCode AI Bootcamp over the course of one week in March 2024.
It is the fourth and last phase of a team project to build a machine learning model that predicts the price of real estate properties in Belgium.

## Thank you for visiting our project page!

By team **Hermit Cra****b** member, [Alice](https://www.linkedin.com/in/alice-edcm/)

![crawl-along](https://biol326.files.wordpress.com/2018/04/andres-rivera-crab-gif-source.gif)
