from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import praw
from dotenv import load_dotenv
import os

load_dotenv()
# FastAPI app instance
app = FastAPI()

# Reddit API credentials
client_id = os.getenv("CLIENT_ID")
print(client_id)
client_secret = os.getenv("CLIENT_SECRET")
user_agent = os.getenv("USER_AGENT")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

# Initialize Reddit instance
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)


# Pydantic model for post data
class PostData(BaseModel):
    subreddit_name: str
    title: str
    body: str

# Endpoint to create a post
@app.post("/create_reddit_post/")
def create_post(post_data: PostData):
    try:
        subreddit = reddit.subreddit(post_data.subreddit_name)
        post = subreddit.submit(post_data.title, selftext=post_data.body)
        return {"message": "Post created successfully", "url": post.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Reddit Poster API"}
