import enum
from enum import Enum
import numpy as np
import pandas as pd


class User:
    """
    The user object should be initialized with the activity to simulate during a full week.
    """

    def __init__(self, simulation_time):
        """
        simulation_time - the duration of the simulation(in minutes) . 
        """
        self.activity = np.array(simulation_time)
        self.has_pod = False
        self.node_assigned_to_pod = None
        self.pod_start_time = 0

    @property
    def pod_is_pending(self):
        return self.node_assigned_to_pod == None

    @property
    def pod_is_assigned(self):
        return self.node_assigned_to_pod != None


class NodeState(enum.Enum):
    """
    This class maintains the state of the Node.
    """

    Stopped = 0
    Starting = 1
    Running = 2
    Stopping = 3


class Node:
    """
    Node class will be initialized with the capacity of user pods that can be scheduled on the node.
    """

    def __init__(self, simulation_time, capacity=20):
        """
        simulation_time - the duration of simulation(in minutes)
        The utilization of the node for every minute of the simulation time is also stored.
        """
        self.capacity = capacity
        self.started_state = np.array(
            [NodeState.Stopped for i in range(simulation_time)]
        )
        self.utilized_capacity = np.zeros(simulation_time)
        self.list_pods = []

    def remove_pod_ref(self, user_pod, time):
        """
        This method is invoked when a user pod is culled.
        The user reference to the pod is removed.
        The user pod is removed from it's assigned node list.
        """
        user_pod.has_pod = False
        user_pod.node_assigned_to_pod = None
        user_pod.start_time = 0
        if self.utilized_capacity[time] > 0:
            self.utilized_capacity[time:] = self.utilized_capacity[time] - 1
        self.list_pods.remove(user_pod)

        # else:
        # raise "this should never happen"


# The main class for running the simulation
class Simulation:
    """

    """

    def __init__(self, configurations, user_activity):
        """
        configurations - Settings for Node memory/CPU usage, user pod memory/CPU usage and the configurations for pod culling.
        
        user_activity  - The list of the activity of different users. 
                         Each user's activity is an array of 10080 minutes of 0's and 1's(0 for inactivity and 1 for active) 
        """

        self.configurations = configurations
        self.node_pool = []
        self.user_pool = []
        self.user_activity = user_activity
        self.simulation_time = len(user_activity[0])
        self.start_time = 0
        self.utilization_data = pd.DataFrame()

    # TODO: make this have only one underscore, along with _add_users
    def __add_nodes(self):

        # Calculate the capacity of the node, given the node resource(memory) and
        # user resource(memory).
        # Initialize the node pool with nodes for the selected min and max number of nodes.
        node_capacity = 0
        node_available_memory = self.configurations["node_memory"] * 1024 - 216
        # 216 MB is the approx. node memory used by system pods.
        node_capacity = node_available_memory / self.configurations["user_pod_memory"]
        for node_count in range(
            self.configurations["min_nodes"], self.configurations["max_nodes"]
        ):
            # rounding off the value to get the capacity.
            self.node_pool.append(
                Node(self.simulation_time, capacity=round(node_capacity))
            )

    def __add_users(self):
        """Initialize the user list with the user activity
        """
        for activity in self.user_activity:
            user = User(self.simulation_time)
            user.activity = activity
            self.user_pool.append(user)

    def run(self, stop=0):
        """
        The method will be looped till the 'stop' time.
        for each minute, the run method will:
        1. Create user pods for active users
        2. Try scheduling the user pods.
        3. Auto scale the nodes.
        4. Cull the pods according to the pod culling configuration.
        """
        if len(self.user_pool) == 0:
            self.__add_users()
        if len(self.node_pool) == 0:
            self.__add_nodes()

        ## The amount of time a user is allowed to be inactive before the user's pod is culled
        pod_culling_max_inactivity_time = self.configurations["pod_inactivity_time"]

        ## The amount of time a pod is allowed to live before it is culled
        pod_culling_max_lifetime = self.configurations["pod_max_lifetime"]

        for t in range(self.start_time, stop):
            # Create user pods for active users without a pod
            for user in self.user_pool:
                if user.activity[t] == 1 and user.has_pod == False:
                    user.has_pod = True

            """
            Scheduler is responsible of placement of pending pods
            on the most resource utilized node that still has room.
            """
            ## Identify pods to schedule
            pending_pods = [
                user_pod
                for user_pod in self.user_pool
                if user_pod.has_pod == True and user_pod.pod_is_pending
            ]
            count = 0
            for user_pod in pending_pods:
                ## Find a node to schedule the pod on
                sorted_node_pool = sorted(
                    self.node_pool,
                    key=lambda node: node.utilized_capacity[t],
                    reverse=True,
                )
                for node in sorted_node_pool:

                    if node.utilized_capacity[t] < node.capacity:
                        user_pod.node_assigned_to_pod = node
                        user_pod.pod_start_time = t
                        node.list_pods.append(user_pod)
                        node.utilized_capacity[t:] = node.utilized_capacity[t] + 1
                        break

            """
            Cluster Autoscaler (CA): start nodes
            The CA looks for 'Stopped' nodes which have some pods assigned to them,
            and transitions the state of those nodes from 'Stopped' to 'Running'
            """
            nodes_to_start = [
                node
                for node in self.node_pool
                if node.started_state[t] == NodeState.Stopped
                and len(node.list_pods) > 0
            ]
            for node in nodes_to_start:
                assert len(node.list_pods) > 0
                node.started_state[t : t + 5] = NodeState.Starting
                node.started_state[t + 5 :] = NodeState.Running

            """
            Cluster Autoscaler (CA): stop nodes
            If a node doesn't have any pods scheduled to it for a certain interval of time(node_stop_time), the CA makes the node 'Stopped'.
            
            """
            node_stop_time = self.configurations["node_stop_time"]
            if t >= node_stop_time:
                started_nodes = [
                    node
                    for node in self.node_pool
                    if node.started_state[t] == NodeState.Running
                ]
                no_of_started_nodes = len(started_nodes)  # count of started nodes
                for node in started_nodes:
                    if no_of_started_nodes > self.configurations["min_nodes"]:
                        if (
                            np.sum(node.utilized_capacity[t - node_stop_time : t + 1])
                            == 0
                        ):
                            node.started_state[t] = NodeState.Stopping
                            node.started_state[t + 1 :] = NodeState.Stopped
                            no_of_started_nodes -= 1
                    else:
                        break

            # Pod Culler
            for node in self.node_pool:
                pods_assigned_to_node = [user_pod for user_pod in node.list_pods]
                for user_pod in pods_assigned_to_node:

                    """
                    Pod Culler: cull for inactivity

                    The Pod Culler deletes the user pods of users who have been inactive 
                    for a too long interval of time (pod_culling_max_inactivity_time)
                    """

                    if pod_culling_max_inactivity_time > 0:
                        if (
                            t >= pod_culling_max_inactivity_time
                            and np.sum(
                                user_pod.activity[
                                    t - pod_culling_max_inactivity_time : t + 1
                                ]
                            )
                            == 0
                        ):
                            node.remove_pod_ref(user_pod, t)
                            continue

                    """
                    Pod Culler: cull for max lifetime

                    The Pod Culler deletes the user pods that has been running for too long (pod_culling_max_lifetime)
                    If pod_culling_max_lifetime is 0 then the user pod has infinite lifetime.
                    """

                    if pod_culling_max_lifetime > 0:
                        if t - user_pod.pod_start_time >= pod_culling_max_lifetime:
                            node.remove_pod_ref(user_pod, t)
        self.start_time = stop

    def create_utilization_data(self):
        # Storing the node wise per minute utilization data.
        time_data = list(range(self.simulation_time))

        node_data = {"time": time_data}

        for index, node in enumerate(self.node_pool):
            node_data_utilized_capacity = []
            node_data_utilized_percent = []

            for i in range(self.simulation_time):
                node_data_utilized_capacity.append(node.utilized_capacity[i])
                node_data_utilized_percent.append(
                    (node.utilized_capacity[i] / node.capacity)
                )

            node_data[
                "node" + str(index) + "_utilized_capacity"
            ] = node_data_utilized_capacity
            node_data[
                "node" + str(index) + "_utilized_percent"
            ] = node_data_utilized_percent

            self.utilization_data = pd.DataFrame(data=node_data)
        return self.utilization_data
