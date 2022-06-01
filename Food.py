class Food:
    """The Food object that creatures can consume

    Parameters
    ------------
    radius: the polar coordinate r of the Food object
    theta: the polar coordinate theta of the Food object
    theta_lim: how close a Creature needs to be to this Food in order for it to possibly be withing eating range"""
    def __init__(self, radius, theta, theta_lim):
        self.radius = radius
        self.theta = theta
        self.theta_lim = theta_lim
