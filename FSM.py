import csv

class State():

    def __init__(self, id : int, name : str, description : str):
        self.id = id
        self.name = name
        self.description = description

    def __str__(self):
        return "{0}:{1} - {2}".format(self.id, self.name, self.description)

class StateTransitionFactory:

    def __init__(self, transitions_file_name : str):

        self.file_name = transitions_file_name

        # a dictionary of state ID to a state transitions
        self._state_transitions = {}

    def load(self):

        # Attempt to open the file
        with open(self.file_name, 'r') as location_file:

            # Load all rows in as a dictionary
            reader = csv.DictReader(location_file)

            # Get the list of column headers
            header = reader.fieldnames

            # For each row in the file....
            for row in reader:

                current_state = int(row.get("Current state"))
                input_name = row.get("Input")
                next_state = int(row.get("Next State"))
                output_name = row.get("Output")
                happiness = int(row.get("happiness"))
                health = int(row.get("health"))
                hunger = int(row.get("hunger"))
                money = int(row.get("money"))
                your_health = int(row.get("money"))


                if current_state not in self._state_transitions.keys():
                    self._state_transitions[current_state] = {}

                self._state_transitions[current_state][input_name] = (next_state, output_name, happiness, health, hunger, money, your_health)

                #logging.info("%s.load(): Loaded Location %i. %s", __class__, new_state.id, new_state.name)

    def get_transitions_for_state(self, state_id : str):

        if state_id not in self._state_transitions.keys():
            return None
        else:
            return self._state_transitions[state_id]

    def print(self):
        for key, value in self._state_transitions.items():
            print("{0}:{1}".format(key, str(value)))

'''
A factory for creating and storing state details for easy access by state ID
'''
class StateFactory():

    def __init__(self, state_file_name : str):

        self.file_name = state_file_name

        # a dictionary of location ID to a state object
        self._states = {}

    @property
    def count(self):
        return len(self._states)

    def load(self):

        # Attempt to open the file
        with open(self.file_name, 'r') as location_file:

            # Load all rows in as a dictionary
            reader = csv.DictReader(location_file)

            # Get the list of column headers
            header = reader.fieldnames

            # For each row in the file....
            for row in reader:
                new_state = State(int(row.get("ID")), \
                                        row.get("Name"), \
                                        row.get("Description"))

                self._states[new_state.id] = new_state


    # Returns the location with the specified ID
    def get_state(self, id):
        if id not in self._states:
            return None
        else:
            return self._states[id]

    def print(self):
        for state in self._states.values():
            print(str(state))

def is_numeric(s):

    try:
        x = int(s)
    except:
        try:
            x = float(s)
        except:
            x = None
    return x

# Function to present a menu to pick an object from a list of objects
# auto_pick means if the list has only one item then automatically pick that item
def pick(object_type: str, objects: list, auto_pick: bool=False):

    selected_object = None
    choices = len(objects)
    vowels ="AEIOU"
    if object_type[0].upper() in vowels:
        a_or_an = "an"
    else:
        a_or_an = "a"

    # If the list of objects is no good the raise an exception
    if objects is None or choices == 0:
        raise(Exception("No %s to pick from." % object_type))

    # If you selected auto pick and there is only one object in the list then pick it
    if auto_pick is True and choices == 1:
        selected_object = objects[0]

    # While an object has not yet been picked...
    while selected_object == None:

        # Print the menu of available objects to select
        print("Select %s %s:-" % (a_or_an, object_type))

        for i in range(0, choices):
            print("\t%i) %s" % (i + 1, str(objects[i])))

        # Along with an extra option to cancel selection
        print("\t%i) Cancel" % (choices + 1))

        # Get the user's selection and validate it
        choice = input("%s?" % object_type)
        if is_numeric(choice) is not None:
            choice = int(choice)

            if 0 < choice <= choices:
                selected_object = objects[choice -1]
            elif choice == (choices + 1):
                raise (Exception("You cancelled. No %s selected" % object_type))
            else:
                print("Invalid choice '%i' - try again." % choice)
        else:
            print("You choice '%s' is not a number - try again." % choice)

    return selected_object


from pathlib import Path

def main():

    print("It is your job to look after Honey Bunny for a week.")
    x = input()
    print("If she is happy when I get back you will get a nice reward!")
    x=input()

    file_name = Path("./")

    # Load in all of the states
    states = StateFactory(file_name / "states.csv")
    states.load()

    # Load in teh state transitions
    state_transitions = StateTransitionFactory(file_name / "state_transitions.csv")
    state_transitions.load()
    #state_transitions.print()

    # Start from state 1
    current_state_id = 0
    total_happiness = 50
    total_hunger = 10
    total_health = 100
    total_money = 1000
    total_your_health = 100
    loop = True
    score_states=[0, 10,16]
    while loop is True:

        # Print the details of the current state
        current_state = states.get_state(current_state_id)
        print("{0}".format(str(current_state.description)))
        if current_state_id in score_states:
            print("happiness: {0}\nhealth: {1}\nhunger: {2}\nmoney: {3}\nyour health: {4}".format(total_happiness, total_health, total_hunger, total_money, total_your_health))
        x=input()

        # What are the available options from the current state?
        available_inputs = state_transitions.get_transitions_for_state(current_state_id)

        # If there are no options then we have reached an end state so time to finish
        if available_inputs is None:
            loop = False

        # Otherwise...
        else:

            # for key, value in available_inputs.items():
            #     next_state, output = value
            #     print("Input {0}: Next state {1}, output {2}".format(key, next_state, output))

            # Present valid list of inputs and ask user to pick one
            result = pick("Input",list(available_inputs.keys()),auto_pick=True)

            if result is not None:

                # Change state
                current_state_id, output, happiness,  health, hunger, money, your_health = available_inputs[result]
                total_happiness+=happiness
                total_health+=health
                total_hunger+=hunger
                total_money+=money
                total_your_health+=your_health


                # Print selection and output
                print("You {0}".format(result))
                x=input()
                print("{0}".format(output))

            else:
                print("Bye bye")
                loop = False

        x=input()



if __name__ == "__main__":
    main()
