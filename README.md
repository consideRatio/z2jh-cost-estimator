# Z2JH Cost Estimator
This project helps you estimate the cloud costs for a cloud based JupyterHub deployment given information about the estimated usage.

## Running this cost-estimator from mybinder.org

Follow the link given below to launch **test-simulator-package.ipynb** for cost-estimator.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Sunita76/z2jh-cost-estimator/master?urlpath=%2Flab%2Ftree%2Ftest_simulator_package.ipynb)

Binder is ideally suited for relatively short sessions. Binder will automatically shut down user sessions that have more than 10 minutes of inactivity.

## Using the cost-estimator on the local machine
 
- Clone the repo and make a change

    ```sh
    git clone https://github.com/Sunita76/z2jh-cost-estimator.git
    cd z2jh-cost-estimator
    ```

- Clone the repo and make a change

    ```sh
    git clone https://github.com/Sunita76/z2jh-cost-estimator.git
    cd z2jh-cost-estimator
    ```

- Install `pipenv` using `pip`.

    ```sh
    pip install pipenv
    ```

- Setup a virtual development environment

    ```sh
    pipenv install --dev
    ```

- Run tests

  The test modules are present in the Z2jh-cost-estimator/z2jh_cost-simulator/tests

    ```sh
    pipenv run pytest
    ```
- Open **test-simulator-package.ipynb** notebook in the jupyter lab.
  Select Run -> Run all to run the simulator.
 

    

## Understanding this cost-estimator

- Input Form :
  The input form allows the user of the simulator to draw a line containing the information about the maximum number of users that are using jupyter hub at a particular hour for one whole day.

![input-form](https://user-images.githubusercontent.com/47885949/60509794-1d488a00-9cce-11e9-9ade-f0a9ea53c3ac.png)

- Presentation :
  The total cost for deploying jupyterhub using Kubernetes is calculated based on the simulation configurations and the utilization of the cluster.
  The line chart shows how the nodes are scaled up/down depending on the users and their activity at that hour.
 

## Contributing
    Pull requests are welcome for the given list of issues. 

  - It would be nice to have an input form which can allow dynamic changes to the upper limit of the maximum number of users instead of configuring the value of the maximum number of users.
    
  - In the simulator, the number of nodes is restricted to a specific range, and when we have potentially unlimited users, they may end up as **pending** without us knowing. It would be good to store the information about the pending users for every hour, and present a line chart displaying the pending users for every hour.
   
  - When you run the cost-estimator, the initial input-form which is displayed, assumes that the number of users increase steadily with each hour. It would be nice to design the input-form by taking into account the time of the day, the day of the week etc and show a graph which is close to the actual usage pattern.
  
    For major changes, please open an issue first to discuss what you would like to change. 

## Authors
    Sunita Anand
    
    Erik Sundell

   


