from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.saas.analytics import Snowflake
from diagrams.onprem.analytics import Dbt
from diagrams.onprem.workflow import Airflow
from diagrams.digitalocean.compute import Docker, Containers
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

#Setup Graph Attribute
graph_attr = {"fontsize":"14", "bgcolor": "white"}
node_attr = {"fontsize":"12", "fontcolor":"black"}
main_clus = {"fontsize":"13", "fontcolor":"black", "bgcolor":"#6694CC", "pencolor":"black"}
to_clus = {"fontsize":"13", "fontcolor":"black", "bgcolor":"#99B7DD", "pencolor":"black"}
sub_clus = {"fontsize":"13", "fontcolor":"black", "bgcolor":"#CCDBEE", "pencolor":"black"}

#Create Layout for the diagram
with Diagram("TVSHOW SA Diagram", show=True, graph_attr=graph_attr, node_attr=node_attr, direction='LR'):

    with Cluster("Task Ochestration", graph_attr=main_clus):
        task_ochestration = Airflow("Ochestrates")
        
        with Cluster("ELTL", graph_attr=to_clus):
            with Cluster("Incremental Extract", graph_attr=sub_clus):
                extract = Docker("Airbyte TVMaze \n Custom Connector") - Edge(color="black", style="dashed") - EC2("RUN INSTANCE")
                task_ochestration >> Edge(color="black") >> extract

            with Cluster("Source Load", graph_attr=sub_clus):
                raw_load = Snowflake("TVSHOW.SOURCE")

            with Cluster("Transform", graph_attr=sub_clus):
                transform = Dbt("MODELING") - Edge(color="black", style="dashed") - EC2("RUN INSTANCE")
                task_ochestration >> Edge(color="black") >> transform 

            with Cluster("Model Load", graph_attr=sub_clus):
                model_load = Snowflake("TVSHOW.MODEL")

#Connecting everything up
    extract >> Edge(color="black")>> raw_load << Edge(color="black")>> transform >> Edge(color="black")>> model_load
