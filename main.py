import streamlit as st
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import sys
import dateparser
st.title('Overblikket')
st.subheader('De seneste uger på Vigeur')
visKaffebrief = st.checkbox('Vis Kaffebrief')
with st.spinner('Henter info ...'):
  #Først henter vi links til historier fra de seneste 4 oversigtssider
  page = 1
  links = []
  while page != 5:
        url = f"https://vigeur.dk/soeg?searchTerm=&page={page}"
        response = requests.get(url)
        html = response.content
        soup = bs(html, "html.parser")
        for a in soup.find_all("a", class_="article-teaser article-teaser--md article-teaser--image-left"):
          if "kaffebrief" in a.get('href'):
            if visKaffebrief:
              links.append(a.get('href'))
          else:
            links.append(a.get('href'))
        page = page + 1
  #Så looper så igennem dem og henter detaljer til stories 
  stories = []
  for link in links:
        url = f"https://vigeur.dk{link}"
        response = requests.get(url)
        html = response.content
        soup = bs(html, "html.parser")  
        rubrik = soup.h1.text
        beskrivelse = soup.find("h2", class_="article-top__sub-header")
        #publicerings_dato =  soup.find("div", class_="mb-5 row")
        publicerings_dato_str =  soup.find("div", class_="text-muted text-xs")
        skribentMedNyLinje = soup.find("div", class_="article-author__name")
        skribent = skribentMedNyLinje.text.strip()
        #print(publicerings_dato_str.text)
        publicerings_dato = dateparser.parse(publicerings_dato_str.text)
        #INDTIL OVENSTÅENDE IKKE GIVER SYS-FEJL
        #publicerings_dato = publicerings_dato_str.text
        #print(rubrik)
        #print(beskrivelse.text)
        #print(publicerings_dato)
        #print(skribent)
        stories.append({'Dato':publicerings_dato, 'HL':rubrik, 'BS':beskrivelse.text, 'Skribent':skribent, 'Link':url})
        #stories.append()
  #Sætter dem i en dataframe og viser den
  dfStories = pd.DataFrame(stories)
  dfStories['Dato'] = dfStories['Dato'].dt.date
#st.success('Klar!')
# Dataframe and Chart display section
st.dataframe(dfStories, use_container_width=True) 
#
#print(soup.prettify())
#print(stories)