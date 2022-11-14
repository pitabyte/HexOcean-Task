

def expiresIsValid(expires):
    if (int(expires) >= 30 and int(expires) <= 30000):
        return True
    return False

def getImageURL(baseURL, filename, photo):
    return baseURL + "static/images/user_{0}/{1}".format(photo.user.id, filename)








