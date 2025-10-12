from client_sdk.methods import LicenseKey, Helpers, HelperMethods
# from licensing.methods import Key, Helpers, HelperMethods

RSAPubKey = ""
authKey = ""
productId = 0
licenseKey = ""

result = LicenseKey.activate(
    token=authKey,
    rsa_pub_key=RSAPubKey,
    product_id=productId,
    key=licenseKey,
    machine_code=Helpers.GetMachineCode(),
)

if result[0] == None or not Helpers.IsOnRightMachine(result[0]):
    print(f"The liscense does not work: {result[1]}")
else:
    print("lisense active")
