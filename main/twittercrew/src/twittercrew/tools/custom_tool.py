from typing import Type
from crewai_tools import BaseTool
from pydantic import BaseModel, Field


import json

# Tool for Liking Tweets
class LikeTweetTool(BaseTool):
    name: str = "LikeTweetTool"
    description: str = "Likes a tweet by incrementing its like count in the dummy tweets JSON file."

    def _run(self, tweet_id: str, filepath: str) -> str:
        with open(filepath, 'r') as f:
            tweets = json.load(f)

        for tweet in tweets:
            if tweet['tweet_id'] == tweet_id:
                tweet['likes'] += 1  # Increment like count
                print(f"Liked tweet: {tweet['text']}")
                return f"Tweet ID {tweet_id} liked."
        
        return f"Tweet ID {tweet_id} not found."

class FeedScannerTool(BaseTool):
    name: str = "Feed Scanner Tool"
    description: str = "Access and scan dummy_tweets.json for individual tweets to evaluate relevance."

    def _run(self, dummy_tweet_path: str) -> str:
        with open(dummy_tweet_path, 'r') as file:
            tweets = json.load(file)
        for tweet in tweets:
            # Here, you can implement logic to decide relevance
            yield tweet  # Yielding each tweet one by one


# Tool for Replying to Tweets
class ReplyTweetTool(BaseTool):
    name: str = "ReplyTweetTool"
    description: str = "Replies to a tweet by appending the reply to its replies in the dummy tweets JSON file."

    def _run(self, tweet_id: str, reply_text: str, filepath: str) -> str:
        with open(filepath, 'r') as f:
            tweets = json.load(f)

        for tweet in tweets:
            if tweet['tweet_id'] == tweet_id:
                reply = {
                    'reply_id': f"reply_{len(tweet.get('replies', [])) + 1}",
                    'tweet_id': tweet_id,
                    'text': reply_text
                }
                tweet.setdefault('replies', []).append(reply)  # Append reply
                print(f"Replied to tweet: {tweet['text']} with: {reply_text}")
                return f"Replied to Tweet ID {tweet_id}."
        
        return f"Tweet ID {tweet_id} not found."


# Tool for Retweeting Tweets
class RetweetTool(BaseTool):
    name: str = "RetweetTool"
    description: str = "Retweets a tweet by incrementing its retweet count in the dummy tweets JSON file."

    def _run(self, tweet_id: str, filepath: str) -> str:
        with open(filepath, 'r') as f:
            tweets = json.load(f)

        for tweet in tweets:
            if tweet['tweet_id'] == tweet_id:
                tweet['retweets'] += 1  # Increment retweet count
                print(f"Retweeted tweet: {tweet['text']}")
                return f"Tweet ID {tweet_id} retweeted."
        
        return f"Tweet ID {tweet_id} not found."


# Initialize the tools
filepath = "D:\crew_ai_new\dummy_tweets.json"  # Path to the dummy tweets JSON file
like_tool = LikeTweetTool()
reply_tool = ReplyTweetTool()
retweet_tool = RetweetTool()
# search_tool = SerperDevTool()
feedscan_tool = FeedScannerTool()
      
