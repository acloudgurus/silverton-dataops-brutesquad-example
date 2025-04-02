# ## TODO: Pass in credentials for TDV connection
# ## TODO: Ensure script connects to TDV via passed in credentials
# ## TODO: Implement PVS Test steps in python script
# ## TODO: Once changelog is being passed in, parse values to obtain SPs

# ## TODO: Create readme.md for documentation

# ## TODO: Possible Pain-Point - Determine how to handle failed PVS_Test - Rollback mechanism or...

import os
from datetime import datetime
import pandas as pd
import teradatasql
import logging
import sys
import glob
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Executes SQL query given against td_conn passed into function
def _execute_tdv_query(td_conn, query):
    query_result = pd.read_sql(query, td_conn)
    logger.info({'query': query, 'result': query_result})

    try:
        return query_result.to_dict()
    except Exception as e:
        logger.info(str(e))
        return {}


# Returns results of the PVS TEST when passing in results from PVS TEST TABLE sql query
def _pass_or_fail(result_dict):
    pvs_result = result_dict['TEST_STATUS'][0]
    logger.info(pvs_result)
    if pvs_result == 'FAILED':
        logger.info("FAILURE")
        exit(1)


# Main function to perform PVS Test against specified stored procedures
def main():
    # Read environment variables
    tdv_env = os.getenv("TDV_ENV", "").strip().lower()
    folder_list_raw = os.getenv("FOLDER_LIST", "[]").strip()
    
    print(f"🔍 DEBUG: TDV_ENV = {tdv_env}")
    print(f"🔍 DEBUG: Raw Folder List = {folder_list_raw}")
    
    # Correctly parse FOLDER_LIST as a JSON array
    try:
        folder_list = json.loads(folder_list_raw)  # Convert string to list
    except json.JSONDecodeError:
        print(" ERROR: FOLDER_LIST is not a valid JSON list.")
        sys.exit(1)
    
    # Ensure we only get valid folder paths
    folder_list = [folder.strip() for folder in folder_list if folder.strip()]
    
    # Validation checks
    if not folder_list:
        print(" ERROR: No folder paths received.")
        sys.exit(1)
    
    if not tdv_env:
        print(" ERROR: No environment (TDV_ENV) received.")
        sys.exit(1)
    
    # Construct expected changelog filename
    changelog_filename = f"{tdv_env}.changelog.xml"
    
    # Process each folder
    for folder in folder_list:
        print(f"Checking Folder: {folder}")
    
        if os.path.isdir(folder):
            changelog_file = os.path.join(folder, changelog_filename)
            print(f"Checking for file: {changelog_file}")
    
            if os.path.exists(changelog_file):
                print(f"Processing Changelog: {changelog_file}")
                # 🔹 Add processing logic here (e.g., parse XML, run Liquibase, etc.)
                try:
                    with open(changelog_file, 'r') as file:
                        contents = file.read()
                        print(f"📂 File Contents of '{changelog_file}':\n{'-'*60}")
                        print(contents)
                        print('-'*60)
                except Exception as e:
        print(f"❌ ERROR reading file: {changelog_file} - {e}")
            else:
                print(f"WARNING: No file found at '{changelog_file}'")
        else:
            print(f"WARNING: Folder does not exist - '{folder}'")

if __name__ == "__main__":
    main()
            

    # logger.info(f"Hello from the script")
    # work_item_id = str(datetime.now().strftime("%Y%m%d%H%M"))

    # ### DO NOT TRY TO PRINT SECRETS - GITHUB MASKS THESE VALUES WHEN PRINTED
    # teradata_username = os.environ.get("TDV_USERNAME")
    # teradata_password = os.environ.get("TDV_PASSWORD")

    # teradata_host_server = "hstntduat.healthspring.inside"

    # ## TODO: Changing workitem id
    # work_item_id = "CHG77777_CTASK77777:"
    # pvs_table_result_query = f"select TEST_STATUS from PVS_TEST.PVS_TEST_INFO_V where USER_NAME = 'SVT_DATAOPS_DEV' and WORK_ITEM = '{work_item_id}'"
    # start_test_procedure = f"CALL PVS_TEST.START_PVS_TEST('SVT_DATAOPS_DEV','{work_item_id}',PROC_MSG)"
    # end_test_procedure = f"CALL PVS_TEST.END_PVS_TEST('SVT_DATAOPS_DEV','{work_item_id}',PROC_MSG)"
    # stored_procedure = "CALL HSETL_WORK_DEV.BLUEPRINT_SAMPLE_SPROC()"

    # with teradatasql.connect(
    #         host=teradata_host_server,
    #         user=teradata_username,
    #         password=teradata_password,
    #         LOGMECH="LDAP",
    #         encryptdata=True
    # ) as td_conn:
    #     # Start PVS Test
    #     logger.info(f"Executing Start PVS Test")
    #     _execute_tdv_query(td_conn=td_conn, query=start_test_procedure)

    #     # Run stored procedure(s)
    #     logger.info(f"Executing Stored Procedure: {stored_procedure}")
    #     _execute_tdv_query(td_conn=td_conn, query=stored_procedure)

    #     # End PVS Test
    #     logger.info(f"Executing End PVS Test")
    #     _execute_tdv_query(td_conn=td_conn, query=end_test_procedure)

    #     # Get results
    #     logger.info(f"Result of PVS Test")
    #     pvs_result = _execute_tdv_query(td_conn=td_conn, query=pvs_table_result_query)
    #     _pass_or_fail(pvs_result)


if __name__ == "__main__":
    main()
