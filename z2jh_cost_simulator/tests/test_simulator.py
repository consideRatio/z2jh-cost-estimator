import pytest

from ..simulator import Simulation, NodeState

# Configurations
"""
The maximum number of Nodes is 2 each with a capacity of 3.
The amount of time a user is allowed to be inactive before the user's pod is culled is 3(pod_culling_max_inactivity_time)
The amount of time a pod is allowed to live before it is culled is 7 (pod_culling_max_lifetime).
The minimum number of nodes that should be 'Running' at all times is 1.
If a node is not used for 5 minutes then it should be 'Stopped'.
"""


def test_pytest_setup():
    """Dummy test to verify we can run tests at all."""
    assert True


def test_create_pod():
    # To check that a pod is created when the user activity becomes 1.

    user_activity = [[0, 1, 1]]
    sim = Simulation(simulation_time=30, user_activity=user_activity)
    sim.generate_user_activity()
    sim.run_simulation(stop=3)

    assert sim.user_pool[0].activity[1] == 1
    assert sim.user_pool[0].has_pod == True


def test_create_multiple_pods():
    user_activity = [[0, 1, 1], [0, 0, 1]]
    sim = Simulation(simulation_time=30, user_activity=user_activity)
    sim.generate_user_activity()
    sim.run_simulation(stop=3)
    assert sim.user_pool[1].activity[2] == 1
    assert sim.user_pool[1].has_pod == True
    assert len(sim.node_pool[0].list_pods) == 2


def test_check_node_state():

    # If there are pods assigned to Nodes which are 'Stopped', then the state of these nodes
    # transitions from 'Stopped' to 'Running'
    user_activity = [[0, 1, 1, 1, 1, 1, 0]]
    sim = Simulation(simulation_time=30, user_activity=user_activity)
    sim.generate_user_activity()
    sim.run_simulation(stop=7)
    assert sim.node_pool[0].started_state[0] == NodeState.Stopped
    assert sim.node_pool[0].started_state[1] == NodeState.Starting
    assert sim.node_pool[0].started_state[6] == NodeState.Running


def test_max_pods_on_node():
    # The maximum number of user pods that can be assigned to a node is 3.
    user_activity = [
        [0, 1, 1, 1, 1, 1, 1],
        [0, 0, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 1, 1],
    ]
    sim = Simulation(simulation_time=30, user_activity=user_activity)
    sim.generate_user_activity()
    sim.run_simulation(stop=6)
    assert sim.node_pool[0].utilized_capacity[4] == 3
    assert sim.node_pool[0].utilized_capacity[5] == 3
    # so, once the node 1 reaches the max capacity, the next user pod is scheduled on Node 2.
    assert sim.node_pool[1].utilized_capacity[5] == 1


def test_culling_pod_max_life_time():
    # The first user pod has been living for 7 minutes(pod_culling_max_lifetime), so it should be culled at 8th min.
    user_activity = [[0, 1, 1, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1, 0, 0]]
    sim = Simulation(simulation_time=30, user_activity=user_activity)
    sim.generate_user_activity()
    sim.run_simulation(stop=4)
    assert len(sim.node_pool[0].list_pods) == 2
    assert sim.start_time == 4
    sim.run_simulation(stop=9)
    # The pod has been removed from the node list.
    assert len(sim.node_pool[0].list_pods) == 1


def test_pod_culling_for_inactivity():
    # The user pod for the first user is culled at 8th minute as it has been inactive for 3 minutes(pod_culling_max_inactive_time).
    user_activity = [[0, 0, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 1, 1, 0, 0]]
    sim = Simulation(simulation_time=30, user_activity=user_activity)
    sim.generate_user_activity()
    sim.run_simulation(stop=4)
    assert len(sim.node_pool[0].list_pods) == 2

    sim.run_simulation(stop=8)
    assert sim.node_pool[0].utilized_capacity[6] == 2
    assert sim.node_pool[0].utilized_capacity[7] == 1
    assert len(sim.node_pool[0].list_pods) == 1


def test_schedule_on_most_utilized_node():

    user_activity = [
        [0, 1, 1, 0, 0, 0, 0, 1, 1],
        [0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 1, 1, 1, 1, 1],
    ]
    sim = Simulation(simulation_time=30, user_activity=user_activity)
    sim.generate_user_activity()
    sim.run_simulation(stop=4)
    assert len(sim.node_pool[0].list_pods) == 3
    assert len(sim.node_pool[1].list_pods) == 0
    sim.run_simulation(stop=7)
    assert len(sim.node_pool[0].list_pods) == 2
    assert len(sim.node_pool[1].list_pods) == 1
    sim.run_simulation(stop=8)
    assert len(sim.node_pool[0].list_pods) == 3

def test_two_pods_culling():
    user_activity = [[0, 0, 1, 1, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1]]
    sim = Simulation(simulation_time=30, user_activity=user_activity)
    sim.generate_user_activity()
    sim.run_simulation(stop=3)
    assert sim.node_pool[0].utilized_capacity[2] == 2
    sim.run_simulation(8)
    assert (
        sim.node_pool[0].utilized_capacity[7] == 1
    )  # the first user pod was culled due to inactivity for 3 minutes
    sim.run_simulation(9)
    assert (
        sim.node_pool[0].utilized_capacity[8] == 0
    )  # the second user pod is culled as it has been active for 7 minutes

    
def test_two_pods_created_simultaneously():
    user_activity = [[0,1,0], [0,1,0]]
    sim = Simulation(simulation_time=3, user_activity=user_activity)
    sim.generate_user_activity()
    sim.run_simulation(stop=2)
    assert sim.node_pool[0].utilized_capacity[1] == 2
    assert len(sim.node_pool[0].list_pods) == 2

def test_simultaneous_pod_creation_1(): 
    user_activity = [[1,0,0], [1,0,0]]
    sim = Simulation(simulation_time=30, user_activity=user_activity)
    sim.generate_user_activity()
    sim.run_simulation(stop=1)
    assert sim.node_pool[0].utilized_capacity[0] == 2
    assert len(sim.node_pool[0].list_pods) == 2

def test_simultaneous_pod_creation_2():
    user_activity = [[1,1,1], [1,1,1]]
    sim = Simulation(simulation_time=30, user_activity=user_activity)
    sim.generate_user_activity()
    sim.run_simulation(stop=1)
    assert sim.node_pool[0].utilized_capacity[0] == 2
    assert len(sim.node_pool[0].list_pods) == 2

def test_simultaneous_pod_creation_3():
    user_activity = [[0,1,1], [0,1,1]]
    sim = Simulation(simulation_time=30, user_activity=user_activity)
    sim.generate_user_activity()
    sim.run_simulation(stop=2)
    assert sim.node_pool[0].utilized_capacity[1] == 2
    assert len(sim.node_pool[0].list_pods) == 2
    

def test_two_pods_culling_at_same_time():
    user_activity = [[0, 0, 1, 1, 1, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1]]
    sim = Simulation(simulation_time=30, user_activity=user_activity)
    sim.generate_user_activity()
    sim.run_simulation(stop=3)
    assert sim.node_pool[0].utilized_capacity[2] == 2
    sim.run_simulation(9)  # two pods being culled at the same time. 
    assert (
        sim.node_pool[0].utilized_capacity[8] == 0
    ) 
    
    

def test_min_number_of_running_nodes():
    # If a node is not used for 5 minutes then it should be 'Stopped'.
    # But at any time,(minimum number of nodes) should always be 'Running'
    user_activity = [[0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0]]

    sim = Simulation(simulation_time=25, user_activity=user_activity)
    sim.generate_user_activity()
    
    
    