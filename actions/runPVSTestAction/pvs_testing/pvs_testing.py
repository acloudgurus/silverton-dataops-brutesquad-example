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
    # Read environment and folder paths from GitHub Actions inputs
    tdv_env = os.getenv("TDV_ENV").lower()
    folder_paths = os.getenv("FOLDER_LIST", "").split()
    
    if not folder_paths:
        print("Error: No folder paths received.")
        sys.exit(1)
    
    if not tdv_env:
        print("Error: No environment (TDV_ENV) received.")
        sys.exit(1)
    
    # Construct the expected file name format
    changelog_filename = f"{tdv_env}.changelog.xml"
    print(changelog_filename)
    
    # Process each folder
    for folder in folder_paths:
        folder = folder.strip()
        print(f"Folder : {folder}")
        if os.path.isdir(folder):
            # Search for {TDV_ENV}.changelog.xml inside the folder
            changelog_file = os.path.join(folder, changelog_filename)
    
            if os.path.exists(changelog_file):
                print(f"Processing Changelog for Environment '{tdv_env}': {changelog_file}")
            else:
                print(f"❌ WARNING: No file found at '{changelog_file}'")
        else:
            print(f"❌ WARNING: Folder does not exist - '{folder}'")
            # Add processing logic here
            

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
