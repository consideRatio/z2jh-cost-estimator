# Z2JH Cost Estimator
This project helps you estimate the costs for a cloud based JupyterHub deployment given information about the estimated usage.

## Running this cost-estimator from mybinder.org

Follow the link given below to launch **cost-estimator**.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Sunita76/z2jh-cost-estimator/master?urlpath=%2Flab%2Ftree%2Ftest_simulator_package.ipynb)

Binder is ideally suited for relatively short sessions. Binder will automatically shut down user sessions that have more than 10 minutes of inactivity.

## Using the cost-estimator on the local machine

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
The working of the cost-estimator can be divided into the following steps:
   
 - **Input Form** : The input form allows the user of the simulator to draw a line containing the information about the maximum number of users that are using jupyter hub at a particular hour for one whole day.

    ![input-form](https://user-images.githubusercontent.com/47885949/60509794-1d488a00-9cce-11e9-9ade-f0a9ea53c3ac.png)
    
 - **Transformation** : The data of the input-form is used to generate an estimated list of users with their usage. This user activity is then used as an input to the simulator.
 
 - **Simulation** : The simulator runs the simulation for the given user activity and stores the information about:  
   How the users are scheduled on the nodes in the cluster 
   When are the nodes scaled up/down in the cluster

 - **Presentation** : The total cost for deploying jupyterhub using Kubernetes is calculated based on the simulation configurations and the utilization of the cluster.
   The line chart shows how the nodes are scaled up/down depending on the users and their activity at that hour.
  
Pull requests are welcome for the given list of issues.   
  - It would be nice to have an input form which can allow dynamic changes to the upper limit of the maximum number of users instead of configuring the value of the maximum number of users.  
  - In the simulator, the number of nodes is restricted to a specific range, and when we have potentially unlimited users, they may end up as **pending** without us knowing. It would be good to store the information about the pending users for every hour, and present a line chart displaying the pending users for every hour.  
  - When you run the cost-estimator, the initial input-form is displayed, assuming that the number of users increase steadily with each hour. It would be nice to draw an initial input-form based on some parameters like the time of the day, the day of the week etc and show a graph which is close to the actual usage pattern.
  
For major changes, please open an issue first to discuss what you would like to change.
    
    
### Running tests

- Run tests

  The test modules are present in the Z2jh-cost-estimator/z2jh_cost-simulator/tests

    ```sh
    pytest
    ```

## Authors
  Sunita Anand  
  Erik Sundell

   


