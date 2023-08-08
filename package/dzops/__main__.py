#commit

from dzops.src.dep.udataset import udataset
from dzops.src.dep.UserAccessControl import AccessControl
from dzops.src.dep.Handler.dvchandler import dvchandler
from dzops.src.dep.config.teamusermanager import teamusermanager
from typing import Optional, List
import re
import json
import shutil
import os
import typer
from datetime import datetime
import configparser
app = typer.Typer(name="udops",add_completion=False,help="Udops utility")

try:
########----------- UAC-------------##########

    @app.command()
    def login(token:str,username:str,teamname:str):
        Userlog = AccessControl()
        Userlog.login(token,username)
        dvchandler1 = dvchandler()
        dvchandler1.team_authenticator(username,teamname)
        

    @app.command()
    def logout():
        Userlog =AccessControl()
        Userlog.logout()

# Corpus commands

    @app.command()
    def RDSConfig(host: str = typer.Option(...,"--host"),
                  dbname: str = typer.Option(...,"--dbname"),
                  username: str = typer.Option(...,"--username"),
                  password: str = typer.Option(...,"--password")):
        udataset.RDSConfig(host = host , dbname = dbname , user = username, password = password)
    
    @app.command()
    def delete_dataset(corpusname):
        udataset.delete_dataset(corpusname)

    @app.command()
    def listDatasetNames(filter_value: str):
        udataset.listDatasetNames(filter_value)

    @app.command()
    def getDatasetMetadata(corpus_id: str):  # take one argument
        
        response=udataset.getDatasetMetadata(corpus_id)
        print(response)

    @app.command()
    def getDatasetMetadatabytype(corpus_type: str):
        response=udataset.getDatasetMetadatabytype(corpus_type)


    @app.command()
    def create_dataset(corpus_name: str = typer.Option(..., "--corpus_name") ,
                      corpustype: str = typer.Option(..., "--corpus_type"),
                      language : str = typer.Option(..., "--language"),
                      source:str = typer.Option(..., "--source_url"),
                      source_type:str = typer.Option(..., "--source_type") , vendor :str = typer.Option(..., "--vendor"),
                      domain: Optional[str] =typer.Option(None, "--domain"),
                      description : Optional[str] = typer.Option(None,"--description" ),
                      lang_code: str = typer.Option(..., "--lang_code") ,
                      acquisition_date: datetime = typer.Option(None,"--acquisition_date"),
                      migration_date : datetime = typer.Option(None,"--migration_date"),
                     ):
        
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_name = os.path.join(dir_path, 'src/dep/config/udops_config')
        def is_file_present(file_name):
            current_directory = os.getcwd()
            directory = os.path.join(current_directory, file_name)
            return os.path.isfile(directory)
        
        file_exists = is_file_present(file_name)
        if file_exists:
            
            config = configparser.ConfigParser()
            config.read(file_name)
            ACCESS_TOKEN = config.get('github', 'access_token')
            team_name = config.get('github', 'team_name')
            
            
            authentication = AccessControl()
            # fetching user id from udops_user table
            user_id = authentication.authenticate(ACCESS_TOKEN)
            
             # fetching team-id from cfg_udops_teams_metadata
            team_id = authentication.get_user_team(team_name)
            
            if team_id==0:
                return "team not found"
            else:
                if re.match("r'^s3://([\w.-]+)/(.+)$'", source) == True:
                   Source_tenant = input("Enter Source Tenant name:")
                   User_Token = input("Enter User Token:") # Partial change for import of data
                   AccessControl().partial_change(Source_tenant,User_Token)
                   if corpus_name == os.path.basename(os.getcwd()):
                        corpus_details = {
                        "corpus_name": corpus_name,
                        "corpus_type": corpustype,
                        "language": language,
                        "source_type": source_type,
                        "vendor": vendor,
                        "domain": domain,
                        "description": description,
                        "lang_code":lang_code,
                        "acquisition_date": acquisition_date,
                        "migration_date": migration_date,
                        
                
                             }
                        udataset.init(corpus_details,source)
                        corpus_id = authentication.corpus_id(corpus_name)
                        authentication.default_access(corpus_id,user_id)
                        authentication.Corpus_team_map(team_id , corpus_id)
                        AccessControl().retrieve_change()
                   else:
                        return "Corpus name and folder name should be same"
                else:
                    if corpus_name == os.path.basename(os.getcwd()):
                       
                        corpus_details = {
                        "corpus_name": corpus_name,
                        "corpus_type": corpustype,
                        "language": language,
                        "source_type": source_type,
                        "vendor": vendor,
                        "domain": domain,
                        "description": description,
                        "lang_code":lang_code,
                        "acquisition_date": acquisition_date,
                        "migration_date": migration_date,
                        
                        }
                        udataset.init(corpus_details,source)
                        corpus_id = authentication.corpus_id(corpus_name)
                        authentication.default_access(corpus_id,user_id)
                        authentication.Corpus_team_map(team_id , corpus_id)
                        AccessControl().retrieve_change()
                    else:
                        return print("Corpus name and folder name should be same")
        else:
            print(f"The file '{file_name}' does not exist in the current working directory.")

    @app.command()
    def dataset_custom_fields(corpusname , data: List[str]):
        """
        Process multiple key-value pairs
        """
        """
        Map key-value pairs to a name
        """
        kv_pairs = dict()
        for i in data:
            for pair in i.split():
                key, value = pair.split('=')
                kv_pairs[key] = value
        udataset.dataset_custom_fields(corpusname , kv_pairs)
    
    @app.command()
    def dataset_custom_fields(datasetname , data:List[str]):
        kv_pairs = dict()
        for i in data:
            for pair in i.split():
                key , value = pair.split('=')
                kv_pairs[key] = value
        udataset.corpus_custom_fields(datasetname , kv_pairs)

    @app.command()
    def list_commits():
        udataset.list_corpus()

    @app.command()
    def checkout(commitid):
        udataset.checkout(commitid)

    @app.command()
    def add(target: str):
        udataset.add(target)
    
    @app.command()
    def remote(name : str,data:str, gita: str):
        udataset.remote(name, data, gita)
        

    @app.command()
    def commit(message: str):
        udataset.commit(message)
    
    @app.command()
    def push(corpus_name):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_name = os.path.join(dir_path, 'src/dep/config/udops_config')
        def is_file_present(file_name):
            current_directory = os.getcwd()
            directory = os.path.join(current_directory, file_name)
            return os.path.isfile(directory)

        authentication = AccessControl()
        corpus_id = authentication.corpus_id(corpus_name)

        file_exists = is_file_present(file_name)

        if file_exists:
            config = configparser.ConfigParser()
            config.read(file_name)
            ACCESS_TOKEN = config.get('github', 'access_token')
            authentication = AccessControl()
            user_id = authentication.authenticate(ACCESS_TOKEN)
            access_type = "write"

            if authentication.authorize_user(user_id,corpus_id,access_type) == 1:
                print("Valid user.....")
                return udataset().push()
            else:
                print("ACCESS DENY")
        else:
            print(f"The file '{file_name}' does not exist in the current working directory.")



    @app.command()
    def save(message:str):
        udataset.commit(message)
        udataset.push()
    
    @app.command()
    def clone(git:str):
        corpus_name = re.sub(r'^.*/(.*?)(\.git)?$', r'\1', git)
        authentication = AccessControl()
        corpus_id = authentication.corpus_id(corpus_name)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_name = os.path.join(dir_path, 'src/dep/config/udops_config')
        def is_file_present(file_name):
            return os.path.isfile(file_name)
        file_exists = is_file_present(file_name)
        
        if file_exists:
            config = configparser.ConfigParser()
            config.read(file_name)
            ACCESS_TOKEN = config.get('github', 'access_token')
            authentication = AccessControl()
            user_id = authentication.authenticate(ACCESS_TOKEN)
            # check the permission from cfg_udops_acl (read, write)
            if authentication.authorize_user_clone(user_id,corpus_id)==1:
                return udataset.clone(git)
            else:
                print("No access for user to clone corpus")
        else:
            print(f"The file '{file_name}' does not exist in the current working directory.")
            
            return udataset.clone(git)
    
    @app.command()
    def fetch(git:str,folder:Optional[str] =typer.Argument(None)):
        udataset.clone(git)
        s = re.sub(r'^.*/(.*?)(\.git)?$', r'\1', git)
        os.chdir(s)
        udataset.pull(folder)

    @app.command()
    def pull(corpus_name,folder: Optional[str] =typer.Argument(None)):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_name = os.path.join(dir_path, 'src/dep/config/udops_config')
        def is_file_present(file_name):            
            return os.path.isfile(file_name)

        authentication = AccessControl()
        corpus_id = authentication.corpus_id(corpus_name)
        file_exists = is_file_present(file_name)

        if file_exists:
            config = configparser.ConfigParser()
            config.read(file_name)
            ACCESS_TOKEN = config.get('github', 'access_token')
            authentication = AccessControl()
            user_id = authentication.authenticate(ACCESS_TOKEN)
            access_type = "write"
            if authentication.authorize_user(user_id, corpus_id, access_type) == 1:
                return udataset.pull(folder)
            else:
                print("ACCESS DENY")
        else:
            print(f"The file '{file_name}' does not exist in the current working directory.")



    @app.command()
    def datareader(corpus_details_dict, schema_type : Optional[str] =typer.Argument("common"),custom_schema:Optional[str] =typer.Argument(None)):
        udataset.datareader(corpus_details_dict, schema_type, custom_schema)

    @app.command()

    def export_data(corpus_details_dict, output_loc, schema_type : Optional[str] =typer.Argument("common"), custom_schema:Optional[str] =typer.Argument(None) ):
        udataset.store_data(corpus_details_dict,output_loc,schema_type,custom_schema)

   

    @app.command()
    def user_authentication(source_dir:str):

        pass



except Exception as e:
    raise e


if __name__ == "__main__":
    app()

    
