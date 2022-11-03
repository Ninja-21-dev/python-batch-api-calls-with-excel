import os
import time
import pandas as pd
import datetime
import json
import openpyxl
from concurrent.futures import ThreadPoolExecutor, as_completed
from api import connect_api, connect_api_capsule


PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
excel_file_name = PROJECT_PATH + '/' + 'input.xlsx'
excel_output_file_name = PROJECT_PATH + '/' + 'output.xlsx'
max_multi_thread_count = 100


start_time = time.time()

try:
    input_data = pd.read_excel(excel_file_name, index_col=0, engine="openpyxl")
    input_df = pd.DataFrame(input_data)
except Exception as inst:
    print('Reading error!')
    print(inst)
    print('\n')

end_time_1 = time.time()
print("Reading Time:")
print(end_time_1 - start_time)


request_datetime = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
frame_data_array = []
threads= []

with ThreadPoolExecutor(max_workers=max_multi_thread_count) as executor:
    for i in range(0, len(input_df.index)):
        plain_param = "[{\"ProshipRequest\":{\"RequestDate\":\"" + request_datetime + "\",\"Channel\":\"ECOM\",\"ServiceRequestType\":\"Rate Shop\",\"ShipperReference\":\"Order number 1\"},\"ShipmentDetails\":{\"SurchargeFlagStoreNumber\":\"00500\",\"Address1\":\"404 E Front St\",\"Address2\":\"APT 104H\",\"City\":\"Battle Mountain\",\"Code\":\"NV\",\"Company\":\"Royal Hardware\",\"Contact\":null,\"Country\":\"US\",\"Phone\":\"7756352422\",\"PostalCode\":\"89820\",\"Reference\":\"420590000041\",\"ResidentialFlag\":false,\"DeliveryFlag\":false,\"DeclaredValueAmt\":23.7,\"HoldAtLocation\":false,\"InsideDelivery\":false,\"Proof\":false,\"ProofRequireSignature\":false,\"ProofRequireSignatureAdult\":false,\"SignatureRelease\":false,\"Refrigerated\":false,\"Shipper\":\"WI01\",\"ItemList\":[{\"SKU\":\"" + str(input_df.iloc[i].name) + "\",\"Quantity\":" + str(input_df.iloc[i].QTY) +" }]}}]"
        threads.append(executor.submit(connect_api_capsule, plain_param, input_df.iloc[i].name, input_df.iloc[i].QTY ))
    for task in as_completed(threads):
        try:
            mock_response=task.result()["data"]
            api_response = []
            if mock_response != "":
                api_response = json.loads(mock_response)

            api_param_array=[]
            api_param_array.append(task.result()["sku"])
            api_param_array.append(task.result()["qty"])
            for j in range(3):
                if j < len(api_response):
                    if "Price" in json.dumps(api_response[j]):
                        api_param_array.append(api_response[j]["Price"])
                    else:
                        api_param_array.append("")
                else:
                    api_param_array.append("")
            frame_data_array.append(api_param_array)
        except Exception as inst:
            print('Building data and interacting APIs error!!!')
            print(inst)
            print('\n')

end_time_2 = time.time()   
print("API Response Time:")
print(end_time_2 - end_time_1)

try:
    output_df = pd.DataFrame(frame_data_array,  columns=['SKU', 'QTY', 'Standard Shipping', 'Two-Day Shipping', 'Express Shipping'])
    output_df.to_excel(excel_output_file_name, index=False)
except Exception as inst:
    print('Building data and interacting APIs error')
    print(inst)
    print('\n')

end_time = time.time()
print(end_time-start_time)

print("Reading Time:")
print(end_time_1 - start_time)

print("API Response Time:")
print(end_time_2 - end_time_1)


print("Writing Time:")
print(end_time - end_time_2)

print("Total Time:")
print(end_time - start_time)


