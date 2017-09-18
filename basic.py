import paho.mqtt.client as mqtt


class State:
    def __init__(self):
        self.next_state_dict = {}
        self.action = None

    def next_states(self, *args):
        """
        Defines the next states for the current state based on variable symbol list
        :param args: ( symbol , next_state upon accepting symbol )
        """
        for input_state_pair in args:
            self.next_state_dict[input_state_pair[0]] = input_state_pair[1]

    def on_symbol(self, symbol):
        """
        Returns next_state if current_state accepts the passed symbol
        :param symbol: A single character
        :return: next_state
        """
        try:
            return self.next_state_dict[symbol]
        except KeyError:
            print("------------------------------")
            print("Error : Unsupported transition")
            print("State was not changed!")
            print("Valid transitions are: " + ",".join(self.next_state_dict.keys()))
            print("------------------------------")
            return self

    def set_action(self, action_callback):
        """
        Set callback in self.action
        :param action_callback: Callback function for the state being defined
        """
        self.action = action_callback

    def run(self):
        """Trigger the callback when run is called"""
        self.action()


# Callback for state a
def runA():
    print("In state A")


# Callback for state b
def runB():
    print("In state B")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("automatize")


def on_message(client, userdata, msg):
    if msg.payload.decode("utf-8") == "exit":
        print("Exiting.")
        client.disconnect()
    else:
        print(msg.topic + " : " + msg.payload.decode("utf-8"))
        userdata[0] = userdata[0].on_symbol(msg.payload.decode("utf-8"))
        userdata[0].run()


if __name__ == '__main__':
    # Automaton definition
    # Expected from programmer
    a = State()
    b = State()
    a.set_action(runA)
    b.set_action(runB)
    a.next_states(('x', a), ('y', b))
    b.next_states(('x', b), ('y', a))
    initial_state = a

    # MQTT client initialization
    # Will be part of the library
    client = mqtt.Client(userdata=[initial_state])
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)

    # MQTT client event loop
    client.loop_forever()
