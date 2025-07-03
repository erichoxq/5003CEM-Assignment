
class Graph:
    """
    Unweighted directed graph data structure.
    This graph can be used for various applications by keeping vertices generic.
    """

    def __init__(self):
        # Dictionary to store vertices and their outgoing edges
        self.adjacency_list = {}

    def addVertex(self, vertex):
        """Add a new vertex to the graph if it doesn't already exist"""
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
            return True
        return False  # Vertex already exists

    def addEdge(self, source, destination):
        """Connect one vertex with another vertex by adding a directed edge"""
        # Check if both vertices exist, add them if they don't
        if source not in self.adjacency_list:
            self.addVertex(source)
        if destination not in self.adjacency_list:
            self.addVertex(destination)

        # Add edge (avoid duplicates)
        if destination not in self.adjacency_list[source]:
            self.adjacency_list[source].append(destination)
            return True
        return False  # Edge already exists

    def removeEdge(self, source, destination):
        """Remove an edge between source and destination if it exists"""
        if source in self.adjacency_list and destination in self.adjacency_list[source]:
            self.adjacency_list[source].remove(destination)
            return True
        return False  # Edge doesn't exist

    def listOutgoingAdjacencyVertex(self, vertex):
        """For a given vertex, list all vertices where edges are outgoing from this vertex"""
        if vertex in self.adjacency_list:
            return self.adjacency_list[vertex]
        return []  # Vertex doesn't exist

    def getAllVertices(self):
        """Return all vertices in the graph"""
        return list(self.adjacency_list.keys())


class Person:
    """
    Represents a single user of a social media app.
    Contains relevant attributes for a user profile.
    """

    def __init__(self, name, gender=None, biography=None, is_private=False):
        self.name = name
        self.gender = gender
        self.biography = biography
        self.is_private = is_private  # Privacy setting (public/private profile)

    def __str__(self):
        """String representation of a Person"""
        return self.name

    def __repr__(self):
        """Representation of a Person object"""
        return f"Person('{self.name}')"

    def get_profile_info(self):
        """Return profile information based on privacy settings"""
        if self.is_private:
            return {
                "name": self.name,
                "privacy": "Private"
            }
        else:
            return {
                "name": self.name,
                "gender": self.gender,
                "biography": self.biography,
                "privacy": "Public"
            }


class SocialMediaApp:
    """
    A simplified social media app that connects people.
    Uses the Graph data structure to store connections between users.
    """

    def __init__(self):
        self.graph = Graph()
        self.people = {}  # Dictionary to store Person objects by name for quick lookup

    def add_person(self, person):
        """Add a new person to the social media app"""
        if person.name not in self.people:
            self.people[person.name] = person
            self.graph.addVertex(person)
            return True
        return False

    def follow_person(self, follower_name, target_name):
        """Make one person follow another person"""
        if follower_name in self.people and target_name in self.people:
            follower = self.people[follower_name]
            target = self.people[target_name]
            return self.graph.addEdge(follower, target)
        return False

    def unfollow_person(self, follower_name, target_name):
        """Make one person unfollow another person"""
        if follower_name in self.people and target_name in self.people:
            follower = self.people[follower_name]
            target = self.people[target_name]
            return self.graph.removeEdge(follower, target)
        return False

    def get_followed_accounts(self, person_name):
        """Get list of accounts followed by a person"""
        if person_name in self.people:
            person = self.people[person_name]
            return self.graph.listOutgoingAdjacencyVertex(person)
        return None  # User not found

    def get_followers(self, person_name):
        """Get list of accounts that follow a person"""
        if person_name in self.people:
            target = self.people[person_name]
            followers = []
            for person in self.graph.getAllVertices():
                if target in self.graph.listOutgoingAdjacencyVertex(person):
                    followers.append(person)
            return followers
        return None  # User not found

    def get_all_users(self):
        """Get list of all users in the app"""
        return list(self.people.values())

    def get_user_profile(self, name):
        """Get profile information for a user"""
        if name in self.people:
            return self.people[name].get_profile_info()
        return None


def run_social_media_app():
    """Run the social media app with a menu-driven interface"""
    app = SocialMediaApp()

    # Create at least 5 person objects (maximum 10)
    p1 = Person("Eric Ho", "Male", "Software developer from Penang", False)
    p2 = Person("Teh Yao Sheng", "Male", "College student studying Computer Science", True)
    p3 = Person("Tan Hong Zheng", "Male", "Food blogger", False)
    p4 = Person("Vennis", "Female", "Travel enthusiast", False)
    p5 = Person("Teh Kai Shuang", "Female", "Photographer", True)

    # Add people to the app
    app.add_person(p1)
    app.add_person(p2)
    app.add_person(p3)
    app.add_person(p4)
    app.add_person(p5)

    # Set up some initial following relationships
    app.follow_person("Eric Ho", "Teh Yao Sheng")
    app.follow_person("Eric Ho", "Tan Hong Zheng")
    app.follow_person("Teh Yao Sheng", "Eric Ho")
    app.follow_person("Tan Hong Zheng", "Vennis")
    app.follow_person("Vennis", "Teh Kai Shuang")
    app.follow_person("Teh Kai Shuang", "Teh Yao Sheng")
    app.follow_person("Vennis", "Eric Ho")

    while True:
        print("\n===== Social Media App =====")
        print("1. Display all user names")
        print("2. View profile details")
        print("3. View followed accounts")
        print("4. View followers")
        print("5. Add new user profile")
        print("6. Follow a user")
        print("7. Unfollow a user")
        print("0. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            # Display all usernames
            print("\n--- All Users ---")
            users = app.get_all_users()
            for i, user in enumerate(users, 1):
                print(f"{i}. {user.name}")

        elif choice == "2":
            # View profile details
            name = input("Enter the name of the user: ")
            profile = app.get_user_profile(name)
            if profile:
                print(f"\n--- Profile: {name} ---")
                for key, value in profile.items():
                    if value is not None:  # Skip None values
                        print(f"{key.capitalize()}: {value}")
            else:
                print(f"User '{name}' not found.")

        elif choice == "3":
            # View followed accounts
            name = input("Enter the name of the user: ")
            followed = app.get_followed_accounts(name)
            if followed is not None:
                print(f"\n--- Accounts followed by {name} ---")
                if followed:
                    for i, person in enumerate(followed, 1):
                        print(f"{i}. {person.name}")
                else:
                    print(f"{name} is not following anyone.")
            else:
                print(f"User '{name}' not found.")

        elif choice == "4":
            # View followers
            name = input("Enter the name of the user: ")
            followers = app.get_followers(name)
            if followers is not None:
                print(f"\n--- Followers of {name} ---")
                if followers:
                    for i, person in enumerate(followers, 1):
                        print(f"{i}. {person.name}")
                else:
                    print(f"{name} has no followers.")
            else:
                print(f"User '{name}' not found.")

        elif choice == "5":
            # Add new user profile
            name = input("Enter name: ")
            gender = input("Enter gender (or press Enter to skip): ")
            bio = input("Enter biography (or press Enter to skip): ")
            privacy = input("Is this profile private? (yes/no): ").lower() == "yes"

            new_person = Person(
                name=name,
                gender=gender if gender else None,
                biography=bio if bio else None,
                is_private=privacy
            )

            if app.add_person(new_person):
                print(f"User '{name}' added successfully!")
            else:
                print(f"User '{name}' already exists.")

        elif choice == "6":
            # Follow a user
            follower = input("Enter follower name: ")
            target = input("Enter name of user to follow: ")

            if app.follow_person(follower, target):
                print(f"{follower} is now following {target}!")
            else:
                print("Failed to follow. Check that both users exist and aren't already connected.")

        elif choice == "7":
            # Unfollow a user
            follower = input("Enter follower name: ")
            target = input("Enter name of user to unfollow: ")

            if app.unfollow_person(follower, target):
                print(f"{follower} has unfollowed {target}!")
            else:
                print("Failed to unfollow. Check that both users exist and are connected.")

        elif choice == "0":
            print("Thank you for using the Social Media App. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")




if __name__ == "__main__":
    run_social_media_app()
