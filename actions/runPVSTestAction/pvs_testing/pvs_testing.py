# # ## TODO: Pass in credentials for TDV connection
# # ## TODO: Ensure script connects to TDV via passed in credentials
# # ## TODO: Implement PVS Test steps in python script
# # ## TODO: Once changelog is being passed in, parse values to obtain SPs

# # ## TODO: Create readme.md for documentation

# # ## TODO: Possible Pain-Point - Determine how to handle failed PVS_Test - Rollback mechanism or...

import os
from datetime import datetime
import pandas as pd
import teradatasql
import logging
import sys
import glob
import json
import xml.etree.ElementTree as ET

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# # Executes SQL query given against td_conn passed into function
# def _execute_tdv_query(td_conn, query):
#     query_result = pd.read_sql(query, td_conn)
#     logger.info({'query': query, 'result': query_result})

#     try:
#         return query_result.to_dict()
#     except Exception as e:
#         logger.info(str(e))
#         return {}


# # Returns results of the PVS TEST when passing in results from PVS TEST TABLE sql query
# def _pass_or_fail(result_dict):
#     pvs_result = result_dict['TEST_STATUS'][0]
#     logger.info(pvs_result)
#     if pvs_result == 'FAILED':
#         logger.info("FAILURE")
#         exit(1)

#fetch files from the tables folder
def find_sp_pairs(base_folder):
    tables_path = os.path.join(base_folder, 'tables')

    sp_def_files = []
    sp_run_files = []

    if not os.path.exists(tables_path):
        print(f"No tables directory in {base_folder}")
        return []

    for filename in os.listdir(tables_path):
        if filename.startswith("BLUE_PRINTS_SAMPLE_SPROC_") and filename.endswith(".sql"):
            sp_def_files.append(os.path.join(tables_path, filename))
        if filename.startswith("BLUE_PRINTS_SAMPLE_RUN_SPROC_") and filename.endswith(".sql"):
            sp_run_files.append(os.path.join(tables_path, filename))

    # Sort both lists to maintain pair order
    sp_def_files.sort()
    sp_run_files.sort()

    return list(zip(sp_def_files, sp_run_files))


# # Main function to perform PVS Test against specified stored procedures
# def main():
#     # Read environment variables
#     tdv_username = os.getenv("TDV_DEV_USERNAME")
#     tdv_password = os.getenv("TDV_DEV_PASSWORD")
#     print(f"Username: {tdv_username}")
#     print(f"Password: {tdv_password}")
#     tdv_env = os.getenv("TDV_ENV", "").strip().lower()
#     folder_list_raw = os.getenv("FOLDER_LIST", "[]").strip()
    
#     print(f"🔍 DEBUG: TDV_ENV = {tdv_env}")
#     print(f"🔍 DEBUG: Raw Folder List = {folder_list_raw}")
    
#     # Correctly parse FOLDER_LIST as a JSON array
#     try:
#         folder_list = json.loads(folder_list_raw)  # Convert string to list
#     except json.JSONDecodeError:
#         print(" ERROR: FOLDER_LIST is not a valid JSON list.")
#         sys.exit(1)
    
#     # Ensure we only get valid folder paths
#     folder_list = [folder.strip() for folder in folder_list if folder.strip()]
    
#     # Validation checks
#     if not folder_list:
#         print(" ERROR: No folder paths received.")
#         sys.exit(1)
    
#     if not tdv_env:
#         print(" ERROR: No environment (TDV_ENV) received.")
#         sys.exit(1)
    
#     # Construct expected changelog filename
#     changelog_filename = f"{tdv_env}.changelog.xml"
    
#     # Process each folder
#     for folder in folder_list:
#         print(f"Checking Folder: {folder}")
    
#         if os.path.isdir(folder):
#             changelog_file = os.path.join(folder, changelog_filename)
#             print(f"Checking for file: {changelog_file}")
    
#             if os.path.exists(changelog_file):
#                 print(f"Processing Changelog: {changelog_file}")
#                 # 🔹 Add processing logic here (e.g., parse XML, run Liquibase, etc.)
#                 sp_names = extract_sql_names_from_changelog(changelog_file)
#                 print(f"Extracted SQL names from changelog: {sp_names}")
#             else:
#                 print(f"WARNING: No file found at '{changelog_file}'")
#         else:
#             print(f"WARNING: Folder does not exist - '{folder}'")

#     ## TODO: Uncomment and integrate after changelog input feature complete
    
#     ## Initialize variables with environment variable values for usage
#     # teradata_username = os.environ.get("TDV_USERNAME")
#     # teradata_password = os.environ.get("TDV_PASSWORD")
#     # teradata_host_server = "hstntduat.healthspring.inside"
#     # ## Parse the stored procedures into a list from a string
#     # stored_procedures = [name.strip() for name in str(os.environ.get("STORED_PROCEDURES")).split(',') if name.strip()]
#     # logger.info(f"STORED PROCEDURES VALUES: {stored_procedures}")
    
#     ## Intialize variables with dynamic definitions constructed from parameters/env vars
#     ## TODO: Change work item id to be a pass value once change tickets are implemented
#     # work_item_id = "CHG33333_CTASK33333:"
#     # pvs_table_result_query = f"select TEST_STATUS from PVS_TEST.PVS_TEST_INFO_V where USER_NAME = '{teradata_username}' and WORK_ITEM = '{work_item_id}'"
#     # start_test_procedure = f"CALL PVS_TEST.START_PVS_TEST('{teradata_username}','{work_item_id}',PROC_MSG)"
#     # end_test_procedure = f"CALL PVS_TEST.END_PVS_TEST('{teradata_username}','{work_item_id}',PROC_MSG)"
    
#     # Parse incoming string into list of strings delimited by ,
#     # stored_procedures = [name.strip() for name in str(os.environ.get("STORED_PROCEDURES")).split(',') if name.strip()]
#     # logger.info(f"STORED PROCEDURES VALUES: {stored_procedures}")
    
#     # with teradatasql.connect(
#     #         host=teradata_host_server,
#     #         user=teradata_username,
#     #         password=teradata_password,
#     #         LOGMECH="LDAP",
#     #         encryptdata=True
#     # ) as td_conn:
    
#     # Start PVS Test
#     # logger.info(f"Executing Start PVS Test")
#     # execute_tdv_query(td_conn=td_conn, query=start_test_procedure)

#     # Run stored procedure(s)
#     for sp in sp_names:
#         logger.info(f"Executing Stored Procedure: {sp}")
#         # _execute_tdv_query(td_conn=td_conn, query=sp)

#     # # End PVS Test
#     # logger.info(f"Executing End PVS Test")
#     # execute_tdv_query(td_conn=td_conn, query=end_test_procedure)

#     # # Get results
#     # logger.info(f"Result of PVS Test")
#     # pvs_result = execute_tdv_query(td_conn=td_conn, query=pvs_table_result_query)
#     # pass_or_fail(pvs_result)

# if __name__ == "__main__":
#     main()

def main():
    teradata_username = os.environ.get("TDV_USERNAME")
    teradata_password = os.environ.get("TDV_PASSWORD")
    teradata_env = os.environ.get("TDV_ENV")
    teradata_dir_list = os.environ.get("DIRECTORY_LIST")
    teradata_folder_list = os.environ.get("FOLDER_LIST")
    logger.info(f"DIRECTORY_LIST: {teradata_dir_list}")
    logger.info(f"FOLDER_LIST: {teradata_folder_list}")
    print(teradata_username)
    print(teradata_password)
    print(teradata_env)
    print(teradata_dir_list)
    print(teradata_folder_list)
    folder_list = os.environ.get("FOLDER_LIST")
    if not folder_list:
        print("FOLDER_LIST not found in env")
        return

    try:
        folder_list = json.loads(folder_list)  # Clean parsing of ["path1", "", "", "path2"]
    except Exception as e:
        print("Failed to parse FOLDER_LIST:", e)
        return

    # Remove empty strings from the list
    folder_list = [folder for folder in folder_list if folder.strip()]

    for folder in folder_list:
        print(f"Searching in Folder: {folder}")
        pairs = find_sp_pairs(folder)
        print(f"Found {len(pairs)} SP File Pairs in {folder}")
        for sp_def, sp_run in pairs:
            print(f"SP Def: {sp_def} -- SP Run: {sp_run}")





if __name__ == "__main__":
    main()


            

