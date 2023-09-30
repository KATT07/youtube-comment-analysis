from googleapiclient.discovery import build
import csv

api_key = "Enter Your OWN API KEY"

csv_lst=[]

def video_comments(video_id):
    replies = []
    youtube = build("youtube", "v3", developerKey=api_key)
    video_response = (
        youtube.commentThreads()
        .list(part="snippet,replies", videoId=video_id)
        .execute()
    )

    # iterate video response
    while video_response:
        for item in video_response["items"]:

            #The primary comment
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            
            #Replies to the comment
            replycount = item["snippet"]["totalReplyCount"]
            if replycount > 0:
                for reply in item["replies"]["comments"]:
                    reply = reply["snippet"]["textDisplay"]
                    replies.append(reply)

            # print comment with list of reply
            print(comment, replies, end="\n\n")

            csv_lst.append(comment)
            for xyz in replies:
                csv_lst.append(xyz)

            replies = []

        # Again repeat
        if "nextPageToken" in video_response:
            video_response = (
                youtube.commentThreads()
                .list(
                    part="snippet,replies",
                    videoId=video_id,
                    pageToken=video_response["nextPageToken"],
                )
                .execute()
            )
        else:
            break

def writetocsv(lst):
    f=open("script_export.csv","w",encoding="utf-8")
    writer = csv.writer(f)
    l=[]
    for i in lst:
        l.append(i)
        writer.writerow(l)
        l=[]

# Enter video id
video_id = input("Enter video id:")
# Call functions
video_comments(video_id)
writetocsv(csv_lst)
print(csv_lst)
