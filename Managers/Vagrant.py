from .InfrastructureManager import InfrastructureManager

class Vagrant(InfrastructureManager):
    def callInfManager(self, config):
        return 0

    def destroy(self):
        return 0