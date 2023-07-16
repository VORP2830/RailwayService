import requests
import schedule
import time
from datetime import datetime, timedelta
from pytz import timezone
import os

def restart_api():
    url = "https://backboard.railway.app/graphql/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.environ.get("TOKEN")
    }
    query = """
        query Deployments {{
            deployments(input: {{serviceId: "{}"}}) {{
                edges {{
                    node {{
                        id
                        serviceId
                        status
                    }}
                }}
            }}
        }}
    """.format(os.environ.get("SERVICEID"))
    response = requests.post(url, headers=headers, json={"query": query})
    data = response.json()

    deployments = data["data"]["deployments"]["edges"]
    last_successful_node = None

    for deployment in deployments:
        node = deployment["node"]
        if node["status"] == "SUCCESS":
            last_successful_node = node
    if last_successful_node is not None:
        last_successful_id = last_successful_node["id"]
        mutation = """
            mutation DeploymentRestart {
                deploymentRestart(id: "%s")
            }
        """ % last_successful_id
        response = requests.post(url, headers=headers, json={"query": mutation})
        data = response.json()
        print("Mutation response:", data)
        if data.get("data", {}).get("deploymentRestart") == True:
            restart_time = datetime.now(timezone("America/Sao_Paulo")).strftime("%Y-%m-%d %H:%M:%S")
            print("API reiniciada com sucesso em", restart_time)
    else:
        print("Nenhum nó com status SUCCESS encontrado.")

restart_api()
