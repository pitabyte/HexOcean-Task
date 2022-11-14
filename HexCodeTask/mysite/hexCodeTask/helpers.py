
def expiresIsValid(expires):
    if (int(expires) >= 30 and int(expires) <= 30000):
        return True
    return False

def getImageURL(baseURL, filename, photo):
    return baseURL + "static/images/user_{0}/{1}".format(photo.user.id, filename)

def convertToThumbnail(photo, height):
    image = Image.open(photo.image.path)
    ratio = image.width / image.height
    MAX_SIZE = (float(height) * ratio, int(height))
    image.thumbnail(MAX_SIZE)
    return image

def getNewPath(photo, height):
    filename = "T" + str(height) + "-" + os.path.basename(photo.image.path)
    dir = os.path.dirname(photo.image.path)
    path = dir + "/" + filename

def extensionIsValid(filename):
    if filename.lower().endswith(('.png', '.jpg')):
        return True
    return False








