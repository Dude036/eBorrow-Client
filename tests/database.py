#!/usr/bin/python3

import simplejson as json
from imdb import IMDb, IMDbError
from pprint import pprint
import hashlib
import sys
import re

database_add = []
database_remove = []
database_requests = []

MONTHS = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}


def create_unique_id(item):
    return hashlib.md5(str(item["Permanent Owner"] + item["Category"] + item["Subcategory"] + item["Name"]).encode()).hexdigest()


def add_to_database(user_db, item):
    item_hash = create_unique_id(item)
    if item_hash in list(user_db.keys()):
        print("Duplicate Key for Item")
        return False
    else:
        del user_db[item_hash]
        return True


def remove_from_database(user_db, item):
    item_hash = create_unique_id(item)
    if item_hash not in list(user_db.keys()):
        print("KeyError: Not in User Database")
        return False
    else:
        user_db[item_hash] = item
        return True


def create_dict_item(owner, category, subcategory, name, identifier=''):
    if not isinstance(owner, str):
        print("Got '", type(owner), "', expected a string.")
        return None
    if not isinstance(category, str):
        print("Got '", type(category), "', expected a string.")
        return None
    if not isinstance(subcategory, str):
        print("Got '", type(subcategory), "', expected a string.")
        return None
    if not isinstance(name, str):
        print("Got '", type(name), "', expected a string.")
        return None
    temp_item = {
        "Current Owner": owner,
        "Permanent Owner": owner,
        "Category": category,
        "Subcategory": subcategory,
        "Name": name,
        "Groups": [],
        "Type Info": {},
        "Image": '',
        "User Tags": [],
    }

    if category == 'Entertainment' and (subcategory == 'Movie' or subcategory == 'TV'):
        temp_item['Type Info'] = {
            "Cast": [],
            "Day": 0,
            "Month": 0,
            "Year": 0,
            "Genres": [],
            "Rating": "",
            "Id": identifier
        }
    elif category == 'Entertainment' and subcategory == 'Game':
        temp_item['Type Info'] = {
            "Day": 0,
            "Month": 0,
            "Year": 0,
            "Platform": "",
            "Publisher": "",
            "Rating": "",
            "Genres": [],
            "Id": identifier
        }
    elif category == 'Entertainment' and subcategory == 'Book':
        temp_item['Type Info'] = {
            "authors": [],
            "Edition": 0,
            "Genres": [],
            "Day": 0,
            "Month": 0,
            "Year": 0,
            "Id": identifier
        }
    return temp_item


def imdb_date(air_date):
    # Data Regex        (1 or more digits) (3 word characters) (1 or more digits)
    match = re.match(r'(\d+) ([\w]{3}) (\d+)', air_date)
    month = MONTHS[match.group(2)]
    day = int(match.group(1))
    year = int(match.group(3))

    return month, day, year


def match_imdb_item(item):
    query = item['Type Info']['Id']
    print("Query:", query)
    scraper = IMDb()
    try:
        movie = scraper.get_movie(query)

        if movie['title'] is None:
            # Unable to get the information.
            print("I didn't find shit!")
            return False
        else:
            cast_list = []
            for director in movie['directors']:
                cast_list.append(str(director['name']))
            for member in movie['cast']:
                cast_list.append(str(member['name']))

            # Get the Date
            item['Type Info']['Month'], item['Type Info']['Day'], item['Type Info']['Year'] = imdb_date(movie['original air date'])
            item['Type Info']['Cast'] = cast_list
            item['Type Info']['Genres'] = movie['genres']
            item['Image'] = movie['cover url']

            # Get the Rating from all certificates
            for cert in movie['certificates']:
                if 'United States' in cert:
                    match = re.match(r'United States\:([A-Za-z \-0-9]+):*', cert)
                    if match is None:
                        print('\t| Unable to resolve this Regex |:' + cert)
                    else:
                        item['Type Info']['Rating'] = match.group(1)

    except IMDbError as e:
        print("IMDB messed up")
        print(e)
        return False
    except AttributeError as e:
        print(e)
        return False
    except KeyError as e:
        print(e)
        return False
    except:
        print("Something unexpected happened!")
        print(sys.exc_info()[0])
        return False
    # pprint(item)
    return True


if __name__ == '__main__':
    Top_250_Movies = {
        "The Shawshank Redemption": '0111161',
        "The Godfather": '0068646',
        "The Godfather: Part II": '0071562',
        "The Dark Knight": '0468569',
        "12 Angry Men": '0050083',
        "Schindler's List": '0108052',
        "The Lord of the Rings: The Return of the King": '0167260',
        "Pulp Fiction": '0110912',
        "The Good, the Bad and the Ugly": '0060196',
        "Fight Club": '0137523',
        "The Lord of the Rings: The Fellowship of the Ring": '0120737',
        "Forrest Gump": '0109830',
        "Star Wars: Episode V - The Empire Strikes Back": '0080684',
        "Inception": '1375666',
        "The Lord of the Rings: The Two Towers": '0167261',
        "One Flew Over the Cuckoo's Nest": '0073486',
        "Goodfellas": '0099685',
        "The Matrix": '0133093',
        "Seven Samurai": '0047478',
        "Se7en": '0114369',
        "City of God": '0317248',
        "Star Wars: Episode IV - A New Hope": '0076759',
        "The Silence of the Lambs": '0102926',
        "It's a Wonderful Life": '0038650',
        "Life Is Beautiful": '0118799',
        "Spider-Man: Into the Spider-Verse": '4633694',
        "The Usual Suspects": '0114814',
        "Spirited Away": '0245429',
        "Saving Private Ryan": '0120815',
        "Léon: The Professional": '0110413',
        "The Green Mile": '0120689',
        "Interstellar": '0816692',
        "Psycho": '0054215',
        "American History X": '0120586',
        "City Lights": '0021749',
        "Once Upon a Time in the West": '0064116',
        "Casablanca": '0034583',
        "Modern Times": '0027977',
        "The Pianist": '0253474',
        "The Intouchables": '1675434',
        "The Departed": '0407887',
        "Back to the Future": '0088763',
        "Terminator 2: Judgment Day": '0103064',
        "Whiplash": '2582802',
        "Raiders of the Lost Ark": '0082971',
        "The Lion King": '0110357',
        "Gladiator": '0172495',
        "The Prestige": '0482571',
        "Apocalypse Now": '0078788',
        "Memento": '0209144',
        "Alien": '0078748',
        "Cinema Paradiso": '0095765',
        "The Great Dictator": '0032553',
        "Grave of the Fireflies": '0095327',
        "Sunset Boulevard": '0043014',
        "The Lives of Others": '0405094',
        "Avengers: Infinity War": '4154756',
        "Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb": '0057012',
        "Paths of Glory": '0050825',
        "The Shining": '0081505',
        "Django Unchained": '1853728',
        "WALL·E": '0910970',
        "Princess Mononoke": '0119698',
        "Witness for the Prosecution": '0051201',
        "Oldboy": '0364569',
        "The Dark Knight Rises": '1345836',
        "American Beauty": '0169547',
        "Aliens": '0090605',
        "Once Upon a Time in America": '0087843',
        "Coco": '2380307',
        "Das Boot": '0082096',
        "Citizen Kane": '0033467',
        "Braveheart": '0112573',
        "Vertigo": '0052357',
        "North by Northwest": '0053125',
        "Reservoir Dogs": '0105236',
        "Star Wars: Episode VI - Return of the Jedi": '0086190',
        "Your Name.": '5311514',
        "M": '0022100',
        "Amadeus": '0086879',
        "Dangal": '5074352',
        "Requiem for a Dream": '0180093',
        "Like Stars on Earth": '0986264',
        "Lawrence of Arabia": '0056172',
        "Eternal Sunshine of the Spotless Mind": '0338013',
        "3 Idiots": '1187043',
        "2001: A Space Odyssey": '0062622',
        "A Clockwork Orange": '0066921',
        "Toy Story": '0114709',
        "Amélie": '0211915',
        "Double Indemnity": '0036775',
        "Singin' in the Rain": '0045152',
        "Taxi Driver": '0075314',
        "Inglourious Basterds": '0361748',
        "Full Metal Jacket": '0093058',
        "Bicycle Thieves": '0040522',
        "To Kill a Mockingbird": '0056592',
        "The Kid": '0012349',
        "The Sting": '0070735',
        "Good Will Hunting": '0119217',
        "Toy Story 3": '0435761',
        "The Hunt": '2106476',
        "Snatch": '0208092',
        "Scarface": '0086250',
        "Monty Python and the Holy Grail": '0071853',
        "For a Few Dollars More": '0059578',
        "The Apartment": '0053604',
        "Metropolis": '0017136',
        "L.A. Confidential": '0119488',
        "A Separation": '1832382',
        "Indiana Jones and the Last Crusade": '0097576',
        "Rashomon": '0042876',
        "Up": '1049413',
        "All About Eve": '0042192',
        "Batman Begins": '0372784',
        "Yojimbo": '0055630',
        "Some Like It Hot": '0053291',
        "Unforgiven": '0105695',
        "Downfall": '0363163',
        "Die Hard": '0095016',
        "The Treasure of the Sierra Madre": '0040897',
        "Heat": '0113277',
        "Andhadhun": '8108198',
        "Ikiru": '0044741',
        "Incendies": '1255953',
        "Raging Bull": '0081398',
        "The Great Escape": '0057115',
        "Children of Heaven": '0118849',
        "Pan's Labyrinth": '0457430',
        "My Father and My Son": '0476735',
        "Chinatown": '0071315',
        "The Third Man": '0041959',
        "My Neighbor Totoro": '0096283',
        "Howl's Moving Castle": '0347149',
        "Ran": '0089881',
        "Judgment at Nuremberg": '0055031',
        "The Secret in Their Eyes": '1305806',
        "Bohemian Rhapsody": '1727824',
        "The Bridge on the River Kwai": '0050212',
        "A Beautiful Mind": '0268978',
        "Lock, Stock and Two Smoking Barrels": '0120735',
        "Casino": '0112641',
        "Three Billboards Outside Ebbing, Missouri": '5027774',
        "On the Waterfront": '0047296',
        "The Seventh Seal": '0050976',
        "Inside Out": '2096673',
        "The Elephant Man": '0080678',
        "The Wolf of Wall Street": '0993846',
        "Room": '3170832',
        "V for Vendetta": '0434409',
        "Mr. Smith Goes to Washington": '0031679',
        "Warrior": '1291584',
        "Blade Runner": '0083658',
        "Dial M for Murder": '0046912',
        "Wild Strawberries": '0050986',
        "The General": '0017925',
        "No Country for Old Men": '0477348',
        "Trainspotting": '0117951',
        "There Will Be Blood": '0469494',
        "The Sixth Sense": '0167404',
        "Gone with the Wind": '0031381',
        "The Thing": '0084787',
        "Fargo": '0116282',
        "Gran Torino": '1205489',
        "The Deer Hunter": '0077416',
        "Finding Nemo": '0266543',
        "Come and See": '0091251',
        "Sherlock Jr.": '0015324',
        "The Big Lebowski": '0118715',
        "Shutter Island": '1130884',
        "Kill Bill: Vol. 1": '0266697',
        "Cool Hand Luke": '0061512',
        "Rebecca": '0032976',
        "Tokyo Story": '0046438',
        "Mary and Max": '0978762',
        "Hacksaw Ridge": '2119532',
        "Gone Girl": '2267998',
        "How to Train Your Dragon": '0892769',
        "Sunrise": '0018455',
        "Wild Tales": '3011894',
        "Jurassic Park": '0107290',
        "Into the Wild": '0758758',
        "The Truman Show": '0120382',
        "In the Name of the Father": '0107207',
        "The Grand Budapest Hotel": '2278388',
        "Life of Brian": '0079470',
        "Stand by Me": '0092005',
        "It Happened One Night": '0025316',
        "Platoon": '0091763',
        "The Bandit": '0116231',
        "Stalker": '0079944',
        "Network": '0074958',
        "Memories of Murder": '0353969',
        "Persona": '0060827',
        "Ben-Hur": '0052618',
        "Hotel Rwanda": '0395169',
        "12 Years a Slave": '2024544',
        "Million Dollar Baby": '0405159',
        "The Wages of Fear": '0046268',
        "Before Sunrise": '0112471',
        "Rush": '1979320',
        "Mad Max: Fury Road": '1392190',
        "The 400 Blows": '0053198',
        "Prisoners": '1392214',
        "Hachi: A Dog's Tale": '1028532',
        "Spotlight": '1895587',
        "Logan": '3315342',
        "Amores Perros": '0245712',
        "Rang De Basanti": '0405508',
        "The Princess Bride": '0093779',
        "Catch Me If You Can": '0264464',
        "Nausicaä of the Valley of the Wind": '0087544',
        "Harry Potter and the Deathly Hallows: Part 2": '1201607',
        "Butch Cassidy and the Sundance Kid": '0064115',
        "Rocky": '0075148',
        "Barry Lyndon": '0072684',
        "Monsters, Inc.": '0198781',
        "The Grapes of Wrath": '0032551',
        "The Maltese Falcon": '0033870',
        "Dead Poets Society": '0097165',
        "The Terminator": '0088247',
        "Donnie Darko": '0246578',
        "Gandhi": '0083987',
        "Diabolique": '0046911',
        "La Haine": '0113247',
        "Groundhog Day": '0107048',
        "The Wizard of Oz": '0032138',
        "In the Mood for Love": '0118694',
        "The Nights of Cabiria": '0050783',
        "Jaws": '0073195',
        "The Help": '1454029',
        "Tangerines": '2991224',
        "The Handmaiden": '4016934',
        "Sanjuro": '0056443',
        "Before Sunset": '0381681',
        "Drishyam": '4430212',
        "Paper Moon": '0070510',
        "Paris, Texas": '0087884',
        "Castle in the Sky": '0092067',
        "Gangs of Wasseypur": '1954470',
        "The Best Years of Our Lives": '0036868',
        "Pirates of the Caribbean: The Curse of the Black Pearl": '0325980',
        "Fanny and Alexander": '0083922',
        "Guardians of the Galaxy": '2015381',
        "Three Colors: Red": '0111495',
        "8½": '0056801',
    }

    Top_250_TV = {
        "Planet Earth II": '5491994',
        "Band of Brothers": '0185906',
        "Game of Thrones": '0944947',
        "Planet Earth": '0795176',
        "Breaking Bad": '0903747',
        "The Wire": '0306414',
        "Cosmos: Possible Worlds": '2395695',
        "Blue Planet II": '6769208',
        "Rick and Morty": '2861424',
        "Cosmos": '0081846',
        "The Sopranos": '0141842',
        "The World at War": '0071075',
        "Avatar: The Last Airbender": '0417299',
        "Life": '1533395',
        "Sherlock": '1475582',
        "The Vietnam War": '1877514',
        "Human Planet": '1806234',
        "The Twilight Zone": '0052520',
        "Dekalog": '0092337',
        "The Civil War": '0098769',
        "Firefly": '0303461',
        "Fullmetal Alchemist: Brotherhood": '1355642',
        "True Detective": '2356777',
        "Fargo": '2802850',
        "Last Week Tonight with John Oliver": '3530232',
        "Batman: The Animated Series": '0103359',
        "Death Note": '0877057',
        "The Blue Planet": '0296310',
        "Cowboy Bebop": '0213338',
        "Black Mirror": '2085059',
        "One Punch Man: Wanpanman": '4508902',
        "Sahsiyet": '7920978',
        "Pride and Prejudice": '0112130',
        "Monty Python's Flying Circus": '0063929',
        "Frozen Planet": '2092588',
        "Das Boot": '0081834',
        "Africa": '2571774',
        "Friends": '0108778',
        "Stranger Things": '4574334',
        "Seinfeld": '0098904',
        "Only Fools and Horses....": '0081912',
        "Arrested Development": '0367279',
        "Apocalypse: The Second World War": '1508238',
        "Twin Peaks": '0098936',
        "Gravity Falls": '1865718',
        "Over the Garden Wall": '3718778',
        "House of Cards": '1856010',
        "Narcos": '2707408',
        "Freaks and Geeks": '0193676',
        "Westworld": '0475784',
        "I, Claudius": '0074006',
        "The Office": '0386676',
        "TVF Pitchers": '4742876',
        "Fawlty Towers": '0072500',
        "Cobra Kai": '7221388',
        "Blackadder Goes Forth": '0096548',
        "Peaky Blinders": '2442560',
        "Rome": '0384766',
        "The Haunting of Hill House": '6763664',
        "Oz": '0118421',
        "The Simpsons": '0096697',
        "It's Always Sunny in Philadelphia": '0472954',
        "Attack on Titan": '2560140',
        "South Park": '0121955',
        "The West Wing": '0200276',
        "House": '0412142',
        "Nathan for You": '2297757',
        "The Jinx: The Life and Deaths of Robert Durst": '4299972',
        "Curb Your Enthusiasm": '0264235',
        "Lonesome Dove": '0096639',
        "Chappelle's Show": '0353049',
        "Dragon Ball Z": '0214341',
        "Deadwood": '0348914',
        "The Adventures of Sherlock Holmes": '0086661',
        "The Marvelous Mrs. Maisel": '5788792',
        "Battlestar Galactica": '0407362',
        "Better Call Saul": '3032476',
        "Dragon Ball Z": '0121220',
        "Steins;Gate": '1910272',
        "Six Feet Under": '0248654',
        "The Crown": '4786824',
        "The Thick of It": '0459159',
        "The Return of Sherlock Holmes": '0090509',
        "The Memoirs of Sherlock Holmes": '0108855',
        "Top Gear": '1628033',
        "The X-Files": '0106179',
        "The Shield": '0286486',
        "This Is Us": '5555260',
        "Dexter": '0773262',
        "Archer": '1486217',
        "Downton Abbey": '1606375',
        "Monster": '0434706',
        "Black-Adder II": '0088484',
        "From the Earth to the Moon": '0120570',
        "Daredevil": '3322312',
        "Making a Murderer": '5189670',
        "Sacred Games": '6077448',
        "Young Justice": '1641384',
        "North &amp; South": '0417349',
        "Bron/Broen": '1733785',
        "Star Trek: The Next Generation": '0092455',
        "Parks and Recreation": '1266020',
        "Code Geass: Lelouch of the Rebellion": '0994314',
        "Masum": '6478318',
        "Black Adder the Third": '0092324',
        "Battlestar Galactica": '0314979',
        "Long Way Round": '0403778',
        "Mind Your Language": '0075537',
        "Shameless": '1586680',
        "Fullmetal Alchemist": '0421357',
        "Spaced": '0187664',
        "Gomorrah": '2049116',
        "Doctor Who": '0436992',
        "Mad Men": '0804503',
        "Through the Wormhole": '1513168',
        "Samurai X: Trust and Betrayal": '0203082',
        "The Grand Tour": '5712554',
        "Atlanta": '4288182',
        "The Bugs Bunny Show": '0053488',
        "Leyla and Mecnun": '1831164',
        "QI": '0380136',
        "Friday Night Lights": '0758745',
        "Skam": '5288312',
        "The Defiant Ones": '6958022',
        "The Punisher": '5675620',
        "Saint Seiya": '0161952',
        "Chef's Table": '4295140',
        "Father Ted": '0111958',
        "Peep Show": '0387764',
        "Justice League": '0275137',
        "Flight of the Conchords": '0863046',
        "Yes Minister": '0080306',
        "Neon Genesis Evangelion": '0112159',
        "The Newsroom": '1870479',
        "Justified": '1489428',
        "Generation Kill": '0995832',
        "Hunter x Hunter": '2098220',
        "Dark": '5753856',
        "Mystery Science Theater 3000": '0094517',
        "Poirot": '0094525',
        "Boardwalk Empire": '0979432',
        "Big Little Lies": '3920596',
        "John Adams": '0472027',
        "Adventure Time": '1305826',
        "Yes, Prime Minister": '0086831',
        "The Night Of": '2401256',
        "Louie": '1492966',
        "Brass Eye": '0118273',
        "The Untold History of the United States": '1494191',
        "Yeh Meri Family": '8595766',
        "Berserk": '0318871',
        "Alfred Hitchcock Presents": '0047708',
        "Samurai Champloo": '0423731',
        "Homicide: Life on the Street": '0106028',
        "Mindhunter": '5290382',
        "Coupling": '0237123',
        "Brideshead Revisited": '0083390',
        "Dragon Ball": '0088509',
        "Dragon Ball": '0280249',
        "The IT Crowd": '0487831',
        "Vikings": '2306299',
        "La casa de papel": '6468322',
        "Umbre": '4269716',
        "Feud": '1984119',
        "Dr. Horrible's Sing-Along Blog": '1227926',
        "Mr. Bean": '0096657',
        "Silicon Valley": '2575988',
        "The Office": '0290978',
        "The Handmaid's Tale": '5834204',
        "Impractical Jokers": '2100976',
        "Horace and Pete": '5425186',
        "Whose Line Is It Anyway?": '0163507',
        "The New Batman Adventures": '0118266',
        "Erased": '5249462',
        "Mr. Robot": '4158110',
        "The Eric Andre Show": '2244495',
        "House of Cards": '0098825',
        "Luther": '1474684',
        "BoJack Horseman": '3398228',
        "Twin Peaks": '4093826',
        "Black Books": '0262150',
        "Spartacus: Gods of the Arena": '1758429',
        "Hannibal": '2243973',
        "Line of Duty": '2303687',
        "Narcos: Mexico": '8714904',
        "Tinker Tailor Soldier Spy": '0080297',
        "The Prisoner": '0061287',
        "American Crime Story": '2788432',
        "Ghost in the Shell: Stand Alone Complex": '0346314',
        "Endeavour": '2701582',
        "Sons of Anarchy": '1124373',
        "Futurama": '0149460',
        "Wentworth": '2433738',
        "Sex Education": '7767422',
        "Jesus of Nazareth": '0075520',
        "The Knick": '2937900',
        "Detectorists": '4082744',
        "Ash vs Evil Dead": '4189022',
        "I'm Alan Partridge": '0129690',
        "Spartacus": '1442449',
        "Rurouni Kenshin: Wandering Samurai": '0182629',
        "The Daily Show": '0115147',
        "Community": '1439629',
        "The Venture Bros.": '0417373',
        "Scenes from a Marriage": '0070644',
        "Generation War": '1883092',
        "The Legend of Korra": '1695360',
        "X-Men": '0103584',
        "The Colbert Report": '0458254',
        "Taboo": '3647998',
        "Happy Valley": '3428912',
        "Suits": '1632701',
        "Behzat Ç.: Bir Ankara Polisiyesi": '1795096',
        "Police Squad!": '0083466',
        "Carnivàle": '0319969',
        "Garth Marenghi's Darkplace": '0397150',
        "Samurai Jack": '0278238',
        "One Piece: Wan pîsu": '0388629',
        "Utopia": '2384811',
        "The Angry Video Game Nerd": '1230180',
        "Borgen": '1526318',
        "Inside Look: The People v. O.J. Simpson, American Crime Story": '6205862',
        "Entourage": '0387199',
        "Doctor Who": '0056751',
        "Modern Family": '1442437',
        "State of Play": '0362192',
        "Inside No. 9": '2674806',
        "The Muppet Show": '0074028',
        "Kardes Payi": '3671754',
        "Jeeves and Wooster": '0098833',
        "Fringe": '1119644',
        "Brooklyn Nine-Nine": '2467372',
        "Humorously Yours": '6328940',
        "Billions": '4270492',
        "The Americans": '2149175',
        "The Expanse": '3230854',
        "Broadchurch": '2249364',
        "Supernatural": '0460681',
        "Lost": '0411008',
        "Naruto: Shippûden": '0988824',
        "Babylon Berlin": '4378376',
        "Avrupa Yakasi": '0421291',
        "Stargate SG-1": '0118480',
        "Star Trek": '0060028',
        "Anne with an E": '5421602',
        "Anthony Bourdain: No Reservations": '0475900',
        "Olive Kitteridge": '3012698',
        "Mirzapur": '6473300',
        "Rectify": '2183404',
        "Permanent Roommates": '4156586',
    }

    catalog = {}
    for top in sorted(list(Top_250_Movies.keys())):
        temp_item = create_dict_item("Josh Higham", "Entertainment", "Movie", top, Top_250_Movies[top])
        temp_key = create_unique_id(temp_item)
        if temp_key in list(catalog.keys()):
            print("Duplicate Key:", temp_key)
        else:
            catalog[temp_key] = temp_item

    for top in sorted(list(Top_250_TV.keys())):
        temp_item = create_dict_item("Josh Higham", "Entertainment", "TV", top, Top_250_TV[top])
        temp_key = create_unique_id(temp_item)
        if temp_key in list(catalog.keys()):
            print("Duplicate Key:", temp_key)
        else:
            catalog[temp_key] = temp_item

    for key, value in catalog.items():
        match_imdb_item(value)

    json.dump(catalog, open("db.json", 'w'), sort_keys=True, indent=4)
