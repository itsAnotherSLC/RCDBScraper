## RCDB WebScraper ##
#Created by: Austin Wright
#Creates a CSV of coasters stats

import time
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import enum

#parse the coasters found on each state page
#def parse_state_page(link,name):
  #print("Parse " + name + " at "  + link)
  #response = requests.get(link)
  #soup = bs(response.text,"html.parser")
  #extant_ref = soup.find("body").find("table", id_="counts")
  #time.sleep(5)
  #print(extant_ref)
  #time.sleep(5)


#test the parse_state_page
def parse_state_page_tester():
  link = "https://rcdb.com/location.htm?id=13833" #State page with the number of extant coasters, defunct
  name = "Nevada"
  response = requests.get(link)
  soup = bs(response.text, "html.parser")
  extant_ref = soup.find("body").find("table").find_all("tr")
  time.sleep(5)
  extant_ref = extant_ref[0].find("td").find("a").get("href")
  extant_ref =  "https://rcdb.com" + extant_ref
  time.sleep(5)
  
#test the parser of state extant coasters using state nevada
def parse_extant_coasters_tester():
  link = "https://rcdb.com/r.htm?ot=2&ex&ol=13833" #state of nevada existant coasters
  response = requests.get(link)
  soup = bs(response.text, "html.parser")
  extants = soup.find("body").find("tbody").find_all("tr")
  time.sleep(5)
  for extant in extants:
    name = extant.select_one('td:nth-child(2)').find("a").get_text()
    time.sleep(5)
    ref = "https://rcdb.com" + extant.select_one('td:nth-child(2)').find("a").get("href")
    print("Parse " + name + " at "  + ref)
    time.sleep(5)
    

#test the parse coaster stats page
def parse_coaster_tester():

  Name = None
  Park = None
  City = None
  State = None
  Country = None
  Status_type = None
  #Status_date = None
  Material = None
  Positioning = None
  Thrill = None
  Make = None
  Model = None
  Length = None
  Height = None
  Drop = None
  Speed = None
  Inversions = None
  VerticalAngle = None
  Duration = None
  GForce = None

  
  #link = "https://rcdb.com/103.htm" #The Desperado In Primn
  link = "https://rcdb.com/3344.htm"
  response = requests.get(link)
  soup = bs(response.text, "html.parser")
  stat_sections = soup.find("body").find_all("section")

  ##getting the name##
  Name = stat_sections[0].select_one("div:nth-child(1)").div.div.h1.get_text()
  
  ##getting the meta data of the coaster (location)##
  metas = stat_sections[0].select_one("div:nth-child(1)").div.div.find_all("a")
  Park = metas[0].get_text()
  City = metas[1].get_text()
  State = metas[2].get_text()
  Country = metas[3].get_text()
  
  ##get operational status <p>  Not Quite working for this page: https://rcdb.com/3344.htm##
  Status_type =  stat_sections[0].select_one("div:nth-child(1)").div.p.a.get_text()
  #Status_date =  stat_sections[0].select_one("div:nth-child(1)").div.p.time["datetime"]
  
  #get type <ul class="ll"
  Types = stat_sections[0].select_one("div:nth-child(1)").div.ul.find_all("li")
  Material = Types[1].a.get_text()
  Positioning = Types[2].a.get_text()
  Thrill  = Types[3].a.get_text()

  ##get make and model <div class="scroll"> <p> <a>##
  Types = stat_sections[0].select_one("div:nth-child(1)").div.find("div",class_="scroll").find("p").find_all("a")
  Make = Types[0].get_text()
  Model = Types[2].get_text()

  ##get track stats <section>[1] <table> <tbody>##
  ## https://github.com/willcliffy/RCDB-Scraper/blob/main/scraper.py
  ## Lines 85-105 were borrowed from this file for this section since I had trouble parsing this tbody
  specs = list(soup.find('table', {'class' : 'stat-tbl'}).strings)
  for i in range (len(specs)):
    if specs[i] == 'Length':
      Length = specs[i + 1]
    elif specs[i] == 'Height':
      Height = specs[i + 1]
    elif specs[i] == 'Drop':
      Drop = specs[i + 1]
    elif specs[i] == 'Speed':
      Speed = specs[i + 1]
    elif specs[i] == 'Inversions':
      Inversions = specs[i + 1]
    elif specs[i] == 'Vertical Angle':
      VerticalAngle = specs[i + 1]
    elif specs[i] == 'Duration':
      Duration = specs[i + 1]
    elif specs[i] == 'G-Force':
      GForce = specs[i + 1]
    else:
        continue
    i += 1
      
  print(Name)
  print(Park)
  print(City)
  print(State)
  print(Country)
  print(Status_type)
  #print(Status_date)
  print(Material)
  print(Positioning)
  print(Thrill)
  print(Make)
  print(Model)
  print(Length)
  print(Height)
  print(Drop)
  print(Speed)
  print(Inversions)
  print(VerticalAngle)
  print(Duration)
  print(GForce)
    

#parse the pages found on the US List of coasters on RCDB tester
def parse_parent_pages_tester():
    us_url = "https://rcdb.com/location.htm?id=59"#List of Coasters in the US
    response = requests.get(us_url)                           #Create the response 
    soup = bs(response.text, "html.parser")              #Parse the response
    states_table = soup.find("body").find("div", class_="stdtbl cen").find("table").find("tbody").find_all("tr")  #Find the table of states
    for state in states_table:                #Parse each state
      table_data = state.find_all("td") #State table data sections
      td = table_data[0].find("a")          #State name and link section
      ref = "https://rcdb.com" + td.get('href') #Link reference
      name = td.get_text()                        #State name
      print("Parsing the state of " + name +  " at " + ref)

def parse_state_page():
  us_url = "https://rcdb.com/location.htm?id=59"#List of Coasters in the US
  response = requests.get(us_url)                           #Create the response 
  soup = bs(response.text, "html.parser")              #Parse the response
  states_table = soup.find("body").find("div", class_="stdtbl cen").find("table").find("tbody").find_all("tr")  #Find the table of states
  for state in states_table:                #Parse each state
    table_data = state.find_all("td") #State table data sections
    td = table_data[0].find("a")          #State name and link section
    ref = "https://rcdb.com" + td.get('href') #Link reference
    name = td.get_text()                        #State name
    print("Parsing the state of " + name +  " at " + ref)

def main():
  #print("Heelo")
  #parse_extant_coasters_tester()
  #parse_state_page_tester()
  #parse_coaster_tester()
  data = [["ID","Name","Park","City","State","Country","Status","Material","Seating","Thrill","Make","Model","Length","Height","Drop","Speed","Inversions","VerticalAngle","Duration","G-Force"]]
  #For Each State
  parse_state_page()
    #For Each Coaster
      #Get Each Coaster and Append to data[[]]
    
  


if __name__ == '__main__':
    main()
