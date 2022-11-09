"""
DESCRIPTION OF THE PROGRAM:
Program is used to search different patterns in text.
List of patterns is passed to build function and appropriate trie based on Aho-Corasick is build.
Then text and the tree algorithm are passed to search function, which seeks appropriate pattern in text.
The output of search function is a list.
Each row in the list is the found pattern and the start index of this pattern in the text.
"""


def build(pattern_list):
    # AhoCorasick machine is a list of dictionaries, each node in trie is a dictionary
    machine = [{'state_number': 0, 'label': '', 'next_states': [], 'fail_link': 0, 'out': []}]

    # goes through each pattern in pattern_list
    for pattern in pattern_list:
        # algorithm is case-insensitive, so each pattern is set to lowercase
        pattern = pattern.lower()
        current_state = 0

        # goes through each character in pattern
        for char in pattern:
            # checks if from current_state you can go to given char (if already node exists)
            # if yes current_state is changed
            if find_next_state(current_state, char, machine):
                current_state = find_next_state(current_state, char, machine)
            # if not, new node is created
            else:
                machine.append({'state_number': len(machine), "label": char, "next_states": [], "fail_link": 0, "out": []})
                # when new node is created, the link between current state and new state (node) have to be created
                machine[current_state]["next_states"].append(len(machine) - 1)
                # goes to new state which before was appended as next_state to current_state
                current_state = len(machine) - 1

        # when whole pattern is iterated it is added as output to current_state(node)
        machine[current_state]["out"].append(pattern)

    # returns a machine but first creates fail links using "create_fail_links function
    return create_fail_links(machine)


# function which finds next state of a trie given character and current state in given machine
def find_next_state(current_state, char, machine):
    for state in machine[current_state]["next_states"]:
        if machine[state]["label"] == char:
            return state
    return None


# function which creates fail links in created tree
def create_fail_links(machine):
    # queue which helps to breadth search tree while creating fails links
    queue = []

    # at the beginning every state which is next state of a root state has fail state equals to 0
    for state in machine[0]["next_states"]:
        machine[state]["fail_link"] = 0
        queue.append(state)

    # as long as nodes are in queue
    while len(queue) != 0:
        # FIFO, gets first element from queue (and deletes it from queue)
        element = queue.pop(0)
        # goes through each next_state of element taken from queue
        for child_node in machine[element]["next_states"]:
            state = machine[element]["fail_link"]

            # as long as we can't find node with given character which goes from state
            # and state is not 0 (if state is zero in some cases loop would be infinite)
            while find_next_state(state, machine[child_node]["label"], machine) is None and state != 0:
                # state is equal to fail state of state
                state = machine[state]["fail_link"]

            # sets fail state of child node
            machine[child_node]["fail_link"] = find_next_state(state, machine[child_node]["label"], machine)

            #  the turning edge so-called joker
            if machine[child_node]["fail_link"] is None:
                machine[child_node]["fail_link"] = 0

            # adds to the output of child node, output of a fail state of this child node
            # thanks to it pattern that are in other patterns will be added too
            machine[child_node]["out"] = (machine[child_node]["out"] + machine[machine[child_node]["fail_link"]]["out"])
            # adds child node to a queue
            queue.append(child_node)

    return machine


def search(machine, text):
    # list of list, each item in list is pattern which appears in text and index when it starts
    pattern_indexes = list()
    # it is auxiliary variable, copy of a current_state, at the beginning it is 0 because we always start from node 0
    current_state_copy = 0

    for i in range(len(text)):
        # looks for a next state with label == text[i]
        # thanks to the copy we are sure that in "find_next_state" function state is not None
        current_state = find_next_state(current_state_copy, text[i], machine)

        # if there is not such node
        if current_state is None:
            # goes to fail state
            current_state = machine[current_state_copy]['fail_link']

            # as long as we can't find next state with text[i] label and current_state is not 0
            while find_next_state(current_state, text[i], machine) is None and current_state != 0:
                # set current state to fail state of current state
                current_state = machine[current_state]["fail_link"]

            # in this case we can be sure that thanks to while loop current_state in function is not None
            # but new current_state-> the result of find function can be none
            current_state = find_next_state(current_state, text[i], machine)

            # so before coping current_state we make sure that current_state in not none
            if current_state is not None:
                current_state_copy = current_state
        else:
            # current state is not none, so we can copy it
            current_state_copy = current_state

        if current_state is not None:
            # if there is any output in current node
            if machine[current_state]["out"]:
                for pattern in machine[current_state]["out"]:
                    # append pattern and starting index to the list
                    pattern_indexes.append([pattern, i + 1 - len(pattern)])

    return pattern_indexes


if __name__ == "__main__":
    patternList = ['abc', 'aab', 'cba', 'aa']
    automate = build(patternList)
    print(search(automate, "kaaabcbaab"))


