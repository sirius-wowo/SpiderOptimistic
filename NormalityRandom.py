import random
def normalityRandom(mu=1, sigma=0.4):
    secs = 3 + random.normalvariate(mu, sigma)
    if secs <= 0:
        secs = mu
    return secs