import random
LOCATIONS = [
    "Airplane", "Bank", "Beach", "Circus Tent", "Corporate Party",
    "Crusader Army", "Day Spa", "Embassy", "Hospital", "Hotel",
    "Military Base", "Movie Studio", "Ocean Liner", "Passenger Train",
    "Pirate Ship", "Polar Station", "Police Station", "Restaurant",
    "School", "Service Station", "Space Station", "Submarine",
    "Supermarket", "Theater", "University",
    "Wedding", "Zoo"
]

ROLES_PER_LOCATION = {
    "Airplane": ["Pilot", "Flight Attendant", "Passenger", "Mechanic", "Air Marshal"],
    "Bank": ["Teller", "Manager", "Customer", "Security Guard", "Robber"],
    "Beach": ["Surfer", "Lifeguard", "Sunbather", "Sandcastle Builder", "Seagull"],
    "Circus Tent": ["Ringmaster", "Clown", "Acrobat", "Lion Tamer", "Ticket Seller"],
    "Corporate Party": ["CEO", "Secretary", "Intern", "DJ", "Caterer"],
    "Crusader Army": ["Knight", "Squire", "Archer", "Monk", "Siege Engineer"],
    "Day Spa": ["Masseuse", "Client", "Yoga Instructor", "Manicurist", "Sauna Attendant"],
    "Embassy": ["Ambassador", "Translator", "Security Officer", "Consul", "Protocol Officer"],
    "Hospital": ["Doctor", "Nurse", "Patient", "Surgeon", "Janitor"],
    "Hotel": ["Receptionist", "Bellhop", "Housekeeper", "Guest", "Chef"],
    "Military Base": ["General", "Soldier", "Medic", "Engineer", "Spy"],
    "Movie Studio": ["Director", "Actor", "Cameraman", "Makeup Artist", "Stunt Double"],
    "Ocean Liner": ["Captain", "Navigator", "Steward", "Deckhand", "Entertainer"],
    "Passenger Train": ["Conductor", "Engineer", "Ticket Inspector", "Passenger", "Dining Car Attendant"],
    "Pirate Ship": ["Captain", "First Mate", "Boatswain", "Gunner", "Parrot"],
    "Polar Station": ["Scientist", "Meteorologist", "Explorer", "Mechanic", "Polar Bear Guard"],
    "Police Station": ["Detective", "Officer", "Suspect", "Dispatcher", "Forensic Expert"],
    "Restaurant": ["Chef", "Waiter", "Customer", "Sommelier", "Dishwasher"],
    "School": ["Teacher", "Student", "Principal", "Janitor", "Librarian"],
    "Service Station": ["Mechanic", "Cashier", "Customer", "Tow Truck Driver", "Car Wash Attendant"],
    "Space Station": ["Astronaut", "Mission Control", "Engineer", "Scientist", "Alien"],
    "Submarine": ["Captain", "Sonar Operator", "Navigator", "Helmsman", "Cook"],
    "Supermarket": ["Cashier", "Stock Clerk", "Customer", "Butcher", "Security Guard"],
    "Theater": ["Actor", "Director", "Stagehand", "Usher", "Lighting Technician"],
    "University": ["Professor", "Student", "Dean", "Librarian", "Researcher"],
    "Wedding": ["Groom", "Bride", "Best Man", "Maid of Honor", "Photographer"],
    "Zoo": ["Zookeeper", "Veterinarian", "Visitor", "Animal Trainer", "Gift Shop Clerk"]
}

class GameError(Exception):
    pass

class GameState:
    def __init__(self, location, roles):
        self.location = location
        self.roles = roles  # dict player_id -> role
        self.votes = {}

def assign_roles(players, location):
    roles = ROLES_PER_LOCATION[location][:]
    random.shuffle(roles)
    # assign roles, one is Spy
    assigned = {}
    spy_index = random.randint(0, len(players)-1)
    for i, player in enumerate(players):
        if i == spy_index:
            assigned[player] = "Spy"
        else:
            assigned[player] = roles[i % len(roles)]
    return assigned
