Usage:

Step1:
python3 psd-nft.py [psd file] 
this will:
create dir of project and [png] and [meta] dir 
generate the rarity.json file 

Step2:
Edit rarity.json to change the ratio of each DNA feature

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