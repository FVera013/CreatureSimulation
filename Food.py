class Food:
    """The Food object that creatures can consume

    Static Parameters
    ------------

    Instance Parameters
    ------------
    radius: the polar coordinate r of the Food object
    \b
    theta: the polar coordinate theta of the Food object
    \b
    map: The associated map class (must be an instance of Map in order to work properly)"""

    def __init__(self, radius, theta, theta_lim):
        self.radius = radius
        self.theta = theta
        self.theta_lim = theta_lim
        self.map = None
