import xml.etree.ElementTree as ET
import html2markdown
import os
from pymongo import MongoClient
import json

data_path = fr'{os.getenv("HOME")}/YOUR_PATH/data'
# subdir = "workplace.meta.stackexchange.com"
file_name = "Posts.xml"


def add_posts(data, language, topic, Id=1, old_Id=1):
    posts = []
    for i in range(len(data['conversations'])):
        for j in range(2):
            if j == 0:
                PostTypeId = 1
                post = {
                    'Id': Id,
                    'PostTypeId': str(PostTypeId),
                    'Score': '1',
                    "ViewCount": "1",
                    'Title': data['conversations'][i][j],
                    "AnswerCount": "1",
                    'Language': language,
                    'Topic': topic,
                }
            else:
                PostTypeId = 2
                post = {
                    'Id': Id,
                    'PostTypeId': str(PostTypeId),
                    'ParentId': str(old_Id),
                    'Score': '1',
                    'Body': data['conversations'][i][j],
                    'Language': language,
                    'Topic': topic,
                }
            posts.append(post)
            old_Id = Id
            Id += 1
    return posts, Id, old_Id


def create_mongodb_database(src, file_name):
    '''
    DESCRIPTION :   Create StarkBotBD mongoDB using all "Posts.xml" files
                    in SUBDIR of SRC
    '''
    # os.path.join(data_path, file)
    Id = 1
    old_Id = 1
    posts_list = []

    # Connexion to mongodb with pymongo
    # DEFAULT connexion to LOCAL HOST at port 27017
    try:
        connection = MongoClient()
        print("SUCCESSFULLY connected to StarkBotBD :-)")
    except MongoClient.DoesNotExist:
        print("Could NOT connect to StarkBotBD :-(")

    # STARKBOT DB creation
    db = connection["StarkBotBD"]

    # QUEST_REP collection creation in StarkBotDB
    collection_Quest_Rep = db.Quest_Rep
    # SUGGESTION collection creation in StarkBotDB
    # collection_Suggestion = db.Suggestion
    # EMOTION collection creation in StarkBotDB
    # collection_Emotion = db.Emotion
    # RATING collection creation in StarkBotDB
    # collection_Rating = db.Rating

    # INITIAL posts COUNT in DB
    init_present_posts = collection_Quest_Rep.count_documents({})
    print(init_present_posts, "posts are stored in", db.name)

    # Subdir SRC or DATA_PATH SCAN
    # MAKE SURE THAT json OR xml FILES ARE IN
    # A SUBDIR OF YOUR DATA_PATH
    for subdir in os.listdir(src):
        current_path = os.path.join(src, subdir)
        print(current_path)

        # FILES SCAN in SUBDIR
        for file in os.listdir(current_path):

            # YOUR_FILE_Posts.xml load into StarkBotDB
            if file == file_name:
                posts_tree = ET.parse(os.path.join(current_path, file))
                posts = posts_tree.getroot()

                # TOPIC preprocessing depending on file is META
                if "meta" in subdir:
                    topic = subdir[:-23]
                    # print(topic)
                else:
                    topic = subdir[:-17]

                # Posts in "Posts.xml" stored in posts_list
                posts_list = [row.attrib for row in posts]

                for post in posts_list:
                    # Text preprocessing
                    post['Body'] = html2markdown.convert(post['Body'])
                    post['Topic'] = topic
                    post['Language'] = 'english'

                    # TEST on Id AND Topic
                    query = collection_Quest_Rep.find({
                        "$and": [{
                            "Id": post["Id"],
                            "Topic": post["Topic"]}]})

                    # After test IF NOT PRESENT
                    # Test post is Answer or Question with Answer
                    # Post INSERTION in Quest_Rep collection
                    if (query.count() == 0) and (
                            (post["PostTypeId"] == '2') or (
                                (post["PostTypeId"] == '1') and
                                (post['AnswerCount'] is not None))):
                        collection_Quest_Rep.insert_one(post)
                        # print("Post", post["_id"], "inserted")

            if file == "my_export_en.json":
                curent_file = os.path.join(current_path, file)
                with open(curent_file) as f:
                    data = json.load(f)
                topic = 'general'
                language = 'english'
                posts, Id, old_Id = add_posts(data,
                                              language,
                                              topic,
                                              Id+1,
                                              old_Id+1)
                collection_Quest_Rep.insert_many(posts)

            if file == "my_export_fr.json":
                curent_file = os.path.join(current_path, file)
                with open(curent_file) as f:
                    data = json.load(f)
                topic = 'general'
                language = 'french'
                posts, Id, old_Id = add_posts(data,
                                              language,
                                              topic,
                                              Id+1,
                                              old_Id+1)
                collection_Quest_Rep.insert_many(posts)

    # INSERTED posts COUNT in DB
    present_posts = collection_Quest_Rep.count_documents({})
    inserted_posts = present_posts - init_present_posts
    print(inserted_posts, "posts have been inserted in", db.name)
    print(present_posts, "posts are stored in", db.name)

    # Create ID index
    db.Quest_Rep.create_index("Id")

    # Create POST_TYPE_ID index
    db.Quest_Rep.create_index("PostTypeId")

    # Create TOPIC index
    db.Quest_Rep.create_index("Topic")

    # Create SCORE index
    db.Quest_Rep.create_index("Score")

    # Create PARENTID index
    db.Quest_Rep.create_index("ParentId")

    # Create ANSWERCOUNT index
    db.Quest_Rep.create_index("AnswerCount")

    # Create TEXT_SEARCH index
    db.Quest_Rep.create_index([('Title', 'text'), ('Body', 'text')],
                              weights={'Title': 2, 'Body': 1},
                              name="text_search")

    # QUEST_REP collection STATISTICS in StarkBotBD
    # db.command("collstats", collection_Quest_Rep)
    # SUGGESTION collection STATISTICS in StarkBotBD
    # db.command("collstats", collection_Suggestion)
    # EMOTION collection STATISTICS in StarkBotBD
    # db.command("collstats", collection_Emotion)
    # RATING collection STATISTICS in StarkBotBD
    # db.command("collstats", collection_Rating)


if __name__ == "__main__":
    create_mongodb_database(data_path, file_name)

