import numpy as np
import pandas as pd
from pandas import DataFrame
import os


def load_data(path: str) -> DataFrame:
    # Imports the data from the raw folder and returns as a DataFrame
    current_dir = os.path.dirname(os.path.abspath(__file__))
    newpath = os.path.join(current_dir, "data", "raw", path)
    df = pd.read_csv(newpath)
    df.drop_duplicates(subset="ID", inplace=True)
    df.set_index("ID", drop=True, inplace=True)
    return df


def fill_empty_data(df: DataFrame) -> DataFrame:
    # Uses Logical Reasoning to Fill in Empty Data
    df.loc[df["Swimming Pool"].isna(), "Swimming Pool"] = 0
    df.loc[df["Openfire"] == False, "Fireplace Count"] = 0
    df.loc[df["Openfire"] == True, "Fireplace Count"] = (
        df["Fireplace Count"].abs().fillna(1)
    )
    df.loc[df["Terrace"] == False, "Terrace Surface"] = 0
    df.loc[df["Garden Exists"] == False, "Garden Surface"] = 0
    return df


def append_data(df: DataFrame) -> DataFrame:
    # Append new data to the existing data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    postals = pd.read_csv(os.path.join(current_dir, "src", "zipcodes.csv"))
    for postalcode in df["Postal Code"]:
        # Appends Municipality to the DataFrame
        municipality = postals[postals["Postcode"] == postalcode]["Hoofdgemeente"]
        province = postals[postals["Postcode"] == postalcode]["Provincie"]
        # Appends Municipality to the DataFrame. Utilizes a smart fill method to fill in the province, if it is not found in the csv file.
        # It's useful in case there are properties in the dataset from another country, which we have encountered in the past.
        if not municipality.empty:
            df.loc[df["Postal Code"] == postalcode, "Municipality"] = (
                municipality.values[0]
            )
        # Appends Province to the DataFrame. Utilizes a smart fill method to fill in the province, if it is not found in the csv file.
        # Same as the above case.
        if not province.empty:
            df.loc[df["Postal Code"] == postalcode, "Province"] = province.values[0]
    return df


def append_data_singular(df: DataFrame) -> DataFrame:
    # Append new data to the existing data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    postals = pd.read_csv(os.path.join(current_dir, "src", "zipcodes.csv"))
    # Appends Municipality to the DataFrame
    postalcode = df["Postal Code"].values[
        0
    ]  # Access the "Postal Code" column correctly
    municipality = postals[postals["Postcode"] == postalcode]["Hoofdgemeente"]
    # Appends Province to the DataFrame. Utilizes a smart fill method to fill in the province, if it is not found in the csv file.
    # Same as the above case.
    if not municipality.empty:
        df.loc[df["Postal Code"] == postalcode, "Municipality"] = municipality.values[0]
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
        "Habitable Surface",
        "Kitchen Type",
        "Furnished",
        "Openfire",
        "Terrace Surface",
        "Garden Surface",
        "State of Building",
        "EPC",
        "Type_APARTMENT",
        "Type_HOUSE",
        "Municipality_AALST",
        "Municipality_AALTER",
        "Municipality_AARSCHOT",
        "Municipality_AARTSELAAR",
        "Municipality_AFFLIGEM",
        "Municipality_AISEAU-PRESLES",
        "Municipality_ALKEN",
        "Municipality_ALVERINGEM",
        "Municipality_AMAY",
        "Municipality_AMEL",
        "Municipality_ANDENNE",
        "Municipality_ANDERLECHT",
        "Municipality_ANDERLUES",
        "Municipality_ANHÉE",
        "Municipality_ANS",
        "Municipality_ANTHISNES",
        "Municipality_ANTOING",
        "Municipality_ANTWERPEN",
        "Municipality_ANZEGEM",
        "Municipality_ARDOOIE",
        "Municipality_ARENDONK",
        "Municipality_ARLON",
        "Municipality_AS",
        "Municipality_ASSE",
        "Municipality_ASSENEDE",
        "Municipality_ASSESSE",
        "Municipality_ATH",
        "Municipality_ATTERT",
        "Municipality_AUBANGE",
        "Municipality_AUBEL",
        "Municipality_AVELGEM",
        "Municipality_AWANS",
        "Municipality_AYWAILLE",
        "Municipality_BAARLE-HERTOG",
        "Municipality_BAELEN",
        "Municipality_BALEN",
        "Municipality_BASSENGE",
        "Municipality_BASTOGNE",
        "Municipality_BEAUMONT",
        "Municipality_BEAURAING",
        "Municipality_BEAUVECHAIN",
        "Municipality_BEERNEM",
        "Municipality_BEERSE",
        "Municipality_BEERSEL",
        "Municipality_BEGIJNENDIJK",
        "Municipality_BEKKEVOORT",
        "Municipality_BELOEIL",
        "Municipality_BERINGEN",
        "Municipality_BERLAAR",
        "Municipality_BERLARE",
        "Municipality_BERLOZ",
        "Municipality_BERNISSART",
        "Municipality_BERTEM",
        "Municipality_BERTOGNE",
        "Municipality_BERTRIX",
        "Municipality_BEVER",
        "Municipality_BEVEREN-WAAS",
        "Municipality_BEYNE-HEUSAY",
        "Municipality_BIERBEEK",
        "Municipality_BILZEN",
        "Municipality_BINCHE",
        "Municipality_BIÈVRE",
        "Municipality_BLANKENBERGE",
        "Municipality_BLÉGNY",
        "Municipality_BOCHOLT",
        "Municipality_BOECHOUT",
        "Municipality_BONHEIDEN",
        "Municipality_BOOM",
        "Municipality_BOORTMEERBEEK",
        "Municipality_BORGLOON",
        "Municipality_BORNEM",
        "Municipality_BORSBEEK",
        "Municipality_BOUILLON",
        "Municipality_BOUSSU",
        "Municipality_BOUTERSEM",
        "Municipality_BRAINE-L'ALLEUD",
        "Municipality_BRAINE-LE-CHÂTEAU",
        "Municipality_BRAINE-LE-COMTE",
        "Municipality_BRAIVES",
        "Municipality_BRAKEL",
        "Municipality_BRASSCHAAT",
        "Municipality_BRECHT",
        "Municipality_BREDENE",
        "Municipality_BREE",
        "Municipality_BRUGELETTE",
        "Municipality_BRUGGE",
        "Municipality_BRUNEHAUT",
        "Municipality_BRUSSEL",
        "Municipality_BUGGENHOUT",
        "Municipality_BURDINNE",
        "Municipality_BURG-REULAND",
        "Municipality_BUTGENBACH",
        "Municipality_BÜLLINGEN",
        "Municipality_CELLES",
        "Municipality_CERFONTAINE",
        "Municipality_CHAPELLE-LEZ-HERLAIMONT",
        "Municipality_CHARLEROI",
        "Municipality_CHASTRE",
        "Municipality_CHAUDFONTAINE",
        "Municipality_CHAUMONT-GISTOUX",
        "Municipality_CHIMAY",
        "Municipality_CHINY",
        "Municipality_CHIÈVRES",
        "Municipality_CHÂTELET",
        "Municipality_CINEY",
        "Municipality_CLAVIER",
        "Municipality_COLFONTAINE",
        "Municipality_COMBLAIN-AU-PONT",
        "Municipality_COURCELLES",
        "Municipality_COURT-SAINT-ETIENNE",
        "Municipality_COUVIN",
        "Municipality_CRISNÉE",
        "Municipality_DALHEM",
        "Municipality_DAMME",
        "Municipality_DAVERDISSE",
        "Municipality_DE HAAN",
        "Municipality_DE PANNE",
        "Municipality_DE PINTE",
        "Municipality_DEERLIJK",
        "Municipality_DEINZE",
        "Municipality_DENDERLEEUW",
        "Municipality_DENDERMONDE",
        "Municipality_DENTERGEM",
        "Municipality_DESSEL",
        "Municipality_DESTELBERGEN",
        "Municipality_DIEPENBEEK",
        "Municipality_DIEST",
        "Municipality_DIKSMUIDE",
        "Municipality_DILBEEK",
        "Municipality_DILSEN-STOKKEM",
        "Municipality_DINANT",
        "Municipality_DISON",
        "Municipality_DOISCHE",
        "Municipality_DONCEEL",
        "Municipality_DOUR",
        "Municipality_DROGENBOS",
        "Municipality_DUFFEL",
        "Municipality_DURBUY",
        "Municipality_ECAUSSINNES",
        "Municipality_EDEGEM",
        "Municipality_EDINGEN",
        "Municipality_EEKLO",
        "Municipality_EGHEZÉE",
        "Municipality_ELLEZELLES",
        "Municipality_ELSENE",
        "Municipality_ENGIS",
        "Municipality_EREZÉE",
        "Municipality_ERPE-MERE",
        "Municipality_ERQUELINNES",
        "Municipality_ESNEUX",
        "Municipality_ESSEN",
        "Municipality_ESTAIMPUIS",
        "Municipality_ESTINNES",
        "Municipality_ETALLE",
        "Municipality_ETTERBEEK",
        "Municipality_EUPEN",
        "Municipality_EVERE",
        "Municipality_EVERGEM",
        "Municipality_FAIMES",
        "Municipality_FARCIENNES",
        "Municipality_FAUVILLERS",
        "Municipality_FERNELMONT",
        "Municipality_FERRIÈRES",
        "Municipality_FEXHE-LE-HAUT-CLOCHER",
        "Municipality_FLEURUS",
        "Municipality_FLOREFFE",
        "Municipality_FLORENNES",
        "Municipality_FLORENVILLE",
        "Municipality_FLÉMALLE",
        "Municipality_FLÉRON",
        "Municipality_FONTAINE-L'EVÊQUE",
        "Municipality_FOSSES-LA-VILLE",
        "Municipality_FRAMERIES",
        "Municipality_FRASNES-LEZ-ANVAING",
        "Municipality_FROIDCHAPELLE",
        "Municipality_GALMAARDEN",
        "Municipality_GANSHOREN",
        "Municipality_GAVERE",
        "Municipality_GEDINNE",
        "Municipality_GEEL",
        "Municipality_GEER",
        "Municipality_GEETBETS",
        "Municipality_GEMBLOUX",
        "Municipality_GENAPPE",
        "Municipality_GENK",
        "Municipality_GENT",
        "Municipality_GERAARDSBERGEN",
        "Municipality_GERPINNES",
        "Municipality_GESVES",
        "Municipality_GINGELOM",
        "Municipality_GISTEL",
        "Municipality_GLABBEEK",
        "Municipality_GOOIK",
        "Municipality_GOUVY",
        "Municipality_GREZ-DOICEAU",
        "Municipality_GRIMBERGEN",
        "Municipality_GROBBENDONK",
        "Municipality_GRÂCE-HOLLOGNE",
        "Municipality_HAACHT",
        "Municipality_HAALTERT",
        "Municipality_HABAY",
        "Municipality_HALEN",
        "Municipality_HALLE",
        "Municipality_HAM",
        "Municipality_HAM-SUR-HEURE",
        "Municipality_HAMME",
        "Municipality_HAMOIR",
        "Municipality_HAMOIS",
        "Municipality_HAMONT-ACHEL",
        "Municipality_HANNUT",
        "Municipality_HARELBEKE",
        "Municipality_HASSELT",
        "Municipality_HASTIÈRE",
        "Municipality_HAVELANGE",
        "Municipality_HECHTEL-EKSEL",
        "Municipality_HEERS",
        "Municipality_HEIST-OP-DEN-BERG",
        "Municipality_HEMIKSEM",
        "Municipality_HENSIES",
        "Municipality_HERBEUMONT",
        "Municipality_HERENT",
        "Municipality_HERENTALS",
        "Municipality_HERENTHOUT",
        "Municipality_HERK-DE-STAD",
        "Municipality_HERNE",
        "Municipality_HERSELT",
        "Municipality_HERSTAL",
        "Municipality_HERVE",
        "Municipality_HERZELE",
        "Municipality_HEUSDEN-ZOLDER",
        "Municipality_HEUVELLAND",
        "Municipality_HOEGAARDEN",
        "Municipality_HOEILAART",
        "Municipality_HOESELT",
        "Municipality_HOLSBEEK",
        "Municipality_HONNELLES",
        "Municipality_HOOGLEDE",
        "Municipality_HOOGSTRATEN",
        "Municipality_HOREBEKE",
        "Municipality_HOTTON",
        "Municipality_HOUFFALIZE",
        "Municipality_HOUTHALEN-HELCHTEREN",
        "Municipality_HOUTHULST",
        "Municipality_HOUYET",
        "Municipality_HOVE",
        "Municipality_HULDENBERG",
        "Municipality_HULSHOUT",
        "Municipality_HUY",
        "Municipality_HÉLÉCINE",
        "Municipality_HÉRON",
        "Municipality_ICHTEGEM",
        "Municipality_IEPER",
        "Municipality_INCOURT",
        "Municipality_INGELMUNSTER",
        "Municipality_ITTRE",
        "Municipality_IZEGEM",
        "Municipality_JABBEKE",
        "Municipality_JALHAY",
        "Municipality_JEMEPPE-SUR-SAMBRE",
        "Municipality_JETTE",
        "Municipality_JODOIGNE",
        "Municipality_JUPRELLE",
        "Municipality_JURBISE",
        "Municipality_KALMTHOUT",
        "Municipality_KAMPENHOUT",
        "Municipality_KAPELLE-OP-DEN-BOS",
        "Municipality_KAPELLEN",
        "Municipality_KAPRIJKE",
        "Municipality_KASTERLEE",
        "Municipality_KEERBERGEN",
        "Municipality_KELMIS",
        "Municipality_KINROOI",
        "Municipality_KLUISBERGEN",
        "Municipality_KNOKKE-HEIST",
        "Municipality_KOEKELARE",
        "Municipality_KOEKELBERG",
        "Municipality_KOKSIJDE",
        "Municipality_KOMEN-WAASTEN",
        "Municipality_KONTICH",
        "Municipality_KORTEMARK",
        "Municipality_KORTENAKEN",
        "Municipality_KORTENBERG",
        "Municipality_KORTESSEM",
        "Municipality_KORTRIJK",
        "Municipality_KRAAINEM",
        "Municipality_KRUIBEKE",
        "Municipality_KRUISEM",
        "Municipality_KUURNE",
        "Municipality_LA BRUYÈRE",
        "Municipality_LA HULPE",
        "Municipality_LA LOUVIÈRE",
        "Municipality_LA ROCHE-EN-ARDENNE",
        "Municipality_LAAKDAL",
        "Municipality_LAARNE",
        "Municipality_LANAKEN",
        "Municipality_LANDEN",
        "Municipality_LANGEMARK-POELKAPELLE",
        "Municipality_LASNE",
        "Municipality_LE ROEULX",
        "Municipality_LEBBEKE",
        "Municipality_LEDE",
        "Municipality_LEDEGEM",
        "Municipality_LENDELEDE",
        "Municipality_LENNIK",
        "Municipality_LENS",
        "Municipality_LEOPOLDSBURG",
        "Municipality_LES BONS VILLERS",
        "Municipality_LESSINES",
        "Municipality_LEUVEN",
        "Municipality_LEUZE-EN-HAINAUT",
        "Municipality_LIBIN",
        "Municipality_LIBRAMONT-CHEVIGNY",
        "Municipality_LICHTERVELDE",
        "Municipality_LIEDEKERKE",
        "Municipality_LIER",
        "Municipality_LIERDE",
        "Municipality_LIERNEUX",
        "Municipality_LIEVEGEM",
        "Municipality_LILLE",
        "Municipality_LIMBOURG",
        "Municipality_LINCENT",
        "Municipality_LINKEBEEK",
        "Municipality_LINT",
        "Municipality_LINTER",
        "Municipality_LIÈGE",
        "Municipality_LO-RENINGE",
        "Municipality_LOBBES",
        "Municipality_LOCHRISTI",
        "Municipality_LOKEREN",
        "Municipality_LOMMEL",
        "Municipality_LONDERZEEL",
        "Municipality_LONTZEN",
        "Municipality_LUBBEEK",
        "Municipality_LUMMEN",
        "Municipality_LÉGLISE",
        "Municipality_MAARKEDAL",
        "Municipality_MAASEIK",
        "Municipality_MAASMECHELEN",
        "Municipality_MACHELEN",
        "Municipality_MALDEGEM",
        "Municipality_MALLE",
        "Municipality_MALMEDY",
        "Municipality_MANAGE",
        "Municipality_MANHAY",
        "Municipality_MARCHE-EN-FAMENNE",
        "Municipality_MARCHIN",
        "Municipality_MARTELANGE",
        "Municipality_MECHELEN",
        "Municipality_MEERHOUT",
        "Municipality_MEISE",
        "Municipality_MEIX-DEVANT-VIRTON",
        "Municipality_MELLE",
        "Municipality_MENEN",
        "Municipality_MERBES-LE-CHÂTEAU",
        "Municipality_MERCHTEM",
        "Municipality_MERELBEKE",
        "Municipality_MERKSPLAS",
        "Municipality_MESEN",
        "Municipality_MESSANCY",
        "Municipality_METTET",
        "Municipality_MEULEBEKE",
        "Municipality_MIDDELKERKE",
        "Municipality_MODAVE",
        "Municipality_MOERBEKE-WAAS",
        "Municipality_MOESKROEN",
        "Municipality_MOL",
        "Municipality_MOMIGNIES",
        "Municipality_MONS",
        "Municipality_MONT-DE-L'ENCLUS",
        "Municipality_MONT-SAINT-GUIBERT",
        "Municipality_MONTIGNY-LE-TILLEUL",
        "Municipality_MOORSLEDE",
        "Municipality_MORLANWELZ",
        "Municipality_MORTSEL",
        "Municipality_MUSSON",
        "Municipality_NAMUR",
        "Municipality_NANDRIN",
        "Municipality_NASSOGNE",
        "Municipality_NAZARETH",
        "Municipality_NEUFCHÂTEAU",
        "Municipality_NEUPRÉ",
        "Municipality_NIEL",
        "Municipality_NIEUWERKERKEN",
        "Municipality_NIEUWPOORT",
        "Municipality_NIJLEN",
        "Municipality_NINOVE",
        "Municipality_NIVELLES",
        "Municipality_OHEY",
        "Municipality_OLEN",
        "Municipality_OLNE",
        "Municipality_ONHAYE",
        "Municipality_OOSTENDE",
        "Municipality_OOSTERZELE",
        "Municipality_OOSTKAMP",
        "Municipality_OOSTROZEBEKE",
        "Municipality_OPWIJK",
        "Municipality_OREYE",
        "Municipality_ORP-JAUCHE",
        "Municipality_OTTIGNIES-LOUVAIN-LA-NEUVE",
        "Municipality_OUD-HEVERLEE",
        "Municipality_OUD-TURNHOUT",
        "Municipality_OUDENAARDE",
        "Municipality_OUDENBURG",
        "Municipality_OUDERGEM",
        "Municipality_OUDSBERGEN",
        "Municipality_OUFFET",
        "Municipality_OUPEYE",
        "Municipality_OVERIJSE",
        "Municipality_PALISEUL",
        "Municipality_PECQ",
        "Municipality_PEER",
        "Municipality_PELT",
        "Municipality_PEPINGEN",
        "Municipality_PEPINSTER",
        "Municipality_PERWEZ",
        "Municipality_PHILIPPEVILLE",
        "Municipality_PITTEM",
        "Municipality_PLOMBIÈRES",
        "Municipality_PONT-À-CELLES",
        "Municipality_POPERINGE",
        "Municipality_PROFONDEVILLE",
        "Municipality_PUTTE",
        "Municipality_PUURS-SINT-AMANDS",
        "Municipality_PÉRUWELZ",
        "Municipality_QUAREGNON",
        "Municipality_QUIÉVRAIN",
        "Municipality_QUÉVY",
        "Municipality_RAEREN",
        "Municipality_RAMILLIES",
        "Municipality_RANST",
        "Municipality_RAVELS",
        "Municipality_REBECQ",
        "Municipality_REMICOURT",
        "Municipality_RENDEUX",
        "Municipality_RETIE",
        "Municipality_RIEMST",
        "Municipality_RIJKEVORSEL",
        "Municipality_RIXENSART",
        "Municipality_ROCHEFORT",
        "Municipality_ROESELARE",
        "Municipality_RONSE",
        "Municipality_ROOSDAAL",
        "Municipality_ROTSELAAR",
        "Municipality_ROUVROY",
        "Municipality_RUISELEDE",
        "Municipality_RUMES",
        "Municipality_RUMST",
        "Municipality_SAINT-GEORGES-SUR-MEUSE",
        "Municipality_SAINT-GHISLAIN",
        "Municipality_SAINT-HUBERT",
        "Municipality_SAINT-LÉGER",
        "Municipality_SAINT-NICOLAS",
        "Municipality_SAINTE-ODE",
        "Municipality_SAMBREVILLE",
        "Municipality_SANKT-VITH",
        "Municipality_SCHAARBEEK",
        "Municipality_SCHELLE",
        "Municipality_SCHERPENHEUVEL-ZICHEM",
        "Municipality_SCHILDE",
        "Municipality_SCHOTEN",
        "Municipality_SENEFFE",
        "Municipality_SERAING",
        "Municipality_SILLY",
        "Municipality_SINT-AGATHA-BERCHEM",
        "Municipality_SINT-GENESIUS-RODE",
        "Municipality_SINT-GILLIS",
        "Municipality_SINT-GILLIS-WAAS",
        "Municipality_SINT-JANS-MOLENBEEK",
        "Municipality_SINT-JOOST-TEN-NODE",
        "Municipality_SINT-KATELIJNE-WAVER",
        "Municipality_SINT-LAMBRECHTS-WOLUWE",
        "Municipality_SINT-LAUREINS",
        "Municipality_SINT-LIEVENS-HOUTEM",
        "Municipality_SINT-MARTENS-LATEM",
        "Municipality_SINT-NIKLAAS",
        "Municipality_SINT-PIETERS-LEEUW",
        "Municipality_SINT-PIETERS-WOLUWE",
        "Municipality_SINT-TRUIDEN",
        "Municipality_SIVRY-RANCE",
        "Municipality_SOIGNIES",
        "Municipality_SOMBREFFE",
        "Municipality_SOMME-LEUZE",
        "Municipality_SOUMAGNE",
        "Municipality_SPA",
        "Municipality_SPIERE-HELKIJN",
        "Municipality_SPRIMONT",
        "Municipality_STABROEK",
        "Municipality_STADEN",
        "Municipality_STAVELOT",
        "Municipality_STEENOKKERZEEL",
        "Municipality_STEKENE",
        "Municipality_STOUMONT",
        "Municipality_TELLIN",
        "Municipality_TEMSE",
        "Municipality_TENNEVILLE",
        "Municipality_TERNAT",
        "Municipality_TERVUREN",
        "Municipality_TESSENDERLO",
        "Municipality_THEUX",
        "Municipality_THIMISTER-CLERMONT",
        "Municipality_THUIN",
        "Municipality_TIELT",
        "Municipality_TIELT-WINGE",
        "Municipality_TIENEN",
        "Municipality_TINLOT",
        "Municipality_TINTIGNY",
        "Municipality_TONGEREN",
        "Municipality_TORHOUT",
        "Municipality_TOURNAI",
        "Municipality_TREMELO",
        "Municipality_TROIS-PONTS",
        "Municipality_TROOZ",
        "Municipality_TUBIZE",
        "Municipality_TURNHOUT",
        "Municipality_UKKEL",
        "Municipality_VAUX-SUR-SÛRE",
        "Municipality_VERLAINE",
        "Municipality_VERVIERS",
        "Municipality_VEURNE",
        "Municipality_VIELSALM",
        "Municipality_VILLERS-LA-VILLE",
        "Municipality_VILLERS-LE-BOUILLET",
        "Municipality_VILVOORDE",
        "Municipality_VIROINVAL",
        "Municipality_VIRTON",
        "Municipality_VISÉ",
        "Municipality_VLETEREN",
        "Municipality_VLOESBERG",
        "Municipality_VOEREN",
        "Municipality_VORSELAAR",
        "Municipality_VORST",
        "Municipality_VOSSELAAR",
        "Municipality_VRESSE-SUR-SEMOIS",
        "Municipality_WAASMUNSTER",
        "Municipality_WACHTEBEKE",
        "Municipality_WALCOURT",
        "Municipality_WALHAIN",
        "Municipality_WANZE",
        "Municipality_WAREGEM",
        "Municipality_WAREMME",
        "Municipality_WASSEIGES",
        "Municipality_WATERLOO",
        "Municipality_WATERMAAL-BOSVOORDE",
        "Municipality_WAVRE",
        "Municipality_WEISMES",
        "Municipality_WELKENRAEDT",
        "Municipality_WELLEN",
        "Municipality_WELLIN",
        "Municipality_WEMMEL",
        "Municipality_WERVIK",
        "Municipality_WESTERLO",
        "Municipality_WETTEREN",
        "Municipality_WEVELGEM",
        "Municipality_WEZEMBEEK-OPPEM",
        "Municipality_WICHELEN",
        "Municipality_WIELSBEKE",
        "Municipality_WIJNEGEM",
        "Municipality_WILLEBROEK",
        "Municipality_WINGENE",
        "Municipality_WOMMELGEM",
        "Municipality_WORTEGEM-PETEGEM",
        "Municipality_WUUSTWEZEL",
        "Municipality_YVOIR",
        "Municipality_ZANDHOVEN",
        "Municipality_ZAVENTEM",
        "Municipality_ZEDELGEM",
        "Municipality_ZELE",
        "Municipality_ZELZATE",
        "Municipality_ZEMST",
        "Municipality_ZOERSEL",
        "Municipality_ZONHOVEN",
        "Municipality_ZONNEBEKE",
        "Municipality_ZOTTEGEM",
        "Municipality_ZOUTLEEUW",
        "Municipality_ZUIENKERKE",
        "Municipality_ZULTE",
        "Municipality_ZUTENDAAL",
        "Municipality_ZWALM",
        "Municipality_ZWEVEGEM",
        "Municipality_ZWIJNDRECHT",
    ]
    for feature in features:
        if feature not in df.columns:
            df[feature] = 0
    return df


def convert_non_numeric(df: DataFrame) -> DataFrame:
    # Receives a DataFrame and converts non-numeric data to numeric data.
    building_state = {
        "TO_RESTORE": 0,
        "TO_RENOVATE": 1,
        "TO_BE_DONE_UP": 2,
        "GOOD": 3,
        "JUST_RENOVATED": 4,
        "AS_NEW": 5,
    }
    df["State of Building"] = df["State of Building"].apply(
        lambda x: building_state.get(x, np.NAN)
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
    df["EPC"] = df["EPC"].apply(lambda x: energy_ratings.get(x, np.NAN))

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
    df["Kitchen Type"] = df["Kitchen Type"].apply(
        lambda x: kitchen_types.get(x, np.NAN)
    )

    boolean = {False: 0, True: 1}

    df["Furnished"] = df["Furnished"].apply(lambda x: boolean.get(x, np.NAN))
    df["Openfire"] = df["Openfire"].apply(lambda x: boolean.get(x, np.NAN))
    return df


def convert_non_numeric_to_numeric(df: DataFrame) -> DataFrame:
    # Receives a DataFrame and converts non-numeric data to numeric data.
    building_state = {
        "TO_RESTORE": 0,
        "TO_RENOVATE": 1,
        "TO_BE_DONE_UP": 2,
        "GOOD": 3,
        "JUST_RENOVATED": 4,
        "AS_NEW": 5,
    }
    df["State of Building"] = df["State of Building"].apply(
        lambda x: building_state.get(x, np.NAN)
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
    df["EPC"] = df["EPC"].apply(lambda x: energy_ratings.get(x, np.NAN))

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
    df["Kitchen Type"] = df["Kitchen Type"].apply(
        lambda x: kitchen_types.get(x, np.NAN)
    )

    boolean = {False: 0, True: 1}

    df["Kitchen"] = df["Kitchen"].apply(lambda x: boolean.get(x, np.NAN))
    df["Furnished"] = df["Furnished"].apply(lambda x: boolean.get(x, np.NAN))
    df["Openfire"] = df["Openfire"].apply(lambda x: boolean.get(x, np.NAN))
    df["Terrace"] = df["Terrace"].apply(lambda x: boolean.get(x, np.NAN))
    df["Garden Exists"] = df["Garden Exists"].apply(lambda x: boolean.get(x, np.NAN))
    df["Swimming Pool"] = df["Swimming Pool"].apply(lambda x: boolean.get(x, np.NAN))
    return df


def exclude_outliers(df: DataFrame):
    # Drop the row where Type is not House or Appartment
    df = df[df["Type"].isin(["APARTMENT", "HOUSE"]) | df["Type"].isna()]

    # Drop Kitchen Surface > 100
    df = df[(df["Kitchen Surface"] < 100) | df["Kitchen Surface"].isna()]

    # drop Build year "< 1850"
    df = df[(df["Build Year"] > 1850) | df["Build Year"].isna()]

    # facades <2 -> 2, >4 -> 4
    df["Facades"] = df["Facades"].apply(lambda x: 2 if x < 2 else x)
    df["Facades"] = df["Facades"].apply(lambda x: 4 if x > 4 else x)

    # drop Bathroom Count > 4
    df = df[(df["Bathroom Count"] < 4) | df["Bathroom Count"].isna()]

    # drop bedroom count > 5
    df = df[(df["Bedroom Count"] < 5) | df["Bedroom Count"].isna()]

    # drop colum fireplace count
    df.drop(columns=["Fireplace Count"], inplace=True)

    # drop garden surface > 5000
    df = df[(df["Garden Surface"] < 5000) | df["Garden Surface"].isna()]

    # habitable surface > 700
    df = df[(df["Habitable Surface"] < 700) | df["Habitable Surface"].isna()]

    # drop Landsurface > 3000
    df = df[(df["Land Surface"] < 3000) | df["Land Surface"].isna()]

    # drop the column parking box count
    df.drop(columns=["Parking box count"], inplace=True)

    # drop items with price > 1_000_000
    df = df[(df["Price"] < 1000000) | df["Price"].isna()]

    # drop items that have sale type LIFE_ANNUITY_SALE
    df = df[df["Sale Type"] != "LIFE_ANNUITY_SALE"]

    # only keep items that have SubType == HOUSE, VILLA, TOWN_HOUSE, BUNGALOW, or not specified
    # df = df[df['Subtype'].isin(['HOUSE', 'VILLA', 'TOWN_HOUSE', 'BUNGALOW', None, '']) | df['Subtype'].isna()]

    # only keep items that have toilets of < 6
    df = df[(df["Toilet Count"] < 6) | df["Toilet Count"].isna()]

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


def price_per_sqm(df: DataFrame):
    # Create a new column 'Price per Sqm' by dividing the 'Price' column by the 'Habitable Surface', 'Garden Surface' and 'Terrace Surface' columns
    df["Price per sqm"] = df["Price"] / (
        df["Habitable Surface"] + df["Garden Surface"] + df["Terrace Surface"]
    )
    return df


def main():
    # And Finally, the main function
    # We start off by loading the raw data
    raw_data = load_data("data.csv")
    # We then append the data
    appended_data = append_data(raw_data)
    # We then convert the non-numeric data to numeric data
    converted_data = convert_non_numeric_to_numeric(appended_data)
    # We then fill in the empty data
    filled_data = fill_empty_data(converted_data)
    # We drop some columns that we don't need
    filled_data.drop(
        columns=[
            "Sewer",
            "Terrace Orientation",
            "Garden Orientation",
            "Has starting Price",
            "Transaction Subtype",
            "Is Holiday Property",
            "Gas Water Electricity",
            "Parking count inside",
            "Parking count outside",
            "Land Surface",
        ],
        inplace=True,
    )
    # We create a new column 'Region' by applying the function 'province_to_region' to the 'Province' column
    filled_data["Region"] = filled_data["Province"].apply(province_to_region)
    # We use the price_per_sqm function to create a new column 'Price per Sqm'
    filled_data = price_per_sqm(filled_data)
    # We output the data to a new csv file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    newpath = os.path.join(current_dir, "data", "cleaned", "data.csv")
    filled_data.to_csv(newpath)


if __name__ == "__main__":
    main()
