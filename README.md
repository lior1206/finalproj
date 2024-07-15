
# Flask Expense Tracker Application
# Overview
This Flask application provides functionalities for user authentication (login and registration) and expense tracking. Users can register, log in, and track their average daily expenses. The app uses MongoDB for data storage and is deployed on a Kubernetes cluster.

# Features
- User Registration
- User Login
- Expense Tracking
- Average Daily Expense Calculation
- Requirements
- The application requires the following Python packages:


**requirements.txt**
~~~sh 
Flask==2.0.1
pymongo==3.11.4
bcrypt==3.2.0
pytest==6.2.4
~~~
- Setup and Installation
- Local Setup


**Clone the repository:**
~~~sh
git clone <https://github.com/lior1206/finalproj >
~~~
0
**Install the required packages:**
~~~sh
pip install -r requirements.txt
~~~

# Set up MongoDB:
Ensure you have a MongoDB instance running. Update the MongoDB connection string in your Flask app as needed.


# Kubernetes Deployment
- Ensure your Kubernetes cluster is running and accessible.

- Deploy MongoDB and your Flask application using Helm charts.


Monitor the application using Prometheus and Grafana.

## Continuous Integration and Deployment
# **Jenkins**
# The application uses Jenkins for continuous integration 
**The Jenkins pipeline includes the following stages**

- Checkout: Fetch the latest code from the Git repository.
- Prepare: Set up the environment and dependencies.
- Build Docker Image: Build a Docker image for the Flask application.
- Test: Run tests using pytest.
- Push Docker Image: Push the Docker image to a Docker registry.
- Update Helm Chart: Update the Helm chart with the new image version.
- Trigger ArgoCD Sync: Trigger ArgoCD to sync the new deployment.
- Create Merge Request: Create a merge request for the changes.
- Commit Changes to GitHub: Commit the changes to the GitHub repository.

## Monitoring

**The application is monitored using Prometheus and Grafana. Ensure that both are deployed and configured to monitor your application and MongoDB instances.**


## Contact
For more information, please contact lior gerbi at liogrb7@gmail.com.