import openai
import time

test_number = 10
try:
    openai.FileSet(f"chris_test{test_number}").delete()
except:
    pass


# Creation
openai.FileSet.create(
    name=f"chris_test{test_number}", file_ids=["file-x6c4dy5ULysgpu1PJCIudyeX"]
)

# List
openai.FileSet.list()

# GET
openai.FileSet.retrieve(f"chris_test{test_number}")

# Deletion
openai.FileSet.retrieve(f"chris_test{test_number}").delete()

# Delete the other way
openai.FileSet.create(name=f"chris_test{test_number}")
# print("waiting")

# time.sleep(5)
openai.FileSet(f"chris_test{test_number}").delete()
