from subprocess import run
from json import loads

from .InfrastructureManager import InfrastructureManager

VARS_PATH = "vultr-opentofu/terraform.tfvars"
REQ_VARS = ["ANSIBLE_SSH_KEY", "VULTR_API_KEY", "VULTR_PLAN_ID", "H-REGION", "VPC-REGION", "V-REGION", "USER_SSH_KEY"]
SEPARATOR = ' '+'='*5+' '


class OpenTofu(InfrastructureManager):
    def callInfManager(self, config):
        self.populateVars(config)

        self.runCommand(["tofu", "-chdir=vultr-opentofu", "init"])
        self.runCommand(["tofu", "-chdir=vultr-opentofu", "apply", "-show-sensitive", "-json-into=tofu_out.json"])
        
        # self.runCommand(["tofu", "-chdir=vultr-opentofu", "show", "-show-sensitive", "-json-into=tofu-apply.json"])

        print("\n\nSuccesfully create HPLMN and VPLMN machines!\n\n")

        with open("vultr-opentofu/tofu_out.json") as f:
            outFile = f.read()
            
            print("Reading OpenTofu outputs...")
            # only parse last line where outputs are stores
            outJson = loads(outFile.split("\n")[-2])

            config["HPLMN_PUBLIC_IP"] = outJson["outputs"]["hplm_ip"]["value"]
            config["VPLMN_PUBLIC_IP"] = outJson["outputs"]["vplm_ip"]["value"]

            print("\n\n OpenTofu completed succesfully!")
            
            


    def populateVars(self, config):
        print("Populating OpenTofu Vars...")

        with open(VARS_PATH, 'w') as f:
            for var in REQ_VARS:
                val = config[var]
                var = var.replace('-', '_')
                f.write(f'{var} = "{val}"\n')
            f.write('H_HOSTNAME = "HPLMNTEST"\n')
            f.write('V_HOSTNAME = "VPLMNTEST"\n')

        print("Vars created successfully!")


    def runCommand(self, command, input=None):
        if len(command) > 2:
            commandName = f"{command[0]} {command[2]}"
        else:
            commandName = command[0]
        
        print("\n"+SEPARATOR+f"Running: {commandName}"+SEPARATOR+"\n\n")
        res = run(command, input=input)

        if(res.returncode != 0):
            print(f"Command ({commandName}) presented an error [Status code: {res.returncode}]")
            return 
        else:
            print(f"Command ({commandName}) was succesful")
            
