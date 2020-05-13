import pandas as pd

class State():

    def __init__(self, id : int, name : str, description : str):
        self.id = id
        self.name = name
        self.description = description

    def __str__(self):
        return "{0}:{1} - {2}".format(self.id, self.name, self.description)

class StateTransitionFactory:

    def __init__(self, states_file_name : str, transitions_file_name : str):

        self.states_file_name = states_file_name
        self.transitions_file_name = transitions_file_name
        self.states = None
        self.transitions = None

    def load(self):

        self.states = pd.read_csv(self.states_file_name, index_col="ID")
        self.transitions = pd.read_csv(self.transitions_file_name, index_col="Current state")

    # Returns the state with the specified ID
    def get_state(self, id):

        if id not in self.states.index:
            return None
        else:
            s = self.states.loc[id]
            return State(id, s["Name"], s["Description"])

    def print(self):
        for state in self._states.values():
            print(str(state))

    def get_transitions_for_state(self, state_id : str):

        if state_id in self.transitions.index:
            transitions = self.transitions.loc[state_id]
        else:
            transitions = None

        return transitions


    def print(self):
        for key, value in self._state_transitions.items():
            print("{0}:{1}".format(key, str(value)))


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
                #raise (Exception("You cancelled. No %s selected" % object_type))
                break
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

    # Load in thh state transitions
    state_transitions = StateTransitionFactory(file_name / "states.csv", file_name / "state_transitions.csv")
    state_transitions.load()
    #state_transitions.print()

    # Start from state 0
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
        current_state = state_transitions.get_state(current_state_id)

        if current_state is None:
            print(f'State {current_state_id} not found')
            break

        print("{0}".format(str(current_state.description)))

        if current_state_id in score_states:
            print("happiness: {0}\nhealth: {1}\nhunger: {2}\nmoney: {3}\nyour health: {4}".format(total_happiness, total_health, total_hunger, total_money, total_your_health))
        x=input()

        # What are the available options from the current state?
        available_transitions = state_transitions.get_transitions_for_state(current_state_id)

        # If there are no options then we have reached an end state so time to finish
        if available_transitions is None:
            print("no available choices for this state")
            loop = False

        # Otherwise...
        else:

            available_inputs = list(available_transitions["Input"])

            # Present valid list of inputs and ask user to pick one
            result = pick("Input",available_inputs,auto_pick=True)

            if result is not None:

                # Change state
                selected_transition = available_transitions.loc[available_transitions["Input"] == result]

                selected_transition = selected_transition.to_dict('index')[current_state_id]


                current_state_id = selected_transition["Next State"]
                happiness = selected_transition["happiness"]
                health = selected_transition["health"]
                hunger = selected_transition["hunger"]
                money = selected_transition["money"]
                your_health = selected_transition["your_health"]
                output = selected_transition["Output"]

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
