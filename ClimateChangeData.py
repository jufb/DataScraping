from bs4 import BeautifulSoup

import requests
import pandas as pd
import re
import tags

print("Reading the data file...")

df = pd.read_excel(r"./Data/data.xlsx", header=None, index_col=None)
urls = df.to_numpy()

print("Accessing pages...")

data = []

for array_url in urls:
    url = array_url[0]
    print(url)
    page = requests.get(url)
    
    soup = BeautifulSoup(page.text, "html.parser")
    
    description_headline = ""
    description_subject = ""
    description_url = ""
    description_tag = ""
    description_source = ""
    description_date = ""
   
    meta_subject = soup.find_all('meta', attrs={'property': 'og:description'})
    if len(meta_subject) > 0:
        description_subject = [meta['content'] for meta in meta_subject][0].replace('&nbsp;', ' ')
    if len(description_subject) == 0:
        meta_subject = soup.find_all('meta', attrs={'name': 'Description'})
        if len(meta_subject) > 0:
            description_subject = [meta['content'] for meta in meta_subject][0].replace('&nbsp;', ' ')

    meta_title = soup.find_all('meta', attrs={'property': 'og:title'})
    if len(meta_title) > 0:
        description_headline = [meta['content'] for meta in meta_title][0].replace('&nbsp;', ' ')
    if len(description_headline) == 0:
        meta_title = soup.find_all('meta', attrs={'name': 'dc.Title'})
        if len(meta_title) > 0:
            description_headline = [meta['content'] for meta in meta_title][0].replace('&nbsp;', ' ')
    if len(description_headline) == 0:
        description_headline = soup.title.string

    meta_url = soup.find_all('meta', attrs={'property': 'og:url'})
    if len(meta_url) > 0:
        description_url = [meta['content'] for meta in meta_url][0].replace('&nbsp;', ' ')
    if len(description_url) == 0:
        description_url = url
    description_url = "=HYPERLINK(\"" + description_url + "\", \"READ\")"

    meta_tag = soup.find_all('meta', attrs={'property': 'article:tag'})
    if len(meta_tag) > 0:
        description_tag = [meta['content'] for meta in meta_tag][0].replace('&nbsp;', ' ')


    meta_site = soup.find_all('meta', attrs={'property': 'og:site_name'})
    if len(meta_site) > 0:
        description_source = [meta['content'] for meta in meta_site][0].replace('&nbsp;', ' ')
    if len(description_source) == 0:
        meta_site = soup.find_all('meta', attrs={'name': 'citation_journal_title'})
        if len(meta_site) > 0:
            description_source = [meta['content'] for meta in meta_site][0].replace('&nbsp;', ' ')


    meta_date = soup.find_all('meta', attrs={'property': 'article:published_time'})
    if len(meta_date) > 0:
        description_date = [meta['content'] for meta in meta_date][0].replace('&nbsp;', ' ')
    if len(description_date) == 0:
        meta_date = soup.find_all('meta', attrs={'name': 'article:published_time'})
        if len(meta_date) > 0:
            description_date = [meta['content'] for meta in meta_date][0].replace('&nbsp;', ' ')
    if len(description_date) == 0:
        meta_date = soup.find_all('meta', attrs={'name': 'dc.Date'})
        if len(meta_date) > 0:
            description_date = [meta['content'] for meta in meta_date][0].replace('&nbsp;', ' ')


    regions = ""
    countries = ""
    groups = ""
    general_tags = description_tag
 
    if len(description_tag) == 0 and len(description_subject) != 0:
        for tag in description_subject.split():
            newtag = re.sub(r'[,.?:]', '', tag)
            description_tag += newtag + ","

    if len(description_tag) > 0:
        for tag in description_tag.split(","):
            if tag.isdigit() is False: #add alphanumeric tag
 
                word = "BIODIVERSITY"
                for title in tags.BIODIVERSITY_1:
                    if title.upper() == tag.upper():
                        groups += word + ","
                        general_tags += title.lower() + ","

                is_clean = False
                word = "CLIMATE CHANGE"
                for title in tags.CLEAN_ENERGY_1:
                    if title.upper() == tag.upper():
                        is_clean = True
                        general_tags += title.lower() + ","
                for title in tags.CLEAN_ENERGY_2:
                    if title.upper() == tag.upper():
                        is_clean = True
                        general_tags += title.lower() + ","
                if is_clean and groups.find(word) == -1:
                    groups += word + ","

                is_climate_change = False
                word = "CLIMATE CHANGE"
                for title in tags.CLIMATE_CHANGE_1:
                    if title.upper() == tag.upper():
                        is_climate_change = True
                        general_tags += title.lower() + ","
                for title in tags.CLIMATE_CHANGE_2:
                    if title.upper() == tag.upper():
                        is_climate_change = True
                        general_tags += title.lower() + ","
                if is_climate_change and groups.find(word) == -1:
                    groups += word + ","

                is_fossil = False
                word = "FOSSIL FUELS"
                for title in tags.FOSSIL_FUELS_1:
                    if title.upper() == tag.upper():
                        is_fossil = True
                        general_tags += title.lower() + ","
                for title in tags.FOSSIL_FUELS_2:
                    if title.upper() == tag.upper():
                        is_fossil = True
                        general_tags += title.lower() + ","
                if is_fossil and groups.find(word) == -1:
                    groups += word + ","

                is_industry = False
                word = "INDUSTRY"
                for title in tags.INDUSTRY_1:
                    if title.upper() == tag.upper():
                        is_industry = True
                        general_tags += title.lower() + ","
                for title in tags.INDUSTRY_2:
                    if title.upper() == tag.upper():
                        is_industry = True
                        general_tags += title.lower() + ","
                if is_industry and groups.find(word) == -1:
                    groups += word + ","

                word = "REGIONS AND COUNTRIES"
                for title in tags.REGIONS_COUNTRIES:
                    if title.upper() == tag.upper() and groups.find(title) == -1:
                        groups += word + ","
                        general_tags += title.lower() + ","

                is_threats = False
                word = "THREATS"
                for title in tags.THREATS_1:
                    if title.upper() == tag.upper():
                        is_threats = True
                        general_tags += title.lower() + ","
                for title in tags.THREATS_2:
                    if title.upper() == tag.upper():
                        is_threats = True
                        general_tags += title.lower() + ","
                if is_threats and groups.find(word) == -1:
                    groups += word + ","

                is_seeking_solutions = False
                word = "SEEKING SOLUTIONS"
                for title in tags.SEEKING_SOLUTIONS_1:
                    if title.upper() == tag.upper():
                        is_seeking_solutions = True
                        general_tags += title.lower() + ","
                for serac in tags.SEEKING_SOLUTIONS_2:
                    if title.upper() == tag.upper():
                        is_seeking_solutions = True
                        general_tags += title.lower() + ","
                if is_seeking_solutions and groups.find(word) == -1:
                    groups += word + ","

                is_social_justice = False
                word = "SOCIAL JUSTICE"
                for title in tags.SOCIAL_JUSTICE_1:
                    if title.upper() == tag.upper():
                        is_social_justice = True
                        general_tags += title.lower() + ","
                for title in tags.SOCIAL_JUSTICE_2:
                    if title.upper() == tag.upper():
                        is_social_justice = True
                        general_tags += title.lower() + ","
                if is_social_justice and groups.find(word) == -1:
                    groups += word + ","

                is_transportation = False
                word = "TRANSPORTATION"
                for title in tags.TRANSPORTATION_1:
                    if title.upper() == tag.upper():
                        is_transportation = True
                        general_tags += title.lower() + ","
                for title in tags.TRANSPORTATION_2:
                    if title.upper() == tag.upper():
                        is_transportation = True
                        general_tags += title.lower() + ","
                if is_transportation and groups.find(word) == -1:
                    groups += word + ","

                for title in tags.REGIONS:
                    tag_country = tag.upper().find(title.upper())
                    if tag_country != -1:
                        regions += title.lower() + ","
                        general_tags = general_tags.replace(tag, "")
                
                for title in tags.COUNTRIES:
                    if title.upper() == tag.upper():
                        countries += title.lower() + ","
                        general_tags = general_tags.replace(tag, "")
    
    if len(general_tags) == 0:
        counter = 0
        for meta_tag in description_tag.split(","):
            if len(meta_tag) > 4 and meta_tag.isdigit() is False and counter < 2: #add tag that is longer than 4 digits, alphanumeric and stops adding after 2 tags
                counter += 1
                general_tags += meta_tag.lower() + ","
    else:
        counter = 0
        for general in general_tags.split(","):
            counter += 1
            if counter > 2:
                general_tags = general_tags.replace(general, "")

    if len(groups) == 0:
        groups += "CLIMATE CHANGE"

    
    
    item = {}
    #item["PREVIEW"] = description_subject
    item["ARTICLE"] = description_headline.title()
    item["LINK"] = description_url
    item["GROUPS"] = groups.title().replace(",,", "").rstrip(",")
    item["TAGS"] = general_tags.title().replace(",,", "").rstrip(",")
    item["REGIONS"] = regions.title().replace(",,", "").rstrip(",")
    item["COUNTRIES"] = countries.title().replace(",,", "").rstrip(",")
    item["SOURCE"] = description_source.title()
    item["DATE"] = description_date[:10]

    data.append(item)

print("Exporting to excel file...")

df = pd.DataFrame(data)
df.to_excel("./Data/ClimateChangeData.xlsx", index = False)

print("Completed!")