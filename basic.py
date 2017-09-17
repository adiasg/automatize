import paho.mqtt.client as mqtt

class State:
    def __init__(self):
        self.next_state_dict = {}
    def next_state(self, input_state_pair):
        # Define transition from this state using this_state.next_state( (symbol,next_state) )
        '''
        TODO -  Take variable number of multiple input_state_pairs as input
                Expected usage is this_state.next_state( input_state_pair1, input_state_pair2, ... )
        '''
        self.next_state_dict[input_state_pair[0]] = input_state_pair[1]
    def on_symbol(self, symbol):
        # Return next_state for transition from this_state on symbol
        return self.next_state_dict[symbol]
    def set_action(self, action_callback):
        # Set callback in self.action for self.run()
        self.action = action_callback
    def run(self):
        # Callback the callback funciton to execute this state's action
        self.action()

# Callback for state a
def runA():
    print("In state A")

# Callback for state b
def runB():
    print("In state B")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("automatize")

def on_message(client, userdata, msg):
    if(msg.payload=="exit"):
      print("Exiting.")
      client.disconnect()
    else:
      print(msg.topic+" : "+msg.payload.decode("utf-8"))
      userdata[0] = userdata[0].on_symbol(msg.payload.decode("utf-8"))
      userdata[0].run()

if __name__ == '__main__':
    # Automaton definition
    # Expected from programmer
    a = State()
    b = State()
    a.set_action(runA)
    b.set_action(runB)
    a.next_state(('x',b))
    b.next_state(('x',a))
    initial_state = a

    # MQTT client initialization
    # Will be part of the library
    client = mqtt.Client(userdata=[initial_state])
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)

    # MQTT client event loop
    client.loop_forever()
