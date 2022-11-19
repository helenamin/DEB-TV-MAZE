<a id="top"></a>
<h1 align="left"> TV MAZE TV SHOWS 📺</h1>
<h6 align="left"> Currated TV Show datasets from <a href="https://www.tvmaze.com/">TV Maze</a></h6>

<hr style="background:#ADD8E6;">

<!-- Project Background -->

<h2 id="background">Project Background</h2>
<p align="center">
 <img src="https://media.istockphoto.com/photos/man-watching-tv-lying-on-sofa-legs-on-table-picture-id1331523088?b=1&k=20&m=1331523088&s=170667a&w=0&h=YnmsLqGLdmntesnGiIzBrbhXDxNbHiOzrbudKivWet4=" alt="Watch TV" width="60%" height="60%">
</p>

<p align="justify"> 
  TV show data extracted from <a href="https://www.tvmaze.com/">TV Maze API</a> for Data Analyst to identify and visualize trends in TV history 
  and for ML use-case to potentially create shows with AI or suggest shows based on genres and ratings. Once data is visualised, it can then be
  used by TV show producers to produce better content and potential actors to star in shows that will be popular. Network channels data can help to determine what shows to air 
  and what time would be a success when aired.
</p>
</br>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><b>Table of Contents</b></summary>
  <ol>
    <li><a href="#background"> Project Background</a></li>
    <li><a href="#Installations">Installation & Setup</a></li>
    <li><a href="#folder-structure">Folder Structure</a></li>
    <li><a href="#theprocess">How it's done</a></li>
      <ul>
        <li><a href="#sad">Solution Architecture Diagram</a></li>
        <li><a href="#data-int">Data Integration</a></li>
        <li><a href="#data-trans">Data Transformation</a></li>
        <li><a href="#data-ochestration">Data Ochestration</a></li>
      </ul>
    </li>
    <li><a href="#discussion">Discussion, Lesson Learnt and Future Improvement</a></li>
    <li><a href="#contributors">Contributors & Contributions</a></li>
  </ol>
</details>

<hr style="background:#ADD8E6;">
<!-- WHAT WE USE -->
<h2 id="Installations">Installation & Setup</h2>

This project is built with Python version 3.9.

The following packages and tools are used in this project:

- Jupyter Notebook
- Airbyte
- Snowflake
- Dbt
- Airflow
- Jinja
- Docker
- AWS Services (S3, ECR, EC2)
- Diagrams

<u>To run the pipeline locally:</u>
Conda Activate "your venv"

pip install -r requirement.txt

#### Deploy airbyte locally

1. Clone the airbyte repo locally from `https://github.com/airbytehq/airbyte.git` 

    ```
    git clone https://github.com/airbytehq/airbyte.git
    ```
2. Make sure you have Docker Desktop running first
3. Run the docker compose file 

    ```
    cd airbyte 
    docker-compose up
    ```

4. Copy /source-tvmaze into airbyte/airbyte-integrations/connector

5. Run docker-compose up again to update the airbyte connector

6. Setup custom TVMaze connector as Airbyte Source

7. Login into Snowflake and setup Snowflake user roles with the SQL files within the data-integration\snowflake

8. Setup Snowflake as Destination and create new connection between Source and Destination in Airbyte 

9. Install dbt-core and its snowflake specific packages `pip install dbt-snowflake`

10. Under dbt project folder run `dbt init`. That will create the same folder as the data-transformation/dbt

11. Models can be copied over from the tvmaze folder under data-transformation/dbt and run `dbt build`

#### Building a Docker Image and push to ECR

1. Build the Docker Image 
`docker build -t tvmaze-dbt:dev -f docker/Dockerfile`

2. Tag the Docker Image for AWS 
`tvmaze-dbt:dev *aws_account_id*.dkr.ecr.*aws_region*.amazonaws.com/tvmaze-dbt-ecr:dev`

3. Login to AWS with CLI 
`aws ecr get-login-password --region *aws_region* | docker login --username AWS --password-stdin *aws_account_id*.dkr.ecr.*aws_region*.amazonaws.com/tvmaze-dbt-ec`

4. Docker Push 
`docker push *aws_account_id*.dkr.ecr.*aws_region*.amazonaws.com/tvmaze-dbt-ecr:dev`


#### Exporting Airflow connections to JSON

1. Open up Terminal and input 
`docker exec -it *replace this with the connection id* /bin/.sh`

2. Identify where the "dags" folder in airflow with `ls` and change directory into the folder with `cd dags`

3. Input `airflow connections export conn.json` and verify that the connections are successfully exported to "conn.json"

4. To import the "conn.json" file for airflow, use 
`airflow connection import conn.json`



<hr style="background:#ADD8E6;">

<!-- FOLDER STRUCTURE -->
<h2 id="folder-structure">Folder Structure</h2>

    code
    .
    │
    ├── data-integration
    │   ├── airbyte
    │   ├── snowflake
    ├── data-ochestration
    │   └── airflow
    │        └── dags
    ├── data-transformation
    │   └── dbt
    │       ├── docker
    │       ├── logs
    │       └── tvmaze
    ├── screenshots
    ├── solution_diagram.py
    └── README.md

<hr style="background:#ADD8E6;">
<!-- THE WHOLE PROCESS OF THE PROJECT -->
Screenshots for AWS ECR image and AWS setup

<h2 id="theprocess">How it's Done</h2>
<p> 
We start off by setting up Airbyte and Snowflake. As we chose the TVMAZE API which does not have a connector in Airbyte, we had to create a custom connector.
The custom connector is built with incremental refresh on the backend and the front end interface specified on spec.yaml. We have also described the schema in tv_maze.json.
This is done through sampling the json response to get the response structure and datatypes, however for datatypes we went with STRINGS ALL THE WAY!. We then build the Docker image and upload to AWS ECR and run the instance with EC2.
In Snowflake, we create the Database - TVSHOW to host all the data we will be ingesting. We've also created roles for DBT and Airbyte.
Once the access is sorted, we created a connector between the Custom TVMaze API as the Source and Snowflake as the Destination. 
The source data is then ingested into Snowflake's S3 storage where we transform the data with models via DBT. These are all ochestrated with Airflow with Notification sent through to our project Slack channel.

<hr style="background:#ADD8E6;">

<h3 id="sad">Solution Architecture Diagram</h3>
<figure>
<img src="https://github.com/LuckyLukeAtGitHub/deb-project2-group2/blob/main/screenshots/tvshow_sa_diagram.png" alt="Solution Architecture Diagram" width="100%"> 
<figcaption>Created using <a href= "https://diagrams.mingrammer.com/">Diagrams</a></figcaption>
</figure>
<hr style="background:#ADD8E6;">

<h3 id="vat">View all tables</h3>
<figure>
<img src="https://github.com/LuckyLukeAtGitHub/deb-project2-group2/blob/main/screenshots/sme_diagram.png" alt="SOURCE-MODEL-EXPOSE Diagram" width="100%"> 
<figcaption>Created using <a href= "https://app.diagrams.net/">DrawIO</a></figcaption>
</figure>
</p>

<figure> 
<img src="https://github.com/LuckyLukeAtGitHub/deb-project2-group2/blob/main/screenshots/sourcetoexpose.png" alt="SME detail Diagram" width="100%"> 
<figcaption>Created using <a href= "https://app.diagrams.net/">DrawIO</a></figcaption>
</figure>
</p>

<hr style="background:#ADD8E6;">

<h2 id="data-int">Data Integration</h2>
<p align="justify"> 
For the data integration, Airbyte was chosen as the tool for performing extract and load, with Snowflake as our datawarehouse. The custom airbyte connector is a source connector used to get tv episode schedule data from the <a href= "https://api.tvmaze.com/schedule">tvmaze.com API</a>. The tvmaze connector was developed for incremental extracts. Testing has been done whereby the connector was added as a source in the Airbyte UI and used in a connection successfully extracting from the tvmaze API and loading the raw data to a Snowflake destination.
<br>
The next step was to create the datawarehouse in Snowflake and apply all corresponding user permissions to Airbyte and dbt. The full SQL query can be viewed <a href="https://github.com/LuckyLukeAtGitHub/deb-project2-group2/blob/main/data-integration/snowflake/user_role_grants.sql">here </a>
<figure> 
<img src="https://github.com/LuckyLukeAtGitHub/deb-project2-group2/blob/main/screenshots/snowflake_permisisons.PNG" alt="Snowflake Permissions" width="100%"> 
<figcaption>TVSHOW Snowflake Permissions</figcaption>
</figure>

Once that is setup, we test both the user permission with the logging into Snowflake and verify access.
Returning to Airbyte, we setup Snowflake as the destination with the Airbyte user credentials created earlier on Snowflake, then connect Source (Airbyte) and Destination (Snowflake). 

<figure> 
<img src="https://github.com/LuckyLukeAtGitHub/deb-project2-group2/blob/main/screenshots/airbyte_interface.png" alt="Airbyte Interface" width="100%"> 
<figcaption>Airbyte Successful Sync</figcaption>
</figure>

Upon successful Sync, response from API call are ingested into Snowflake's storage on the backend.

<figure> 
<img src="https://github.com/LuckyLukeAtGitHub/deb-project2-group2/blob/main/screenshots/snowflake_tvshows.PNG" alt="Snowflake TVSHOW" width="40%"> 
<figcaption>TVSHOW database structure</figcaption>
</figure>
</p>

<hr style="background:#ADD8E6;">


<h2 id="data-trans">Data Transformation</h2>

<p align="justify"> 
All transformations are done using dbt. We have created 3 staging tables and 5 serving tables. 
Models are written in SQL and can be found in the <a href="https://github.com/LuckyLukeAtGitHub/deb-project2-group2/blob/main/data-transformation/dbt/tvmaze/models">dbt\tvmaze\models</a> folder.
We've built the dbt docker image, upload onto ECR and run the instance with EC2. All credentials are hosted on S3 in an .env file.

<figure> 
<img src="https://github.com/LuckyLukeAtGitHub/deb-project2-group2/blob/main/screenshots/dbt_success.png" alt="Successful dbt run" width="100%"> 
<figcaption>Successful dbt run</figcaption>
</figure>

<b>We have used the following transformation techniques:</b>
<ul>
<li>Renaming - renaming certain column headers to avoid confusion</li>
<li>Data type casting - date string to date type, IDs into integers</li>
<li>Joins - Joins on multiple tables for the staging and serving tables</li>
<li>Aggregation function - avg() for ratings, rank() for ratings, count() number of shows</li>
<li>Data Cleaning - Nested replace() for Genres and Days </li>
<li>Filtering - where claused used to get show types with best rating.</li>
<li>Grouping - group by show_type, network_name </li>
<li>Sorting - Order By show runtime</li>
</ul>
</p>

<hr style="background:#ADD8E6;">

<h2 id="data-ochestration">Data Ochestration</h2>
<p align="justify"> 
Our ELTL process is ochestrated with a local version of Airflow. Our DAGS include a SlackWebhookOperator which is positioned at the start and end of the "ETL" process.
For the AirbyteTriggerSyncOperator, we had to setup 2 connection ids for the task - `airflow_airbyte_conn_id` and `airbyte_tvmazeapisf_conn_id`. This is for the ingestion of the data from the TV MAZE API to our datawarehouse on Snowflake. Then we setup the ECSOperator to trigger the dbt image which is hosted on ECR. For this, we needed the `aws-login-for-ecs-task`.
<figure> 
<img src="https://github.com/LuckyLukeAtGitHub/deb-project2-group2/blob/main/screenshots/dags_connjson.PNG" alt="aws-login-for-ecs-task" width="70%"> 
<figcaption>conn.json for ECSOperator</figcaption>
</figure>
</p>

</p>

<hr style="background:#ADD8E6;">
<!-- RESULTS AND DISCUSSION -->


<h2 id="discussion">Discussion, Lesson Learnt and Future Improvement</h2>

<p align="justify">

Current iteration Airbyte and dbt docker images are built and pushed onto ECR and task instance created to run the pipeline on EC2 with Airflow running locally on Luke's device.<br>
<b>Key Learnings and Room for Improvements:</b> 
<ul> 
 <li>How to pronounce the word Genre
  </li>
    <figure> 
<img src="https://github.com/LuckyLukeAtGitHub/deb-project2-group2/blob/main/screenshots/pronouncingGenre.PNG" alt="Pronouncing Genre" width="20%"> 
<br>
<figcaption><i>Sounds like "Zhon-Ruh"</i></figcaption>
</figure>
  <li>Learned when Implementing the Airbyte Connector, in the "parse_response" function, 
  the original codes from class reference the response in square brackets, ours didnt need that as it is already in a json object. </li>
  <li>When Implementing schemas for custom connector on Airbyte, each objects require a type (as object) and each type would have its own properties that can contain 
  the "columns" with their own type and properties.</li>
  <li>When starting an Airbyte EC2 instance following a non-graceful shutdown , use `sudo service docker status` to check if the docker daemon is running before running `docker-compose up -d`</li>
  <li>To avoid the above, run `sudo systemctl enable docker` to enable the docker daemon to auto start on boot and when your container is running, run `docker update --restart unless-stopped $(docker ps -q)` to ensure your airbyte container will auto start on the next reboot.</li>
  <li><i>"When it's curly braces it's an Object, if it's a square bracket it's a List"</i> - Luke, 2022</li>
  <li>For Snowflake permission, being the owner of the Database does not automatically grant access rights.
  <figure> 
<img src="https://github.com/LuckyLukeAtGitHub/deb-project2-group2/blob/main/screenshots/wordsofwisdom(snowflake).PNG" alt="Snowflake permission" width="100%"> 
</figure>
  </li>
  <li>When creating the custom connector, discovered that a Python Class name cannot be too long. Originally we had TV_MAZE_API as a class and that did not work, had to change it to just TVMAZE</li>
  <li>When experimenting and working with Airflow, definitely export all connectors first and delete everything that is not the DAG folder to save setup time.</li>
  <li>Create Airbyte Custom Connector Test and make use of dbt Macros</li>  
  <li>To improve the ETL notification messages - More unique and cater for failed pipeline.</li>
  <li>As New Airbyte connectors are regularly being added, did not realised that there is already a TVMaze connector in Alpha, we built one anyways!</li>
</ul>

</p>

<hr style="background:#ADD8E6;">
<!-- CONTRIBUTORS -->
<h2 id="contributors">Contributors & Contributions</h2>

<p>
  <i>All participants in this project are professional individuals enrolled in <a href="https://www.dataengineercamp.com">Data Engineering Camp</a> </i> <br> <br>
  
<table>
<tr>
<th>Name</th>
<th>GitHub</th>
<th>Contributions</th>
</tr>
<tr>
 <td> <b>Luke Huntley</b></td>
<td><a href="https://github.com/LuckyLukeAtGitHub">LuckyLukeAtGitHub</a></td>
<td>Airbyte, Docker Image Build & Upload, AWS (IAM, S3, EC2, ECR), Airflow</td>
</tr>

<tr>
 <td> <b>Helen Amin</b> </td>
  <td><a href="https://github.com/helenamin">Helenamin</a> </td>
  <td>dbt Transformation Models & Tests, Airflow</td>
 </tr>

<tr>
 <td> <b>Fang Xuan Foo</b></td>
<td><a href="https://github.com/foofx88">foofx88</a></td>
<td>Snowflake, Documentation, Airflow</td>
</tr>

</table>
</p>

<i>All Team members partook on the development,cross check and supplied content for project documentation. </i>
<i>This was the Second project for the ETL part of the course in the <a href="https://www.dataengineercamp.com">Data Engineering Camp</a>.</i> <br>

<a href="#top"> Go back up🔼</a>
