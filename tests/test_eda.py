import pandas as pd
from src.eda import category_frequencies, temporal_counts

def test_frequencies_and_months():
    frame=pd.DataFrame({"category":["Theft","Theft","Assault"],"date":pd.to_datetime(["2024-01-01","2024-01-02","2024-02-01"])})
    assert category_frequencies(frame).iloc[0]==2
    assert list(temporal_counts(frame,"M").index)==[pd.Period("2024-01","M"),pd.Period("2024-02","M")]

def test_optional_and_invalid():
    assert category_frequencies(pd.DataFrame({"x":[]})).empty
    assert temporal_counts(pd.DataFrame({"date":["invalid"]})).empty
