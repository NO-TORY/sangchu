from requests import get
from pymongo import MongoClient
from bson import ObjectId

class LastVideo:
    database = MongoClient(A STRING MONGO-DB URL)

    def __init__(self, id: str, api_key: str):
        self.id = id
        self.api_key = api_key
        self.old_last_video = self.get_old()
        self.last_video = self.get()

    def get(self):
        channel = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=%s&maxResults=10&order=date&type=video&key=%s"%(self.id, self.api_key)
        lastVideo = get(channel).json()["items"][0]
        return "https://www.youtube.com/watch?v=%s"%lastVideo["id"]["videoId"]

    def update(self):
        return self.database["dddd"]["dddd"].update_one({"_id": ObjectId("61e2df1d5b282eb1e1ee12b0")}, {"$set": {"new_video": self.last_video}})

    def get_old(self):
        return self.database["dddd"]["dddd"].find_one()
