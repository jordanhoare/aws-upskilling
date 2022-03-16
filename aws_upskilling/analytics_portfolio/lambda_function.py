import os
import time

import boto3

# Environment Variables
DATABASE = os.environ["DATABASE"]
TABLE = os.environ["TABLE"]
# Top X Constant
TOPX = 5
# S3 Constant
S3_OUTPUT = f's3://{os.environ["BUCKET_NAME"]}/query_results/'
# Number of Retries
RETRY_COUNT = 10


def lambda_handler(event, context):
    client = boto3.client("athena")
    # query variable with two environment variables and a constant
    query = f"""
        SELECT track_name as \"Track Name\", 
                artist_name as \"Artist Name\",
                count(1) as \"Hits\" 
        FROM {DATABASE}.{TABLE} 
        GROUP BY 1,2 
        ORDER BY 3 DESC
        LIMIT {TOPX};
    """
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": DATABASE},
        ResultConfiguration={"OutputLocation": S3_OUTPUT},
    )
    query_execution_id = response["QueryExecutionId"]
    # Get Execution Status
    for i in range(0, RETRY_COUNT):
        # Get Query Execution
        query_status = client.get_query_execution(QueryExecutionId=query_execution_id)
        exec_status = query_status["QueryExecution"]["Status"]["State"]
        if exec_status == "SUCCEEDED":
            print(f"Status: {exec_status}")
            break
        elif exec_status == "FAILED":
            raise Exception(f"STATUS: {exec_status}")
        else:
            print(f"STATUS: {exec_status}")
            time.sleep(i)
    else:
        client.stop_query_execution(QueryExecutionId=query_execution_id)
        raise Exception("TIME OVER")
    # Get Query Results
    result = client.get_query_results(QueryExecutionId=query_execution_id)
    print(result["ResultSet"]["Rows"])
    # Function can return results to your application or service
    # return result['ResultSet']['Rows']
