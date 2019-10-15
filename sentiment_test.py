from textblob import TextBlob
pos_count = 0
pos_correct = 0

testBlob = TextBlob("flacko can’t even sing")
print(testBlob.pos_tags)