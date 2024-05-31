import csv

# Read the content of the text file with UTF-8 encoding
with open("C:/Users/86137/Desktop/new/ChainStream/ChainStreamOJ/test_data/daily_dialog/ijcnlp_dailydialog/dialogues_text.txt", "r", encoding="utf-8") as file:
    data = file.read()

# Replace "__eou__" with "--" and split the data into individual conversations based on the newline character
data = data.replace("__eou__", "--")
conversations = data.split("\n")

# Output the conversations into a CSV file
output_file = "C:/Users/86137/Desktop/new/ChainStream/ChainStreamOJ/test_data/daily_dialog/ijcnlp_dailydialog/conversations.csv"
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Conversation Number", "Conversation"])
    for i, conversation in enumerate(conversations, start=1):
        writer.writerow([i, conversation.strip()])  # Strip whitespace
