import pandas as pd
from src.insights import generate_insights

def test_dynamic_insights():
    frame=pd.DataFrame({"category":["Theft","Theft","Fraud"],"area":["A","B","B"]})
    notes=generate_insights(frame)
    assert "Theft" in notes[0] and "66.7%" in notes[0]
    assert "B" in notes[1]

def test_empty_insights():
    assert generate_insights(pd.DataFrame())[0].startswith("Not enough")
