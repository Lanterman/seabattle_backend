column_name_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

row = "{'A1': '', 'A2': 'qwe', 'A3': '', 'A4': '', 'A5': '12', 'A6': '', 'A7': 'qwe', 'A8': '', 'A9': '', 'A10': ''}"

board = {
    "A": {
        "A1": 27.4,
        "A2": " space 27.3 space 27.4",
        "A3": 27.3,
        "A4": " space 27.3",
        "A5": "",
        "A6": "",
        "A7": "",
        "A8": " space 33.3",
        "A9": " space 33.3",
        "A10": " space 33.3"
    },
    "B": {
        "B1": 27.4,
        "B2": " space 27.3 space 27.4",
        "B3": 27.3,
        "B4": " space 27.3 space 45.2",
        "B5": " space 45.2",
        "B6": " space 39.1 space 45.2",
        "B7": " space 39.1",
        "B8": " space 33.3 space 39.1",
        "B9": 33.3,
        "B10": " space 33.3"
    },
    "C": {
        "C1": 27.4,
        "C2": " space 27.3 space 27.4",
        "C3": "hit",
        "C4": " space 27.3 space 45.2",
        "C5": 45.2,
        "C6": " space 39.1 space 45.2",
        "C7": 39.1,
        "C8": " space 33.3 space 39.1",
        "C9": 33.3,
        "C10": " space 33.3"
    },
    "D": {
        "D1": 27.4,
        "D2": " space 27.3 space 27.4",
        "D3": "hit",
        "D4": " space 27.3 space 45.2",
        "D5": " space 45.2",
        "D6": " space 39.1 space 45.2",
        "D7": 39.1,
        "D8": " space 33.3 space 39.1",
        "D9": 33.3,
        "D10": " space 33.3"
    },
    "E": {
        "E1": " space 27.1 space 27.4",
        "E2": " space 27.1 space 27.3 space 27.4",
        "E3": "miss",
        "E4": " space 27.3",
        "E5": " space 27.2",
        "E6": " space 27.2 space 39.1",
        "E7": " space 27.2 space 39.1",
        "E8": " space 27.2 space 33.3 space 39.1",
        "E9": " space 27.2 space 33.3",
        "E10": " space 27.2 space 33.3"
    },
    "F": {
        "F1": 27.1,
        "F2": " space 27.1 space 33.1",
        "F3": " space 33.1",
        "F4": " space 33.1",
        "F5": " space 27.2",
        "F6": 27.2,
        "F7": 27.2,
        "F8": 27.2,
        "F9": 27.2,
        "F10": " space 27.2"
    },
    "G": {
        "G1": 27.1,
        "G2": " space 27.1 space 33.1",
        "G3": 33.1,
        "G4": " space 33.1",
        "G5": " space 27.2 space 39.2",
        "G6": " space 27.2 space 39.2",
        "G7": " space 27.2 space 39.2",
        "G8": " space 27.2 space 39.2",
        "G9": " space 27.2 space 45.1",
        "G10": " space 27.2 space 45.1"
    },
    "H": {
        "H1": 27.1,
        "H2": " space 27.1 space 33.1",
        "H3": 33.1,
        "H4": " space 33.1",
        "H5": " space 39.2",
        "H6": 39.2,
        "H7": 39.2,
        "H8": " space 39.2",
        "H9": " space 45.1",
        "H10": 45.1
    },
    "I": {
        "I1": 27.1,
        "I2": " space 27.1 space 33.1",
        "I3": 33.1,
        "I4": " space 33.1",
        "I5": " space 33.2 space 39.2",
        "I6": " space 33.2 space 39.2",
        "I7": " space 33.2 space 39.2",
        "I8": " space 33.2 space 39.2",
        "I9": " space 33.2 space 45.1",
        "I10": " space 45.1"
    },
    "J": {
        "J1": " space 27.1",
        "J2": " space 27.1 space 33.1",
        "J3": " space 33.1",
        "J4": " space 33.1",
        "J5": " space 33.2",
        "J6": 33.2,
        "J7": 33.2,
        "J8": 33.2,
        "J9": " space 33.2",
        "J10": ""
    },
}
            
ships = [
    {"id": 27, "name": "fourdeck", "plane": "horizontal", "size": 4, "count": 1},
    {"id": 33, "name": "tripledeck", "plane": "horizontal", "size": 3, "count": 2},
    {"id": 39, "name": "doubledeck", "plane": "horizontal", "size": 2, "count": 3},
    {"id": 45, "name": "singledeck", "plane": "horizontal", "size": 1, "count": 4}
]

messages = [
    {
        "message": "Lanterman want to play again.",
        "owner": "lanterman",
        "is_bot": True,
        "created_in": "18.04.2023 00:23:10"
    },
    {
        "message": "Admin want to play again.",
        "owner": "admin",
        "is_bot": False,
        "created_in": "18.04.2023 00:23:07"
    },
    {
        "message": "Admin connected to the game.",
        "owner": "admin",
        "is_bot": True,
        "created_in": "18.04.2023 00:22:43"
    }
]
