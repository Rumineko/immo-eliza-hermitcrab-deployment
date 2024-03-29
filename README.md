# Hermit Crab / Model Deployment (MVP)

[![forthebadge made-with-python](https://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

![Charlie](https://cdn.discordapp.com/attachments/1209053035783913502/1214893521212018758/Charlie_100.png?ex=66167443&is=6603ff43&hm=ffa00a8503d1d0990689c5a027e7f6eecfa360c1da4b86534789054696740159&)

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

By team **Hermit Crab** member, [Alice](https://www.linkedin.com/in/alice-edcm/)

![Charlie](https://cdn.discordapp.com/attachments/1209053035783913502/1214893521212018758/Charlie_100.png?ex=66167443&is=6603ff43&hm=ffa00a8503d1d0990689c5a027e7f6eecfa360c1da4b86534789054696740159&)
