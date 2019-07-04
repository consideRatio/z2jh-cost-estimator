# Z2JH Cost Estimator
This project helps you estimate the costs for an autoscaling [cloud based JupyterHub deployment](https://z2jh.jupyter.org/en/latest/) given information about the estimated usage.

## Running this cost-estimator from mybinder.org

Click on the **launch** link below to open a notebook where you can run the simulator for calculating the cloud costs for your JupyterHub deployment.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Sunita76/z2jh-cost-estimator/master?urlpath=/lab/tree/notebooks/test_simulator_package.ipynb)

Binder is ideally suited for relatively short sessions. Binder will automatically shut down user sessions that have more than 10 minutes of inactivity.

## Running the cost-estimator on your local machine

- Clone the repo and make a change

    ```sh
    git clone https://github.com/Sunita76/z2jh-cost-estimator.git
    cd z2jh-cost-estimator
    ```

- Install `pipenv` using `pip`.

    ```sh
    pip install pipenv
    ```

- Setup and enter a virtual development environment

    ```sh
    pipenv install --dev
    pipenv shell
    ```
    
- Start JupyterLab

    ```sh
    jupyter lab
    ```
    
- Open **test_simulator_package.ipynb** notebook in jupyter lab.
  Select Run -> Run all to run the simulator.
  

## Contributing

To help you contribute, it could be useful to understand how the code is currently structured. There are four key sections.
   
- **Input**: The input form allows the user of the simulator to draw a line containing the information about the maximum number of users that are using jupyter hub at a particular hour for one whole day.

    ![input-form](https://user-images.githubusercontent.com/47885949/60585313-bc818600-9d8f-11e9-9ba5-2aa14e72f6cb.png)
    
- **Transformation**: The data from the input-form is used to generate an estimated list of users with their usage. This user activity is then used as an input to the simulator.
 
- **Simulation**: The simulator runs the simulation for the given user activity and stores the information about:  
    How the users are scheduled on the nodes in the cluster   
    When are the nodes scaled up/down in the cluster

- **Presentation**: The total cost for deploying jupyterhub using Kubernetes is calculated based on the simulation configurations and the utilization of the cluster.
    The line chart shows how the nodes are scaled up/down depending on the users and their activity at that hour.
  
Pull requests are welcome for the given list of issues.

- It would be nice to have an input form which can allow dynamic changes to the upper limit of the maximum number of users instead of configuring the value of the maximum number of users.  
- In the simulator, the number of nodes is restricted to a specific range, and when we have potentially unlimited users, they may end up as **pending** without us knowing. It would be good to store the information about the pending users for every hour, and present a line chart displaying the pending users for every hour.  

  
For major changes, please open an issue first to discuss what you would like to change.
    
    
### Running tests

There are tests defined in [z2jh_cost_simulator/tests](z2jh_cost_simulator/tests). To run them:

```sh
pytest
```

## Background

This project was founded by Sunita Anand ([@Sunita76](https://github.com/Sunita76)). It started as part of a summer intership at Sandvik's Center of Digital Excellence (CODE) with Erik Sundell ([@consideRatio](https://github.com/consideRatio)) as a guide.
