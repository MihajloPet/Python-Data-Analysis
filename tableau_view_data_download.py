


from tableau_api_lib import TableauServerConnection
from tableau_api_lib.utils import querying, flatten_dict_column, extract_pages
import pandas as pd
import io
import urllib




def df_from_tableau_view(server_url, api_ver, site_name,site_url, personal_access_token_name, personal_access_token_secret, project_name, wb_name, view_to_query, variable_dict):

	#connection sequence
	config = {
	        'my_env': {
	                'server': server_url,
	                'api_version': api_ver,
	#                 'username': user_name, #for some reason, not working with password, only wirh personal token
	#                 'password': password,
	            
	                'personal_access_token_name': personal_access_token_name,
	                'personal_access_token_secret':personal_access_token_secret,
	                'site_name': site_name,
	                'site_url': site_url
	        }
	}
	#connect to tableau server
	conn = TableauServerConnection(config, env='my_env')
	conn.sign_in()


	#get all views and dashboards in form of dataframe
	views_df = querying.get_views_dataframe(conn=conn)

	#flatten dataframe - extract project and workbook data
	#both commands have to be executed in order to be able to filter project and workbook
	#extract data from workbook column and add keys to columns
	views_with_wb_info_df = flatten_dict_column(df=views_df,
	                                           keys=['name','id'],
	                                           col_name='workbook')

	#extract data from project column and add keys to columns - 
	views_with_wb_and_project_info_df = flatten_dict_column(df=views_df,
	                                           keys=['name','id'],
	                                           col_name='project')

	#---------------------------------------
	#should split this into two functions

	#------------------------------------------------
	

	#get sheet id where sheet name == view_to_query
	view_id = views_with_wb_and_project_info_df.loc[((views_with_wb_and_project_info_df['project_name']==project_name)&
	                                     (views_with_wb_and_project_info_df['workbook_name']==wb_name)&
	                                     (views_with_wb_and_project_info_df['name']==view_to_query)),'id'].values[0]

	#create filtering sequence
	custom_url_params = {}
	for key in variable_dict.keys():
	    vr_name = urllib.parse.quote(key)
	    vr_val = urllib.parse.quote(','.join(variable_dict[key]))
	    #append to dict
	    custom_url_params[key] =  f"vf_{vr_name}={vr_val}"

	#
	views_data_response_param = conn.query_view_data(view_id=view_id, parameter_dict=custom_url_params)
	urlData = views_data_response_param.content
	df = pd.read_csv(io.StringIO(urlData.decode('utf-8')))

	#disconnect from Tableau Server
	conn.sign_out()

	return df
