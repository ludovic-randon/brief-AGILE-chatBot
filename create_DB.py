import xml.etree.ElementTree as ET
import html2markdown
import os
import pymongo
from pymongo import MongoClient

data_path = fr'{os.getenv("HOME")}/Documents/Briefs/2_Block_janv_fev/20210208_Brief_Agile/Datas'
#subdir = "workplace.meta.stackexchange.com"
file_name = "Posts.xml"


def create_mongodb_database(src, file_name):
    '''
    DESCRIPTION :   Create a mongodb DataBase using all post files
                    in subdir of src
    '''
    #os.path.join(data_path, file)
    for subdir in os.listdir(src):
        current_path = os.path.join(src, subdir)
        print(current_path)
        for file in os.listdir(current_path):
            if file == file_name:
                posts_tree = ET.parse(os.path.join(current_path, file))
                posts = posts_tree.getroot()

                if "meta" in subdir:
                    topic = subdir[:-23]
                    print(topic)
                else:
                    topic = subdir[:-17]

                post_list = [row.attrib for row in posts]
                for post in post_list: 
                    post['Body'] = html2markdown.convert(post['Body'])
                    post['Topic'] = topic

                ## Connexion to mongodb with pymongo
                connection = MongoClient() ## connects by default to db at localhost:27017

                ## Create DataBase
                db = connection["StarkBotBD"] 

                ## Ajout collection
                Quest_Rep = db["Quest_Rep"] 

                ## Insert elements
                db.Quest_Rep.insert(post_list)

                # ## Create Index
                # db.Quest_Rep.drop_index()
                #### Text search
                db.Quest_Rep.create_index([('Title', 'text'), ('Body', 'text')],
                          weights = {'Title':2, 'Body':1}, 
                          name = "text_search")
                #### Topic
                db.Quest_Rep.create_index("Topic")
                #### Score
                db.Quest_Rep.create_index("Score")
                #### PostTypeId
                db.Quest_Rep.create_index("PostTypeId")
                #### ParentId
                db.Quest_Rep.create_index("ParentId")

if __name__=="__main__":
    create_mongodb_database(data_path, file_name)