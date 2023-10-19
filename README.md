# DoctoraliaScraper
DoctoraliaScraper recursively crawls [doctoralia.com.br](https://www.doctoralia.com.br/) and extracts data from healthcare professionals listed on Doctoralia.

I built DoctoraliaScraper to create a dataset of all healthcare professionals in 🇧🇷 Brazil (where I was located at the time) including price, location, specialization, and number of reviews to find the best professionals.

## About Doctoralia
Doctoralia is an global online platform that allows users to search, read ratings, and book appointments with healthcare professionals. It is highly popular in Brazil.

## Inspiration
Selecting a healthcare professional is an important decision and it can be challenging to find the right person for you. 

I built DoctoraliaScraper to create a dataset of all healthcare professionals in 🇧🇷 Brazil (where I'm currently located) including price, location, specialization, and number of reviews. Find the best healthcare professional for you!

## Requirements

- Python
- [Scrapy](https://scrapy.org)
- [tqdm](https://tqdm.github.io)
- [Pandas](https://pandas.pydata.org) (optional)

## Usage

1. Clone this repository
2. Move to the `doctoralia-scraper` directory
3. Run `scrapy runspider scrapy-project/doctoralia/spiders/doctoralia.py -o output.jl`. This generates a JSON lines file which you can read with Pandas:

```python
import pandas as pd
df = pd.read_json('./output.jl', lines=True)
```

## Dataset
Check out a dataset of 165k doctors and healthcare professionals in Brazil I published on [Kaggle.com](https://www.kaggle.com/datasets/miguelcorraljr/doctoralia-brasil).

## Attributes
|   Attribute     |   Description                                                                            |   Data Type           |
|-----------------|------------------------------------------------------------------------------------------|-----------------------|
|   doctor_id     |   Doctor identification number provided by Doctoralia                                    |   int                 |
|   title         |   Title of the healthcare professional (e.g. 'Dr', 'Dra', 'Prof.')                       |   string              |
|   name          |   Full name of the healthcare professional                                               |   string              |
|   city1         |   Name of the city including local grammar (e.g. São Paulo)                              |   string              |
|   city2         |   Name of the city in lower case and hyphens (e.g. sao-paulo)                            |   string              |
|   region        |   Name of the region including inititals for the state (e.g. sao-paulo-sp)               |   string              |
|   specialization|   The main specializaton of the healthcare professional (e.g. cardiologist)              |   string              |
|   reviews       |   Count of reviews/opinions                                                              |   int                 |
|   newest_review_date |   Date of the most recent review posted                                             |   date                |
|   telemedicine  |   If the healthcare professional provides service remotely (i.e. 1 = 'Yes', 0 = 'No')    |   int                 |
|   price         |   Most common price of all the services provided by the healthcare professional          |   string              |
|   url           |   URL to the healthcare professional's page                                              |   string              |
|   fetch_time    |   Date and time the data was fetched                                                     |   date                |

## Sample Data
| doctor_id | name                     | city1         | city2         | region            | specialization           | reviews | newest_review_date        | telemedicine | price | url                                                   | fetch_time          |
|-----------|--------------------------|---------------|---------------|-------------------|--------------------------|---------|---------------------------|--------------|-------|-------------------------------------------------------|---------------------|
| 357421    | Marília Rocha            | Porto Velho   | porto-velho   | rondonia-ro       | alergista-pediatrico     | 244     | 2022-10-23T15:00:55-03:00 | 0            |       | http://www.doctoralia.com.br/marilia-rocha            | 2022-10-28 12:02:04 |
| 621416    | Juliana Murata           | Curitiba      | curitiba      | parana-pr         | pneumologista-pediatrico | 324     | 2022-10-27T17:40:27-03:00 | 0            | 300   | http://www.doctoralia.com.br/juliana-murata           | 2022-10-28 12:02:04 |
| 691614    | Queise Cettolin          | Salvador      | salvador      | bahia-ba          | cirurgiao-vascular       | 46      | 2022-10-21T18:06:29-03:00 | 0            | 250   | http://www.doctoralia.com.br/queise-cettolin          | 2022-10-28 12:02:46 |
| 43986     | Letícia Scolfaro Celegao | Campinas      | campinas      | sao-paulo-sp      | angiologista             | 194     | 2022-10-27T23:43:16-03:00 | 1            | 650   | http://www.doctoralia.com.br/leticia-scolfaro-celegao | 2022-10-28 12:02:48 |
| 4828      | Priscilla Vogt           | Florianópolis | florianopolis | santa-catarina-sc | psicologo                | 46.0    | 2022-10-14T20:35:58-03:00 | 1            | 170   | http://www.doctoralia.com.br/priscilla-vogt           | 2022-10-27 23:28:43 |


## Meta
Author: Miguel Corral Jr.  
Email: corraljrmiguel@gmail.com  
LinkedIn: https://www.linkedin.com/in/iMiguel  
GitHub: https://github.com/corralm

Distributed under the MIT license. See [LICENSE](./LICENSE) for more information.
