# Dataset sources and limitations

## Default: Chicago crime records, 2026 year to date

- **Provider:** City of Chicago Data Portal; the source description says records are extracted from Chicago Police Department CLEAR (Citizen Law Enforcement Analysis and Reporting).
- **Dataset:** [Crimes - 2001 to Present](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2), dataset ID `ijzp-q8t2`.
- **API:** `https://data.cityofchicago.org/resource/ijzp-q8t2.csv`
- **Snapshot retrieved:** 2026-11-01.
- **Coverage in this project file:** 2026-01-01 through 2026-10-24, the latest date returned by the source query when retrieved (the portal excludes its most recent seven days).
- **Rows returned:** 189,983.
- **Selected fields:** incident ID, date, primary crime type, description, location description, police district, community area, latitude, longitude.
- **License:** The portal lists access as public and refers users to its Terms of Use; it does not name a specific standard open-data license for this dataset. Review those terms before redistribution or other reuse.
- **Attribution:** City of Chicago Data Portal / Chicago Police Department.

This is a static snapshot. The live city dataset is updated regularly; later reports and corrections are not reflected here. The City and CPD warn records may be preliminary and unverified, may contain human or mechanical errors, and are not guaranteed complete or accurate. The portal advises against comparisons over time. Addresses are generalized to blocks; map coordinates are approximate and must not be used to infer specific addresses. Counts are reported incidents, not crime prevalence or population-adjusted rates. This partial-year snapshot cannot support conclusions about full-year totals, seasons, or long-term trends.

The CSV is bundled so the dashboard works offline. To refresh it, query the source and record the retrieval date and returned coverage here. The app itself does not call an external API.

## Earlier full-year snapshot

`chicago_crime_2024.csv` preserves the calendar-year 2024 extract (259,678 records) used for the initial full-year analysis. Apply the same provider, attribution, license, and data-quality caveats above. The dashboard defaults to the 2026 year-to-date snapshot.

## Synthetic fallback

`sample_crime_data.csv` is a deterministic synthetic demonstration dataset authored for this project. It is not real and has no external source, coverage, or third-party license. Select it only for a small offline demonstration.
