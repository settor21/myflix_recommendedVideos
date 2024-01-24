from pymongo import MongoClient
from urllib.parse import quote_plus
from datetime import datetime
import pytz

# MongoDB connection details
username = 'amedikusettor'
password = 'Praisehim69%'
escaped_username = quote_plus(username)
escaped_password = quote_plus(password)
mongo_uri = f'mongodb://{escaped_username}:{escaped_password}@35.239.170.49:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.1.1'
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client['recommendationInput']
selected_videos_collection = mongo_db['selectedVideos']

# Function to save recommended videos back to MongoDB


def save_recommended_videos_to_mongo(recommended_videos):
    # Combine all recommendations into a single document
    combined_recommendations = {"recommendations": recommended_videos}

    # Insert the combined recommendations into the 'recommendedVideos' collection
    mongo_db['recommendedVideos'].insert_one(combined_recommendations)

def main():
    try:
        # Get all data from selectedVideos collection
        all_selected_videos = selected_videos_collection.find()

        # Count the frequency of each video_name
        video_name_counts = {}
        for video in all_selected_videos:
            video_name = video['video_name']
            video_name_counts[video_name] = video_name_counts.get(
                video_name, 0) + 1

        # Get the top 5 most clicked videos based on frequency
        top_clicked_videos = sorted(
            video_name_counts.items(), key=lambda x: x[1], reverse=True)[:5]

        # Format the results for insertion into recommendedVideos
        recommended_videos = [
            {"video_name": video_name, "rank": i+1, "frequency": frequency,
                "timestamp": datetime.now(pytz.utc)}
            for i, (video_name, frequency) in enumerate(top_clicked_videos)
        ]

        # Save most clicked videos to MongoDB
        save_recommended_videos_to_mongo(recommended_videos)

        print("Recommendations saved successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
