import pytest

#to figure out how to do......

from ..simulator import Simulation
from ..simulator import NodeState

def test_pytest_setup():
    """Dummy test to verify we can run tests at all."""
    assert True
    
def test_create_pod():
    #To check that a pod is created when the user activity becomes 1.
    
    #user_activity = [[0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     #            [0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     #            [0,0,0,1,1,1,1,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
      #           [0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],
      #           [0,0,0,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0]]
    
    user_activity = [[0,1,1]]
    sim = Simulation(simulation_time=30, user_activity=user_activity)
    sim.run_simulation(stop=3)
    assert sim.user_pool[0].activity[1] == 1
    assert sim.user_pool[0].pod != None
    

def test_create_multiple_pods():
    user_activity = [[0,1,1],[0,0,1]]
    sim = Simulation(simulation_time=30, user_activity=user_activity)
    sim.run_simulation(stop=3)
    assert sim.user_pool[1].activity[2] == 1
    assert sim.user_pool[1].pod != None
    assert len(sim.node_pool[0].list_pods) == 2
    

def test_check_node_state():
    # A 'Stopped' node should start 'Running' when there are pods assigned to the node.
    user_activity = [[0,1,1,1,1,1,0]]
    sim = Simulation(simulation_time=30, user_activity=user_activity)
    sim.run_simulation(stop=7)
    assert sim.node_pool[0].started_state[0] == NodeState.Stopped
    assert sim.node_pool[0].started_state[1] == NodeState.Starting
    assert sim.node_pool[0].started_state[6] == NodeState.Running
    

def test_culling_pod_max_life_time():
    #The first user pod has been living for 7 minutes(pod_max_lifetime), so it should be culled at 8th min.
    user_activity = [[0,1,1,1,1,1,0,0,0,0],[0,0,1,1,1,1,1,1,1,0]]
    sim = Simulation(simulation_time=30, user_activity=user_activity)
    sim.run_simulation(stop=4)
    assert len(sim.node_pool[0].list_pods) == 2
    sim = Simulation(simulation_time=30, user_activity=user_activity)
    sim.run_simulation(stop=9)
    assert len(sim.node_pool[0].list_pods) == 1

#def test_pod_culling_for_inactivity():
 #   user_activity = [[0,1,1,1,1,0,0,0,0,0]]
  #  sim = Simulation(simulation_time=30, user_activity=user_activity)
    
    
    
    

    