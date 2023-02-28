import requests

# function to get image path
def randomimage() -> str:
    # get image from random image api
    response = requests.get("https://cataas.com/cat?type=sq")
    # save image to /tmp
    if response.status_code != 200:
        print(response.text)
        exit(1)
    with open("/tmp/cat.jpg", "wb") as f:
        f.write(response.content)
    # return image path
    return "/tmp/cat.jpg"