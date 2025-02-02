## RCDB WebScraper ##
# Created by: Austin Wright
# Creates a CSV of coasters stats

import time
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
from random import seed
from random import randint
import logging
import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains


seed(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Parser class: Methods are
class Parser():
    coaster_data_array = [[]]
    coaster_extant_pages = []

    visited_parks_and_rides = {
        "Arizona": {
            "Castles n' Coasters": [
                "Desert Storm",
                "Patriot",
            ]
        },
        "California": {
            "Belmont Park": ["Giant Dipper"],
            "California's Great America": [
                "Gold Striker",
                "RailBlazer",
                "Invertigo",
                "Lucy's Crabbie Cabbies",
                "Patriot",
                "Flight Deck",
                "Demon",
                "Grizzly",
                "Psycho Mouse",
                "Woodstock Express",
            ],
            "Disney California Adventure Park": [
                "Incredicoaster",
                "Goofy's Sky School",
            ],
            "Disneyland": [
                "Space Mountain",
                "Matterhorn Bobsleds",
                "Big Thunder Mountain Railroad",
                "Chip & Dale’s Gadget Coaster",
            ],
            "Gilroy Gardens Family Theme Park": ["Quicksilver Express", "Timber Twister"],
            "Happy Hollow Park and Zoo": ["Pacific Fruit Express"],
            "Knott's Berry Farm": [
                "GhostRider",
                "HangTime",
                "Boomerang",
                "Silver Bullet",
                "Xcelerator",
                "Sierra Sidewinder",
                "Jaguar!",
                "Pony Express",
                "Montezooma's Revenge",
                "Coast Rider",
                "Timberline Twister",
            ],
            "Legoland California": ["The Dragon", "Coastersaurus", "Technic Coaster", "Dragon"],
            "Oakland Zoo": ["Tiger Trek"],
            "Pacific Park": ["Santa Monica West Coaster"],
            "Santa Cruz Beach Boardwalk": ["Giant Dipper", "Undertow", "Hurricane", "Sea Serpent"],
            "SeaWorld San Diego": ["Manta", "Journey to Atlantis", "Electric Eel", "Emperor", "Arctic Rescue","Tidal Twister"],
            "Six Flags Discovery Kingdom": [
                "Medusa",
                "Kong",
                "Superman Ultimate Flight",
                "Joker",
                "Boomerang",
                "Batman The Ride",
                "Flash: Vertical Velocity",
                "Roadrunner Express",
                "Pandemonium",
                "Roar",
                "Cobra",
                "Harley Quinn Crazy Coaster",
            ],
            "Six Flags Magic Mountain": [
                "Twisted Colossus",
                "X2",
                "Tatsu",
                "Goliath",
                "Scream!",
                "Gold Rusher",
                "Batman The Ride",
                "Riddler's Revenge",
                "Apocalypse the Ride",
                "Ninja",
                "Viper",
                "New Revolution",
                "Canyon Blaster",
                "Wonder Woman Flight of Courage",
                "West Coast Racers",
                "Speedy Gonzales Hot Rod Racers",
                "Road Runner Express",
                "Full Throttle",
                "Superman: Escape from Krypton",
                "Colossus",
                "Green Lantern: First Flight",
            ],
            "Universal Studios Hollywood": ["Revenge of the Mummy the Ride"]
        },
        "Colorado": {
            "Glenwood Caverns Adventure Park": [
                "Alpine Coaster",
            ]
        },
        "Florida": {
            "Busch Gardens Tampa": [
                "Air Grover",
                "Montu",
                "Kumba",
                "SheiKra",
                "Cheetah Hunt",
                "Scorpion",
                "Cobra's Curse",
                "Tigris",
                "SandSerpent",
                "Iron Gwazi",
            ],
            "Walt Disney World - Disney's Animal Kingdom": ["Expedition Everest", "Primeval Whirl"],
            "Walt Disney World - Disney's Hollywood Studios": ["Rock 'n' Roller Coaster"],
            "SeaWorld Orlando": [
                "Mako",
                "Kraken",
                "Manta",
                "Journey to Atlantis",
                "Pipeline the Surf Coaster",
                "Ice Breaker",
            ],
            "Universal Studios Islands of Adventure": [
                "Incredible Hulk",
                "Hagrid's Magical Creatures Motorbike Adventure",
                "Flight of the Hippogriff",
                "VelociCoaster",
            ],
            "Universal Studios Florida": [
                "Hollywood Rip, Ride, Rockit",
                "Revenge of the Mummy",
                "Harry Potter and the Escape from Gringotts",
            ]
        },
        "Missouri": {
            "Silver Dollar City": [
                "Outlaw Run",
                "Time Traveler",
                "Wildfire",
                "Powder Keg: A Blast in the Wilderness",
                "Thunderation",
                "Fire In The Hole",
            ]
        },
        "Nevada": {
            "New York, New York Hotel & Casino": [
                "Big Apple Coaster",
            ]
        },
        "New Jersey": {
            "Six Flags Great Adventure": [
                "El Toro",
                "Kingda Ka",
                "Nitro",
                "Medusa",
                "Skull Mountain",
                "Runaway Mine Train",
                "Joker",
                "Batman The Ride",
                "Dark Knight",
                "Jersey Devil Coaster",
            ],
            "Nickelodeon Universe Theme Park": [
                "Nickelodeon Slime Streak",
                "Sandy’s Blasting Bronco",
                "Shredder",
                "TMNT Shellraiser",
            ]
        },
        "Ohio": {
            "Cedar Point": [
                "Millennium Force",
                "Top Thrill 2",
                "Maverick",
                "Steel Vengeance",
                "Magnum XL-200",
                "Raptor",
                "GateKeeper",
                "Valravn",
                "Rougarou",
                "Blue Streak",
                "Cedar Creek Mine Ride",
                "Gemini",
                "Iron Dragon",
                "Wicked Twister",
                "Corkscrew",
            ],
            "Kings Island": [
                "Diamondback",
                "Banshee",
                "Backlot Stunt Coaster",
                "Beast",
                "Mystic Timbers",
                "Flight of Fear",
                "Invertigo",
                "Bat",
                "Adventure Express",
                "Racer",
                "Vortex",
                "Firehawk",
                "Woodstock’s Air Rail"
            ]
        },
        "Pennsylvania": {
            "Hersheypark": [
                "Candymonium",
                "Skyrush",
                "Storm Runner",
                "Fahrenheit",
                "Great Bear",
                "Lightning Racer",
                "Wildcat's Revenge",
                "Comet",
                "Sooperdooperlooper",
                "Laff Trakk",
            ],
        },
        "Texas": {
            "Six Flags Fiesta Texas": [
                "Iron Rattler",
                "Superman Krypton Coaster",
                "Goliath",
                "Poltergeist",
                "Batman The Ride",
                "Superman Krypton Coaster",
                "Wonder Woman Golden Lasso Coaster",
                "Dr. Diabolical's Cliffhanger",
            ],
            "Six Flags Over Texas": [
                "Batman The Ride",
                "New Texas Giant",
                "Joker",
                "Titan",
                "Mr. Freeze",
                "Mini Mine Train",
                "Shock Wave",
                "Batman The Ride",
                "Runaway Mine Train",
                "Runaway Mountain",
                "Judge Roy Scream",
                "La Vibora",
                "Aquaman: Power Wave",
                "Pandemonium",
            ],
            "SeaWorld San Antonio": [
                "Great White",
                "Journey to Atlantis",
                "Steel Eel",
                "Texas Stingray",
                "Wave Breaker: The Rescue Coaster",
            ]
        },
        "Utah": {
            "Lagoon": [
                "Cannibal",
                "Colossus the Fire Dragon",
                "Wicked",
                "Spider",
                "Jet Star 2",
                "Roller Coaster",
                "Primordial",
                "Wild Mouse",
                "Roller Coaster",
            ]
        }
    }

    #####################################################
    # Return a data array of coaster stats
    # Must include a link to a coaster
    #####################################################
    def parse_coaster(coaster_link):

        ## Initialize the stats ##
        ID = Name = Park = City = State = Country = None
        Status_type = Status_date = Material = Positioning = Thrill = None
        Make = Model = Length = Height = Drop = Speed = Inversions = None
        VerticalAngle = Duration = GForce = Link = None

        # Fetch the page
        try:
            response = requests.get(coaster_link)
            response.raise_for_status()
            soup = bs(response.text, "html.parser")

            try:
                # Parse the name
                stat_sections = soup.find("body").find_all("section")
                Name = stat_sections[0].select_one("div:nth-child(1)").div.div.h1.get_text(strip=True)
                # Add Link
                Link = coaster_link
            except Exception as e:
                logging.error(f"Error parsing Name: {e}")

            try:
                # Parse location metadata
                #time.sleep(randint(0, 2))
                metas = stat_sections[0].select_one("div:nth-child(1)").div.div.find_all("a")
                if metas:
                    Park = metas[0].get_text(strip=True)
                    City = metas[1].get_text(strip=True)
                    State = metas[2].get_text(strip=True)
                    Country = metas[3].get_text(strip=True)
            except Exception as e:
                logging.error(f"Error parsing location metadata: {e}")

            try:
                # Parse operational status
                status = stat_sections[0].select_one("div:nth-child(1)").div.p
                if status:
                    Status_type = status.a.get_text(strip=True)
                    if status.time:
                        Status_date = status.time.get("datetime", None)
            except Exception as e:
                logging.error(f"Error parsing operational status: {e}")

            try:
                # Parse type (Material, Positioning, Thrill)
                Types = stat_sections[0].select_one("div:nth-child(1)").div.ul.find_all("li")
                if Types:
                    #time.sleep(randint(0, 2))
                    Material = Types[1].a.get_text(strip=True) if len(Types) > 1 else None
                    Positioning = Types[2].a.get_text(strip=True) if len(Types) > 2 else None
                    Thrill = Types[3].a.get_text(strip=True) if len(Types) > 3 else None
            except Exception as e:
                logging.error(f"Error parsing type: {e}")

            try:
                # Parse Make and Model
                Types = stat_sections[0].select_one("div:nth-child(1)").div.find("div", class_="scroll")
                #time.sleep(randint(0, 2))
                if Types:
                    TypesCheck = Types.get_text().split(":")
                    for i, t in enumerate(Types.find_all("a")):
                        if "Make" in TypesCheck[i]:
                            Make = t.get_text(strip=True)
                        if "Model" in TypesCheck[i]:
                            Model = t.get_text(strip=True)
            except Exception as e:
                logging.error(f"Error parsing Make and Model: {e}")

            try:
                # Parse track stats
                stats_table = soup.find('table', {'class': 'stat-tbl'})
                time.sleep(randint(0, 2))
                if stats_table:
                    specs = list(stats_table.strings)
                    for i in range(len(specs)):
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
            except Exception as e:
                logging.error(f"Error parsing track stats: {e}")

        except requests.exceptions.RequestException as e:
            logging.critical(f"Request error: {e}")
            return None

        except Exception as e:
            logging.critical(f"Unexpected error: {e}")
            return None

        # Hash a deterministic ID
        try:
            if Name is not None and Park is not None:
                # Combine park and coaster name for a unique key
                unique_string = f"{Park}-{Name}".lower().strip()
                ID = hashlib.md5(unique_string.encode()).hexdigest()  # Generate a hash
        except Exception as e:
            logging.critical(f"Unable to generate ID: {e}")
            return None

        # Return the data array
        data = [
            ID, Name, Park, City, State, Country, Status_type, Status_date, Material,
            Positioning, Thrill, Make, Model, Length, Height, Drop, Speed, Inversions,
            VerticalAngle, Duration, GForce, Link
        ]
        #logging.info("Parsed data successfully")
        #print(data)

        return data

    ####################################################
    # Parse a park page
    ####################################################
    def parse_park_page(link):
        ## Initialize the stats ##
        ID = Name = City = State = Country = Status_type = Status_date = None

        # Fetch the page
        try:
            response = requests.get(link)
            response.raise_for_status()
            soup = bs(response.text, "html.parser")
            time.sleep(randint(0, 2))

            try:
                # Parse the park name
                Name = soup.find("body").find("div", id="feature").find("h1").get_text(strip=True)
            except Exception as e:
                logging.error(f"Error parsing Name: {e}")

            try:
                # Parse location metadata
                location_section = soup.find("body").find("div", id="feature").find_all("a")
                if location_section:
                    City = location_section[0].get_text()
                    State = location_section[1].get_text()
                    Country = location_section[2].get_text()
            except Exception as e:
                logging.error(f"Error parsing location metadata: {e}")

            try:
                # Parse operational status
                status_section = soup.find("body").find("div", id="feature").find("p")
                if status_section:
                    Status_type = status_section.find("a").get_text()
                    Status_date = status_section.find("time").get("datetime", None)

            except Exception as e:
                logging.error(f"Error parsing operational status: {e}")

        except requests.exceptions.RequestException as e:
            logging.critical(f"Request error: {e}")
            return None

        except Exception as e:
            logging.critical(f"Unexpected error: {e}")
            return None

        # Hash a deterministic ID
        try:
            if Name is not None and Name is not None:
                # Combine park and coaster name for a unique key
                unique_string = f"{Name}".lower().strip()
                ID = hashlib.md5(unique_string.encode()).hexdigest()  # Generate a hash
        except Exception as e:
            logging.critical(f"Unable to generate ID: {e}")
            return None

        # Return the data array
        data = [ID, Name, City, State, Country, Status_type, Status_date, link]
        logging.info("Parsed park data successfully")
        print(data)

        return data

    ####################################################
    # Return an array of extant coaster page links
    ####################################################
    def get_extant_pages(link):
        response = requests.get(link)  # Get Response
        soup = bs(response.text, "html.parser")  # Create Responser
        num_pages = soup.body.section.select_one("div:nth-child(3)").select_one(
            "a:nth-child(5)").get_text()  # Get number of pages of existant coasters
        _ = [None] * (int(num_pages))  # Array of existing coaster pages
        _[0] = link
        prev_page = link
        for i in range(1, int(num_pages)):
            if i == 36:
                break
            response = requests.get(prev_page)  # Get Response
            soup = bs(response.text, "html.parser")  # Create Responser
            _[i] = "https://rcdb.com" + soup.body.section.select_one("div:nth-child(3)").find("a", string=">>").get(
                "href")
            prev_page = _[i]
            print("new page: " + _[i])
            #time.sleep(randint(0, 2))
        return _

    ####################################################
    # Return an array of links to State pages
    ####################################################
    def get_state_page_links(us_url, visited_parks_and_rides):
        # us_url = "https://rcdb.com/location.htm?id=59"  # List of Coasters in the US
        include_visited = True
        response = requests.get(us_url)  # Create the response
        #time.sleep(randint(0, 2))
        soup = bs(response.text, "html.parser")  # Parse the response
        states_table = soup.find("body").find("div", class_="stdtbl cen").find("table").find("tbody").find_all(
            "tr")  # Find the table of States
        refs = []

        # Extract the visited states from the dictionary keys
        visited_states = visited_parks_and_rides.keys()

        for i in range(len(states_table)):  # Parse each State
            table_data = states_table[i].find_all("td")  # State table data sections
            #time.sleep(randint(0, 2))
            td = table_data[0].find("a")  # State name and link section
            ref = "https://rcdb.com" + td.get('href')  # URL to State page
            name = td.get_text()  # State name
            if not include_visited or name in visited_states:  # Check if the state is in visited states
                refs.append(ref)  # Populate reference array with new URL reference
                #print(f"The state of {name} is at {ref}")
        return refs

    #####################################################
    # Return a link to the extant parks of a state page
    # ***Must include a link to a state page***
    #####################################################
    def get_state_extant_parks_link(state__page_link):
        response = requests.get(state__page_link)  # Create response
        soup = bs(response.text, "html.parser")  # Parse the response
        name = soup.find("body").find("h1").get_text()
        #time.sleep(randint(0, 2))
        extant_ref = soup.find("table").find_all("tr")  # Find tr's within the table body
        extant_ref = extant_ref[2].find("td").find("a").get("href")  # Extract 3rd table reference to get the url href for extant parks
        extant_ref = "https://rcdb.com" + extant_ref  # Format url
        #print(name, "'s extant coasters are located at: ", extant_ref)
        return extant_ref

    ####################################################
    # Return a link to a State's additional amusement park page
    ####################################################
    def get_additional_park_page_links(state_link):
        try:
            # Fetch the page
            response = requests.get(state_link)
            response.raise_for_status()  # Raise an error for HTTP issues
            soup = bs(response.text, "html.parser")
            #time.sleep(randint(0, 2))

            # Parse pagination section
            pagination = soup.find("body").find("section").find("div", id="rfoot")
            if not pagination:
                raise ValueError("Pagination section not found.")

            # Extract additional park link
            pagination_links = pagination.find_all("a")
            if not pagination_links or len(pagination_links) < 1:
                raise ValueError("No additional park links found.")

            additional_park_link = "https://rcdb.com" + pagination_links[0].get("href")
            #print("Additional page found at: ", additional_park_link)
            return additional_park_link

        except requests.exceptions.RequestException as e:
            print(f"HTTP request error: {e}")
        except ValueError as e:
            print(f"Parsing error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return None

    ####################################################
    # Return an array of links to each park from a state page
    ####################################################
    def get_park_page_links(link, visited_parks_and_rides):
        response = requests.get(link)
        soup = bs(response.text, "html.parser")
        #time.sleep(randint(0, 2))
        park_table = soup.find("body").find("div", class_="stdtbl rer").find("table").find("tbody").find_all(
            "tr")  # Find the table of parks
        refs = []

        # Flatten the visited_parks_and_rides dictionary to extract all parks
        all_parks = {park for state in visited_parks_and_rides.values() for park in state.keys()}

        for i in range(len(park_table)):  # Parse each State
            table_data = park_table[i].find_all("td")  # State table data sections
            #time.sleep(randint(0, 2))
            td = table_data[1].find("a")  # State name and link section
            ref = "https://rcdb.com" + td.get('href')  # URL to State page
            name = td.get_text()  # State name
            if name in all_parks:  # Check if park name is in visited parks
                refs.append(ref)  # Populate reference array with new URL reference
                #print(f"The park {name} is at {ref}")

        return refs

    ####################################################
    # Return an array of links to each park's coaster page from a park page
    ####################################################
    def get_park_coaster_page_links(park_page, visited_parks_and_rides):
        response = requests.get(park_page)
        soup = bs(response.text, "html.parser")

        # Store references to coaster pages
        refs = []
        # Find park title
        park_td = soup.find("body").find("div", id="demo").find("div", id="feature").find("div").find("h1")

        # Find all ride tables on a page
        ride_tables = soup.find("body").find_all("section")
        for ride_table in ride_tables:
            if ride_table.find("h4"):
                table_tl = ride_table.find("h4").get_text()
                # Find a valid ride table header
                if (
                    "Roller Coasters Under Construction: " in table_tl or
                    "Operating Roller Coasters: " in table_tl or
                    "Defunct Roller Coasters: " in table_tl or
                    "SBNO Roller Coasters: " in table_tl
                ):
                    #time.sleep(randint(0, 2))
                    ride_table = ride_table.find("div", class_="stdtbl ctr").find("table").find("tbody").find_all("tr")
                    # Flatten the dictionary to get a mapping of parks to coasters
                    all_parks = {
                        park: set(coasters) for state, parks in visited_parks_and_rides.items() for park, coasters in parks.items()
                    }
                    park_name = park_td.get_text().strip() if park_td else None  # Park name

                    if park_name in all_parks:  # Check if the park is in visited parks
                        for row in ride_table:  # Iterate through the ride table
                            table_data = row.find_all("td")
                            coaster_td = table_data[1].find("a")  # Coaster name and link section
                            #time.sleep(randint(0, 2))
                            if not coaster_td or not coaster_td.get_text(strip=True):
                                print("No valid coaster name found.")
                                continue
                            coaster_name = coaster_td.get_text(strip=True).lower()  # Coaster name
                            ref = "https://rcdb.com" + coaster_td.get('href') if coaster_td else None  # Coaster URL d
                            # Check each coaster in the visited list for the park
                            for visited_coaster in all_parks[park_name]:
                                # Normalize visited coaster name
                                normalized_visited_coaster = visited_coaster.strip().lower()

                                # Compare with extracted coaster name
                                if coaster_name == normalized_visited_coaster:
                                    refs.append(ref)
                                    print(f"Match found! Park: {park_name}, Coaster: {coaster_name}, URL: {ref}")
                                    break
                            else:
                                print(f"No match for {coaster_name}!")
        return refs

    ####################################################
    # Export a dataframe of visited parks to a csv
    ####################################################
    def parse_visited_parks():
        print("Exporting a dataframe of visited parks and coasters to a csv")
        coaster_columns = ["ID", "Name", "Park", "City", "State", "Country", "Status", "Status Date", "Material",
                           "Seating", "Thrill",
                           "Make", "Model", "Length", "Height", "Drop", "Speed", "Inversions", "VerticalAngle",
                           "Duration", "G-Force", "Link"]
        park_columns = ['ID', 'Name', 'City', 'State', 'Country', 'Status', 'Status Date', 'Link', 'Coaster_IDs']

        us_link = "https://rcdb.com/location.htm?id=59"  # List US states
        response = requests.get(us_link)  # Get Response
        soup = bs(response.text, "html.parser")  # Create Responser
        num_parks, num_coasters = Parser.count_parks_and_rides(Parser.visited_parks_and_rides)

        print("Number of parks:", num_parks)
        print("Number of coasters:", num_coasters)

        # Parse the parks and export a parks dataframe
        state_links = Parser.get_state_page_links(us_link, Parser.visited_parks_and_rides)
        state_park_index_links = []

        for state_link in state_links:
            first_park_page = Parser.get_state_extant_parks_link(state_link)
            second_park_page = Parser.get_additional_park_page_links(first_park_page)
            state_park_index_links.append(first_park_page)
            if second_park_page is not None:
                state_park_index_links.append(second_park_page)

        park_links = []
        for park_link in state_park_index_links:
            next_park_links = Parser.get_park_page_links(park_link, Parser.visited_parks_and_rides)
            park_links.extend(next_park_links)

        # Parse coaster data and store in a dataframe
        coaster_data = []
        coaster_to_park_mapping = {}  # Map coaster IDs to parks

        for park_link in park_links:
            next_coaster_links = Parser.get_park_coaster_page_links(park_link, Parser.visited_parks_and_rides)
            for next_coaster_link in next_coaster_links:
                coaster = Parser.parse_coaster(next_coaster_link)
                coaster_data.append(coaster)
                coaster_id = coaster[0]  # The first column is the coaster ID
                coaster_park = coaster[2]  # Assuming "Park" is the third column
                if coaster_park not in coaster_to_park_mapping:
                    coaster_to_park_mapping[coaster_park] = []
                coaster_to_park_mapping[coaster_park].append(coaster_id)

        # Create coaster dataframe
        coaster_dataframe = pd.DataFrame(coaster_data, columns=coaster_columns)
        coaster_dataframe.to_csv("Visited_Coasterlist.csv")
        coaster_dataframe.to_json("Visited_Coasterlist.json", orient="records", indent=4)

        # Parse parks data and add Coaster_IDs
        parks_data = []
        for park_link in park_links:
            park = Parser.parse_park_page(park_link)
            # Handle None case
            if park is None:
                print(f"Failed to parse park from link: {park_link}")
                continue
            park_name = park[1]  # Assuming park Name is the second field
            # Add coaster IDs for this park
            coaster_ids = coaster_to_park_mapping.get(park_name, [])
            park.append(coaster_ids)
            parks_data.append(park)

        # Create park dataframe
        park_dataframe = pd.DataFrame(parks_data, columns=park_columns)
        park_dataframe.to_csv("Visited_Parklist.csv")
        park_dataframe.to_json("Visited_Parklist.json", orient="records", indent=4)

    ####################################################
    # Count the number of parks and rides
    ####################################################
    def count_parks_and_rides(visited_parks_and_rides):
        total_parks = 0
        total_rides = 0
        for state, parks in visited_parks_and_rides.items():
            total_parks += len(parks)  # Count parks in each state
            for rides in parks.values():
                total_rides += len(rides)  # Count rides in each park

        return total_parks, total_rides


    ####################################################
    # Print visited parks and rides
    ####################################################
    def print_visited_parks_and_rides(parks_and_rides):
        for state, parks in parks_and_rides.items():
            print(f"State: {state}")
            for park, rides in parks.items():
                print(f"  Park: {park}")
                print("    Rides:")
                for ride in rides:
                    print(f"      - {ride}")

    ####################################################
    # Test for missing values
    ####################################################
    def test_missing_values(csv_file, parks_and_rides):
        # Load the CSV file into a pandas DataFrame
        coaster_df = pd.read_csv(csv_file)

        # Normalize park and ride names from the CSV for comparison
        csv_parks_rides = (
            coaster_df.groupby("Park")["Name"].apply(list).to_dict()
        )

        # Compare each park and its coasters in the dictionary
        for state, parks in Parser.visited_parks_and_rides.items():
            for park, coasters in parks.items():
                # Get coasters for the current park from the CSV
                csv_coasters = csv_parks_rides.get(park, [])

                # Identify missing coasters
                missing_coasters = [coaster for coaster in coasters if coaster not in csv_coasters]

                # Print results
                if missing_coasters:
                    print(f"Missing coasters in {park}, {state}:")
                    for coaster in missing_coasters:
                        print(f"  - {coaster}")

    ####################################################
    # Parse through a single page of existant coasters
    ####################################################
    #def parse_extant_coasters_page(extant_link):
        #response = requests.get(extant_link)
        #soup = bs(response.text, "html.parser")  # Create Responser
        #coasters_on_page = soup.body.section.find("div", {"class": "stdtbl rer"}).find("table").find_all(
        #    "tr")  # Find table references of coasters on the next page
        #coaster_data_array = [[] for r in range(len(coasters_on_page))]  # Store data in an array
        # print(coaster_data_array)
        # num_extants = soup.body.find("table").select_one("tr:nth-child(1)").td.a.get_text()                              #Get total number of extisting coasters in the country

        ##For first coaster data stats##
        #coaster_link = "https://rcdb.com" + coasters_on_page[1].select_one("td:nth-child(2)").a.get(
        #    "href")  # Next coaster link
        #print("Getting the first coaster: " + str(0) + " at " + coaster_link)
        #coaster_data_array[0] = Parser.parse_coaster(coaster_link)
        #time.sleep(5)

        ##Get the next coaster data stats##
        #for i in range(2, len(coasters_on_page)):
            ## If the coaster page contains no image (Clean up logic here in the future)
        #    if coasters_on_page[i].select_one("td:nth-child(1)").a.get("aria-label") == None:
        #        coaster_link = "https://rcdb.com" + coasters_on_page[i].select_one("td:nth-child(1)").a.get(
        #            "href")  # Next coaster link
        #    else:
        #        coaster_link = "https://rcdb.com" + coasters_on_page[i].select_one("td:nth-child(2)").a.get(
        #            "href")  # Next coaster link
        #    print("Getting the next coaster stats: " + str(i) + " at " + coaster_link + "\n\n")
        #    coaster_data_array[i] = Parser.parse_coaster(
        #        coaster_link)  # Get the next coaster data stats
        #    print(coaster_data_array[i])
        #    time.sleep(20)
        #    col_names = ['Name', 'Park', 'City', 'State', 'Country', 'Status', 'Status Date', 'Material', 'Seating',
        #                 'Thrill', 'Make', 'Model', 'Length', 'Height', 'Drop', 'Speed', 'Inversions', 'VerticalAngle',
        #                 'Duration', 'G-Force']
        #_ = pd.DataFrame(coaster_data_array, columns=col_names)
        #return _

    ####################################################
    # Parse through all the pages of existant coasters
    ####################################################
    #def parse_extant_coasters():
        #columns = ["Name", "Park", "City", "State", "Country", "Status", "Status Date", "Material", "Seating", "Thrill",
        #           "Make", "Model", "Length", "Height", "Drop", "Speed", "Inversions", "VerticalAngle", "Duration",
        #           "G-Force"]
        #link = "https://rcdb.com/r.htm?ot=2&ex&ol=59"  # List of existing coasters in the US (page 1)
        #response = requests.get(link)  # Get Response
        #soup = bs(response.text, "html.parser")  # Create Responser
        #num_extants = soup.body.find("table").select_one(
        #    "tr:nth-child(1)").td.a.get_text()  # Get total number of extisting coasters in the country
        #pages = Parser.get_extant_pages(link)
        #frames = [None] * len(pages)
        #print("frames length: " + str(len(frames)))
        #for i in range(len(pages)):
        #    frames[i] = Parser.parse_extant_coasters_page(pages[i])
        #    time.sleep(2)
        #data_frame = pd.concat(frames)
        #data_frame.set_axis(columns, axis=1)
        #data_frame.to_csv("US_Coaster_Stats_2021.csv")

    #####################################################
    # Return an array of links to extant coasters from a state
    #####################################################
    #def get_state_coasters_list(extant_link):
        #response = requests.get(extant_link)  # Create response
        #soup = bs(response.text, "html.parser")  # Parse response
        #extants = soup.find("body").find("tbody").find_all("tr")  # Find table of extant coasters
        #refs = [None] * len(extants)  # Create array of links to extant coasters
        #for i in range(len(extants)):
            #name = extants[i].select_one('td:nth-child(2)').find("a").get_text()
            #ref = "https://rcdb.com" + extants[i].select_one('td:nth-child(2)').find("a").get("href")
            #refs[i] = ref  # Populate the references array with the next reference
            #print("Found coaster " + name + " at " + ref)

    #####################################################
    # Return a link to the extant coasters of a state page
    # Must include a link to a state page
    #####################################################
    #def get_state_extant_coasters_link(state_link):
        #response = requests.get(state_link)  # Create response
        #soup = bs(response.text, "html.parser")  # Parse the response
        #name = soup.find("body").find("h1").get_text()
        #time.sleep(randint(1, 2))
        #extant_ref = soup.find("table").find_all("tr")  # Find tr's within the table body
        #extant_ref = extant_ref[0].find("td").find("a").get("href")  # Extract first table reference to get the url href
        #extant_ref = "https://rcdb.com" + extant_ref  # Format url
        #print(name, "'s extant coasters are located at: ", extant_ref)
        #return extant_ref

#####################################################
# Main
#####################################################
def main():
    print(str(int(len("hello"))))
    Parser.parse_visited_parks()

if __name__ == '__main__':
    main()
