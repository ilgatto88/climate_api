# Municipality Data Output Description

## General Information

A detailed description of the output of the endpoints `api/v1/municipalitydata/historical/<parameter>/<municipality_id>` and `api/v1/municipalitydata/scenario/<scenario>/<parameter>/<municipality_id>` are provided below. Please note that the output is only an example and the actual values may differ. The example output is based on the municipality with the ID `10101` (Eisenstadt), the climate parameter `tm` (mean temperature) and the scenario `rcp26` where needed.  
How many grid points are included in the analysis depends on the municipality.

## Municipality historical data structure

The output is a JSON object that contains the following fields:

- `municipalityId`: Represents the unique identifier of the municipality (Gemeinde ID). Example: `10101`, which is the municipality ID of the municipality Eisenstadt in Burgenland.
- `source`: Describes the source of the data. Example in case of historical data: `Spartacus v2.1`
- `climateParameter`: Indicates the climate parameter being analyzed. Abbreviations are used for the parameter names. Example: `tm` for mean temperature.
- `temporalResolution`: Specifies the temporal resolution of the data. Currently, only annual data is available. Example: `annual`
- `analysisTimeRange`: Defines the time range over which the analysis was performed. A list of numbers representing the years included in the analysis. This dataset includes every year between 1961 and 2021. Example: `[1961, 1962, ..., 2020, 2021]`
- `rawData`: Represents the raw climate data used for analysis. The data is organized in a list, where each element represents the parameter value for a given year. Example: `[1.2, 1.3, ..., 1.4, 1.5]`
- `statistics0D`: Contains statistical data for 0-dimensional (scalar) values.
  - `1971-2000`: Statistical information for the period 1971-2000.
    - `mean`: Mean value calculated for the given parameter.
  - `1981-2010`: Same structure as `1971-2000`.
  - ...

## Municipality scenario data structure

The output is a JSON object that contains the following fields:

- `municipalityId`: Represents the unique identifier of the municipality (Gemeinde ID). Example: `10101`, which is the municipality ID of the municipality Eisenstadt in Burgenland.
- `source`: Describes the source of the data. Example in case of scenario data: `rcp26` or `rcp85`
- `climateParameter`: Indicates the climate parameter being analyzed. Abbreviations are used for the parameter names. Example: `tm` for mean temperature.
- `temporalResolution`: Specifies the temporal resolution of the data. Currently, only annual data is available. Example: `annual`
- `ensembleTimeRange`: Specifies the time range for the ensemble data. A list of numbers representing the years included in the ensemble data. This dataset includes every year between 1970 and 2100. Example: `[2021, 2022, ..., 2099, 2100]`
- `modelNames`: List of the model names used in the ensemble.
- `rawData`: Represents the raw ensemble data extracted for the selected municipality. This serves as the basis for the statistical analysis. The data is organized into key-value pairs, where the key represents the model name and the value represents the raw data for the given model. Example: `{ "ICHEC-EC-EARTH_r12i1p1_CLMcom-CCLM4-8-17": [1.2, 1.3, ..., 1.4, 1.5], "model2": [1.2, 1.3, ..., 1.4, 1.5], ... }`
- `statistics1D`: Contains statistical data for 1-dimensional (time series) values.
  - `minimum`: Minimum value calculated from the models for the given parameter. Example: `[1.2, 1.3, ..., 1.4, 1.5]`
  - `lowerPercentile`: Lower percentile (10%) value calculated from the models for the given parameter. Example: `[1.3, 1.4, ..., 1.5, 1.6]`
  - `median`: Median value calculated from the models for the given parameter. Example: `[1.4, 1.5, ..., 1.6, 1.7]`
  - `mean`: Mean value calculated from the models for the given parameter. Example: `[1.4, 1.5, ..., 1.6, 1.7]`
  - `upperPercentile`: Upper percentile (90%) value calculated from the models for the given parameter. Example: `[1.5, 1.6, ..., 1.7, 1.8]`
  - `maximum`: Maximum value calculated from the models for the given parameter. Example: `[1.6, 1.7, ..., 1.8, 1.9]`
- `statistics0D`: Contains statistical data for 0-dimensional (scalar) values, specific to different time ranges, calculated from the models.
  - `1971-2000`: Statistical information for the period 1971-2000.
    - `minimum`: Minimum value calculated from the models for the given parameter. Example `10.0`
    - `lowerPercentile`: Lower percentile (10%) value calculated from the models for the given parameter. Example `10.2`
    - `median`: Median value calculated from the models for the given parameter. Example `10.4`
    - `mean`: Mean value calculated from the models for the given parameter. Example `10.5`
    - `upperPercentile`: Upper percentile (90%) value calculated from the models for the given parameter. Example `10.8`
    - `maximum`: Maximum value calculated for the given parameter. Example `11.0`
  - `1981-2010`: Same structure as `1971-2000`.
    - ...
  - Additional statistical information for future time ranges follows the same structure.

These structures allow organizing and accessing climate data for different parameters, time ranges, scenarios, and statistical measures. The separation of the datasets by parameter and source allows more flexibility regarding expanding them with new parameters and sources.
