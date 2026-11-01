import pandas as pd
import pytest
from src.data_loader import load_csv, standardize_columns

def test_load_and_alias(tmp_path):
    p=tmp_path/"x.csv"; p.write_text("Incident Date,Crime Type\n2024-01-01,Theft\n",encoding="utf-8")
    assert list(load_csv(p).columns)==["date","category"]

def test_missing_path():
    with pytest.raises(FileNotFoundError): load_csv("absent.csv")

def test_columns():
    assert list(standardize_columns(pd.DataFrame(columns=["Crime Type","Area Name"])).columns)==["category","area_name"]
