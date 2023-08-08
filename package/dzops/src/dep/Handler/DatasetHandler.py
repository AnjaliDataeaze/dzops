from dzops.src.dep.Manager.DatasetMetadataManager import *
from dzops.src.dep.Manager.DatasetRepositoryManager import *
from dzops.src.dep.Manager.DatasetDataReaderManager import *
import os
from dzops.src.dep.config.Connection import *
from dzops.src.dep.InputProperties import *
prop=properties()
connection = Connection()
conn = connection.get_connection()



class DatasetHandler:

    def RDSConfig(self,host, dbname , user, password):
        connection.create_connection( host=host, dbname=dbname, user=user, password=password)


    def dataset_custom_fields(self,corpusname,kv_pairs):
        datasetMetadataManager = DatasetMetadataManager()
        conn = connection.get_connection()
        datasetMetadataManager.dataset_custom_fields(corpusname, kv_pairs, conn)

    def list_commits(self):
        datasetRepositoryManager = DatasetRepositoryManager()
        datasetRepositoryManager.list_commits()
       
    def checkout(self, commitid):
        datasetRepositoryManager = DatasetRepositoryManager()
        datasetRepositoryManager.checkout(commitid)



    def list_dataset_names(self, filter_value):
         try:
             datasetMetadataManager = DatasetMetadataManager()
             conn = connection.get_connection()
 #            print(filter_value)
             answer = datasetMetadataManager.list_dataset_names(filter_value, conn)
  #           print(answer)
             if answer == []:
                 raise Exception("No corpus belongs to this filter  exist")
             for names in answer:
                 print(names['corpus_name'])
             return answer
         except Exception as e:
             raise e

    def get_dataset_metadata(self, corpus_name):
        try:
            datasetMetadataManager = DatasetMetadataManager()
            
            row1 = datasetMetadataManager.get_dataset_metadata_by_id(corpus_name, conn)
            if row1 ==[]:
                raise Exception("ENter valid corpus name")
            output=""
            str1={}
            
            for row in row1:
                output={
                        "corpus_id":row['corpus_id'],
                        "corpus_name":row['corpus_name'],
                        "language":row['language'],
                        "corpus_type":row['corpus_type'],
                        "source_type":row['source_type'],
                        "customer_name":row['customer_name'],
                        "data_domain_name":row['data_domain_name']
                        }
            response=json.dumps(output)
            return response
        except Exception as e:
            raise e
     
    def delete_dataset(self, corpus_name):
        try:
            datasetMetadataManager = DatasetMetadataManager()
            datasetMetadataManager.delete_dataset(corpus_name,conn)
            datasetRepositoryManager = DatasetRepositoryManager()
            datasetRepositoryManager.destroy()
        except Exception as e:
            raise e

    def update_dataset(self,json_loader):
        try:
            datasetMetadataManager = DatasetMetadataManager()
            if datasetMetadataManager.update_dataset(json_loader,conn)==1:
               return 1
            else:
                return 0
        except Exception as e:
            raise e

    def manager_get_metadata_type(self, corpus_type):
        try:
            datasetMetadataManager = DatasetMetadataManager()
            rows = datasetMetadataManager.get_dataset_metadata_by_type(corpus_type, conn)
            if rows ==[]:
                raise Exception("ENter valid corpus name")
            output=""
            # str1={}
            for row in rows:
                output={
                    "corpus_id":row['corpus_id'],
                    "corpus_name":row['corpus_name'],
                    "language":row['language'],
                    "corpus_type":row['corpus_type'],
                    "source_type":row['source_type'],
                    "customer_name":row['customer_name'],
                    "data_domain_name":row['data_domain_name']
                }
                # str1=((x, y) for x, y in output )
            response=json.dumps(output)
#            for i in response:
 #               print(i)
            return response
        except Exception as e:
            raise e

    def create_dataset(self, json_loader,target):
        try:
            datasetRepositoryManager1 = DatasetRepositoryManager()
            datasetRepositoryManager1.init()
            datasetRepositoryManager1.get_url(target)
            datasetMetadataManager = DatasetMetadataManager()
            datasetMetadataManager.create_dataset(json_loader, conn)

        except Exception as e:
            raise e

    def add_repo(self, target):
        try:
            datasetRepositoryManager1 = DatasetRepositoryManager()
            datasetRepositoryManager1.add(target)
        except Exception as e:
            raise e

    def commit_repo(self, str1):
        try:
            datasetRepositoryManager1 = DatasetRepositoryManager()
            datasetRepositoryManager1.commit(str1)
        except Exception as e:
            raise e

    def remote_repo(self, name,data, gita):
        try:
            datasetRepositoryManager1 = DatasetRepositoryManager()
            datasetRepositoryManager1.remote(name,data,gita)
            datasetMetadataManager=DatasetMetadataManager()
            datasetMetadataManager.update_dataset_remote(name,data,gita,conn)
        except Exception as e:
            raise e

    def clone_repo(self, args):
        try:
            DatasetRepositoryManager1 = DatasetRepositoryManager()
            DatasetRepositoryManager1.clone(args)
        except Exception as e:
            raise e

    def datareader(self, corpus_name, schema_type, custom_schema):
        try:
            DatasetDataReaderManager1 = DatasetDataReaderManager()
            path = os.getcwd()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            output = {"template_file_path": [],"data_dir_path":[], "common_schema": [], "native_schema": []}
            conn = connection.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("select * from corpus_metadata where corpus_name='" + corpus_name + "'")
            row = cursor.fetchone()
            cursor.execute("select * from corpus_custom_fields where corpus_id='" + str(row["corpus_id"]) + "'")
            result = cursor.fetchall()
            response=prop.input_properties(path,corpus_name,output,result)
            
            dataset = DatasetDataReaderManager1.read_data(corpus_name,response, schema_type, custom_schema=custom_schema)['data']
            return dataset
        except Exception as e:
            raise e

    def store_data(self, corpus_name, output_loc, schema_type, custom_schema=None):
        try:
            DatasetDataReaderManager1 = DatasetDataReaderManager()
            DatasetDataReaderManager1 = DatasetDataReaderManager()
            path = os.getcwd()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            output = {"template_file_path": [],"data_dir_path":[], "common_schema": [], "native_schema": []}
            conn = connection.get_connection()
    
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("select * from corpus_metadata where corpus_name='" + corpus_name + "'")
            row = cursor.fetchone()
            cursor.execute("select * from corpus_custom_fields where corpus_id='" + str(row["corpus_id"]) + "'")
            result = cursor.fetchall()
            response=prop.input_properties(path,corpus_name,output,result)

            if output_loc == ".":
                output_loc = os.getcwd()

            if schema_type == "custom":
                if custom_schema is not None:
                    dataset = DatasetDataReaderManager1.store_data(corpus_name,response, output_loc, schema_type, custom_schema)
                else:
                    return ("invalid custom_schema path")
            else:
               # print("&&&&&&&&&&&&&&&&&&",response,output_loc,schema_type)
                dataset = DatasetDataReaderManager1.store_data(corpus_name,response, output_loc, schema_type)

            return dataset
        except Exception as e:
            raise e

    def push_remote(self):
        try:
            connection = Connection()
            datasetRepositoryManager1 = DatasetRepositoryManager()
            datasetRepositoryManager1.push()
            datasetMetadataManager = DatasetMetadataManager()
            # print("xvz")
            # corpusMetadataManager.update_timestamp(conn,args)
        except Exception as e:
            raise e

    def pull_repo(self, audio):
        try:
            datasetRepositoryManager1 = DatasetRepositoryManager()
            datasetRepositoryManager1.pull(audio)
        except Exception as e:
            raise e
### ______________________________________________#########333
    def get_Counts(self):
        try:
            datasetMetadataManager = DatasetMetadataManager()
            return datasetMetadataManager.get_Counts(conn)
        except Exception as e:
            raise e

    def summary(self, column):
        datasetMetadataManager = DatasetMetadataManager()
        return datasetMetadataManager.summary(conn, column)

    def list_corpus(self , language , corpus_type ,  source_type):
        try:
            datasetMetadataManager = DatasetMetadataManager()
            return datasetMetadataManager.list_corpus(language , corpus_type ,  source_type, conn)
        except Exception as e:
            raise e
        
    def language(self,conn):
        datasetMetadataManager = DatasetMetadataManager()
        return datasetMetadataManager.language(conn)
    
    def source_type(self,conn):
        datasetMetadataManager = DatasetMetadataManager()
        return datasetMetadataManager.source_type(conn)
    
    def corpus_type(self,conn):
        datasetMetadataManager = DatasetMetadataManager()
        return datasetMetadataManager.dataset_type(conn)

    def search_corpus(self, corpus_name):
        try:
            datasetMetadataManager = DatasetMetadataManager()
            if datasetMetadataManager.search_dataset(corpus_name, conn) == 0:
                return 0
            else:
                return datasetMetadataManager.search_corpus(corpus_name, conn)
        except Exception as e:
            raise e

    def donut(self, column):
        datasetMetadataManager = DatasetMetadataManager()
        return datasetMetadataManager.donut(conn, column)

    def summary_custom(self, corpus_name):
        datasetMetadataManager = DatasetMetadataManager()
        return datasetMetadataManager.summary_cutom(conn, corpus_name)

    def update_custom_field(self, data):
        datasetMetadataManager = DatasetMetadataManager()
        if datasetMetadataManager.update_custom_field(data, conn) == 1:
            return 1
        else:
            return 2
