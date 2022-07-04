Usage:

Step1:
python3 psd-nft.py [psd file] 
this will:
create dir of project and [png] and [meta] dir 
generate the rarity.json and meta.json file 

Step2:
Edit rarity.json to change the ratio of each DNA feature
Edit meta.json to set the name and description as the meta data template

Step3:
python3 psd-nft.py [psd file] [number to generate]
generate png files and meta files
generate records.json file to record the files generated

Step4:
Upload the [png] dir with png files to ipfs
Get the ipfs path and edit ipfs.json file to save the path

Step5:
update_ipfs.py [project] [project] ...
Go through all the metadata files in [project/meta] dir and update them with ipfs path

ipfs://bafybeidhtpoveijwhbap52l3f5dgglihsxrthg4ah4z26prcutyn6frla4
https://nftstorage.link/ipfs/bafybeidhtpoveijwhbap52l3f5dgglihsxrthg4ah4z26prcutyn6frla4
bafybeidhtpoveijwhbap52l3f5dgglihsxrthg4ah4z26prcutyn6frla4


https://nftstorage.link/ipfs/bafybeicnnewm2jibaenborp44zn6uuvenxw4ioplbb5q6ujoqhzldo4wae/
ipfs://bafybeicnnewm2jibaenborp44zn6uuvenxw4ioplbb5q6ujoqhzldo4wae
bafybeicnnewm2jibaenborp44zn6uuvenxw4ioplbb5q6ujoqhzldo4wae