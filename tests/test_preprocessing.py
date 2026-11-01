import pandas as pd
from src.preprocessing import preprocess_data

def test_parse_duplicates_and_missing():
    source=pd.DataFrame({"Incident Date":["2024-01-01","bad","2024-01-01"],"Crime Type":[" Theft ",None," Theft "]})
    clean,report=preprocess_data(source.rename(columns={"Incident Date":"date","Crime Type":"category"}))
    assert len(clean)==2 and report["exact_duplicates_removed"]==1
    assert pd.api.types.is_datetime64_any_dtype(clean.date) and clean.category.iloc[0]=="Theft"

def test_empty_frame():
    clean,_=preprocess_data(pd.DataFrame(columns=["category"]))
    assert clean.empty
