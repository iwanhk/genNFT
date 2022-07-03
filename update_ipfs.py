import json, os, sys

ipfs={}

def update(project):
    for file in os.listdir(project+'/meta'):
        if file.endswith(".json"):
            meta_data={}
            with open(project+'/meta/'+file, 'r') as f:
                meta_data= json.load(f)
                meta_data['image']= ipfs[project]+'/png/'+file[:-5]+'.png'
            with open(project+'/meta/'+file, 'w') as f:
                json.dump(meta_data, f, indent=4, ensure_ascii=False)


if __name__ =="__main__":
    if len(sys.argv)<=1:
        print("Uage: update_ipfs.py [project] [project] ...")
        exit(0)

    if os.path.exists('ipfs.json'):
        with open('ipfs.json', 'r') as f:
            ipfs= json.load(f)
    else:
        print("ipfs.json not found, exit")
        exit(-1)

    for project in sys.argv[1:]:
        if len(ipfs)==0 or not project in ipfs:
            print(f"ipfs.json not set for {project}")
        else:
            update(project)