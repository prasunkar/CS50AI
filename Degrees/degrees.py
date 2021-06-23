import csv
import sys

from util import Node, QueueFrontier

# names  - Maps names to a set of corresponding person_ids.
# people - Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
# movies - Maps movie_ids to a dictionary of: title, year, stars -> (a set of person_ids)
names, people, movies = {}, {}, {}

def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people from people.csv
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Loop through all rows and append a new dictionary per actor/actress
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }

            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

        print("'people.csv' loaded successfully")

    # Load movies from movies.csv
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Loop through all rows and append a new dictionary per movie
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

        print("'movies.csv' loaded successfully")

    # Load stars from stars.csv
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Loop through all rows and append a new dictionary per star
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

        print("'stars.csv'  loaded successfully")


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")

    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...\n")
    load_data(directory)
    print("\nAll data loaded.")

    run_again = True

    while run_again:
        # Receive user input for source, return None if not found
        source_input = input("\nEnter your source name.\n>> ")
        source = person_id_for_name(source_input.strip())
        if source is None:
            sys.exit(f"\n(!) That person was not found.")

        # Receive user input for target, return None if not found
        target_input = input("\nEnter your target name.\n>> ")
        target = person_id_for_name(target_input.strip())
        if target is None:
            sys.exit("\n(!) That person was not found.")

        print("\nWorking...")
        path = shortest_path(source, target)

        if path is None:
            print(f"\nIt seems like {source_input} and {target_input} are not connected.")
        else:
            degrees = len(path)
            print(f"\nSuccess! There are {degrees} degrees of separation.\n")
            path = [(None, source)] + path

            # Loop through the successful branch and print the results
            for i in range(degrees):
                person1 = people[path[i][1]]["name"]
                person2 = people[path[i + 1][1]]["name"]
                movie = movies[path[i + 1][0]]["title"]

                print(f"({i + 1}) {person1} and {person2} starred in {movie}")

        # Allows the user to run multiple searches without restarting the script
        run_again = input("\nWant to run the program again? (y/n)\n>> ").lower().strip()[0] == 'y'


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # Initiate the starting node, frontier and explored node set
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)
    nodes_explored = set()

    while True:
        
        # Return if the frontier is empty of available nodes
        if frontier.empty():
            return None

        # Pick the next available node from the frontier
        current_node = frontier.remove()

        # Iterate through the neighbours of the current node
        for movie, person in neighbors_for_person(current_node.state):
            if not frontier.contains_state(person) and person not in nodes_explored:
                new_node = Node(state=person, parent=current_node, action=movie)

                # Check if the highlighted node is our target
                if person == target:
                    solution = list()
                    
                    while new_node.parent is not None:
                        solution.append((new_node.action, new_node.state))
                        new_node = new_node.parent
                    
                    solution.reverse()  
                    return solution
                else:
                    frontier.add(new_node)

        # Mark the current node as 'explored'
        nodes_explored.add(current_node.state)


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))

    if len(person_ids) == 0:
        return None

    # Triggered if there is more than one person with the same name
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")

        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")

        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass

        return None

    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    
    # Loop through all movies with a given person and find actors/actresses that starred in the same movies
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    
    return neighbors


if __name__ == "__main__":
    main()