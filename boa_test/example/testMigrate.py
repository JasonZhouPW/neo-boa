from boa.interop.Ontology.Contract import Migrate
from boa.interop.Ontology.Contract import Destroy
from boa.interop.System.Runtime import Notify

value = "123"
name = "testNmae"
def Main(operation, args):
    if operation == "DestroyContract":
        return DestroyContract()
    if operation == "MigrateContract":
        code = args[0]
        return MigrateContract(code)
    if operation == "Value":
        return Value()
    if operation == "Name":
        return Name()
    return False

def Name():
    Notify(["Name"])
    return name

def Value():
    Notify(["Value"])
    return value

def DestroyContract():
    Destroy()
    Notify(["Destory"])
    return True


def MigrateContract(code):
    Migrate(code, "", "", "", "", "", "", "", "")
    Notify(["Migrate"])
    return True