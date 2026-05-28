from abc import ABC, abstractmethod
import argparse 
import yaml
import requests

from json import loads


CLOUD_PROVIDERS = ["vultr"]
LOCAL_PROVIDERS = ["vb", "vbox", "virtual box", "virtualbox", "vmware", "vm ware"]

COMMON_REQUIRED_PARAMETERS = ["OGS", "H-IP", "V-IP"]
LOCAL_REQUIRED_PARAMETERS = ["RAM", "DISK", "CPU"]
CLOUD_REQUIRED_PARAMETERS = ["REGION", "VULTR_API_KEY", "VULTR_PLAN_ID"]


class InfrastructureManager(ABC):

    @abstractmethod
    def callInfManager(self, config):
        pass


class OpenTofu(InfrastructureManager):
    def callInfManager(self, config):
        return 0


class Vagrant(InfrastructureManager):
    def callInfManager(self, config):
        return 0


class setupTOPSSIM():
    strategy = None

    def setup(self):
        parser = argparse.ArgumentParser(description="Open5Gs testing environment \
                                                    setup for the TOPSSIM project")

        parser.add_argument("ConfigFile", help="Gives the path to the config file that outlines all of the information necessary to execute the program")
        parser.add_argument("--provider", help="The VM provider that is used (Vultr, VirtualBox, VMWare, QEMU)")
        parser.add_argument("-VultrRegions", action='store_true', help="Shows the available regions for Vultr")
        parser.add_argument("-VultrPlans", action='store_true', help="Shows the available plans for Vultr")
        
        args = parser.parse_args()
        
        config = {}
        try:
            f = open(args.ConfigFile, 'r')
        except FileNotFoundError:
            print(f"Inputted config file was not found: {args.ConfigFile}")
        else:
            with f:
                config = yaml.load(f, Loader=yaml.SafeLoader)
        
        if not args.provider:
            if config["PROVIDER"].lower() in CLOUD_PROVIDERS:
                if "VULTR_API_KEY" not in config.keys():
                    raiseMissingConfig("VULTR_API_KEY")

                if args.VultrRegions:
                    regions = getVultrRegions(config['VULTR_API_KEY'])
                    [print(f"City: {region['city']}, ID: {region['id']}\n") for region in regions]
                    return
                
                if args.VultrRegions:
                    plans = getVultrPlans(config['VULTR_API_KEY'])
                    [print(f"ID: {plan['id']}\n") for plan in plans]
                    return

                for p in CLOUD_REQUIRED_PARAMETERS:
                    if p not in config.keys():
                        raiseMissingConfig(p)

                strategy = OpenTofu()
            elif config["PROVIDER"].lower() in LOCAL_PROVIDERS:
                for p in LOCAL_REQUIRED_PARAMETERS:
                    if p not in config.keys():
                        raiseMissingConfig(p)

                strategy = Vagrant()
            else:
                raise Exception("Provider not recognized. Available providers are: VirtualBox, VMWare and Vultr")

        for p in COMMON_REQUIRED_PARAMETERS:
            if p not in config.keys():
                raiseMissingConfig(p)

        for c in ["HPLMNConfigPath", "VPLMNConfigPath"]:
            if c not in config.keys():
                config[c] = "default"
        
        strategy.callInfManager()


def getVultrPlans(apiKey):
    availVultrPlans = requests.get("https://api.vultr.com/v2/plans", headers={"Authorization": f"Bearer {apiKey}"})

    if availVultrPlans.status_code != 200:
        raise Exception("Error retrieving Vultr plans. Check internet connection or API key.")
    
    jsonVultrPlans = loads(str(availVultrPlans.content)[2:-1])['plans']
    return jsonVultrPlans


def getVultrRegions(apiKey):
    availVultrRegions = requests.get("https://api.vultr.com/v2/regions", headers={"Authorization": f"Bearer {apiKey}"})    
    
    if availVultrRegions.status_code != 200:
        raise Exception("Error retrieving Vultr regions. Check internet connection or API key.")
    
    jsonVultrRegions = loads(str(availVultrRegions.content)[2:-1])['regions']
    return jsonVultrRegions


def raiseMissingConfig(par):
    errorMsg = f"Required paramater not provided: {par}"
    raise Exception(errorMsg)


if __name__ == "__main__":
    setup = setupTOPSSIM()

    setup.setup()