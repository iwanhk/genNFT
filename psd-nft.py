# -*-coding:utf-8 -*- 
from psd_tools import PSDImage
import PIL.Image as Image
import json, os, sys
import random

components={}

pos={}

rarity={}

records={}

meta_data={}

ID=0

def layer_info(layer):
    print(f'{"Group" if layer.is_group() else "Element"} {layer.name} size-{layer.size} offset-{layer.offset} opacity-{layer.opacity}')

def go_through(file):
    total_elements=1
    psd = PSDImage.open(file)
    
    for layer in psd:
        layer_info(layer)
        if layer.is_group():
            total_elements*= len(layer)

            components[layer.name]=[]
            pos[layer.name]=[]
            rarity[layer.name]=[]

            id=0
            for child in layer:
                layer_info(child)

                components[layer.name].append(child.topil())
                pos[layer.name].append(child.offset)
                rarity[layer.name].append((child.name, id* (100//len(layer))))
                id+=1
        else:
            print(f"Warning, element not in group: {layer.name} ignored")

    return total_elements, psd.size

def gen_meta(id, project):
    meta={}
    if id==-1:
        # generate template
        # "name": "Cute Squares #1",
        # "symbol": "CS",
        # "description": "Cutest squares on Solana Network!!",
        # "seller_fee_basis_points": 500,
        # "image": "0.png",
        # "external_url": "YOUR WEBPAGE",
        meta['name']=project
        meta['symbol']="SYM"
        meta['description']="Description ..."
        meta['image']="URL"
        meta['attributes']=[]

        for feature in components.keys():
            attr={}
            attr["trait_type"]= feature
            attr["value"]= "TBD"

            meta['attributes'].append(attr)            

            # {
            #     "trait_type": "Background",
            #     "value": "Orange"
            # },
        with open(project+'/meta.json', 'w') as f:
            json.dump(meta, f, indent=4, ensure_ascii=False)
        
    else: # generate meta file for each PNG
        meta= meta_data
        meta['name']+= '#'+ str(id)
        meta['image']= str(id)+ '.png'
        # attributes ameatdata had been changed in gen_image
        with open(project+'/meta/'+str(id)+'.json', 'w') as f:
            json.dump(meta, f, indent=4, ensure_ascii=False)
        # restore name value
        meta['name']= meta['name'][:-(len(str(id))+1)]



def gen_image(size):
    image= Image.new('RGBA', size) #创建一个新图
    record= ''

    for feature in components.keys():
        matrix= random.randint(0, 100)
        elements= rarity[feature]
        elements.reverse()
        elements_size= len(elements)

        for i in range(elements_size):
            if matrix >= elements[i][1]:
                id= elements_size-1-i
                record+= elements[i][0]+ '+'
                print(f"Rarity {feature} - {elements[i][0]}")
                if components[feature][id]!= None:
                    image.paste(components[feature][id], pos[feature][id], components[feature][id])

                    # find the trait_type and change the value
                    for j in range(len(meta_data['attributes'])):
                        if meta_data['attributes'][j]['trait_type']== feature:
                            meta_data['attributes'][j]['value']= elements[i][0]

                    if j== len(meta_data['attributes']):
                        print(f"Warning {feature} value had not been set")
                break

    return image, record

if __name__ =="__main__":
    if len(sys.argv)<=1:
        print("Uage: psd-nft.py [psd file] [number to generate]")
        exit(0)

    total, size = go_through(sys.argv[1])
    project= sys.argv[1][:-4] # remove .psd

    # create directories
    if not os.path.exists(project):
        os.mkdir(project)
    if not os.path.exists(project+'/png'):
        os.mkdir(project+'/png')
    if not os.path.exists(project+'/meta'):
        os.mkdir(project+'/meta')  


    # create/load rarity file
    if not os.path.exists(project+'/rarity.json'):
        with open(project+'/rarity.json', 'w') as f:
            json.dump(rarity, f, indent=4, ensure_ascii=False)
    else:
        with open(project+'/rarity.json', 'r') as f:
            rarity= json.load(f)
    # print(rarity)

    # create/load meta template file
    if not os.path.exists(project+'/meta.json'):
        with open(project+'/meta.json', 'w') as f:
            gen_meta(-1, project) # template metadata file
    else:
        with open(project+'/meta.json', 'r') as f:
            meta_data= json.load(f)

    if os.path.exists(project+'/records.json'):
        with open(project+'/records.json', 'r') as f:
            records= json.load(f)
            ID= len(records)

    print(f"Total {total} elements can be generated")

    if len(sys.argv)<=2:
        exit(0)

    i=0
    while i < int(sys.argv[2]):
        image, record = gen_image(size)

        if record in records:
            print(f"{record} had been generated")
        else:
            records[record]=ID
            #image.show()
            image.save(project+ '/png/'+ str(ID)+'.png')
            meta_data['image']=str(ID)+'.png'
            gen_meta(ID, project)

            print(f"[{i}/{ID}] {record}")
            i+=1
            ID+=1

    with open(project+'/records.json', 'w+') as f:
        json.dump(records, f, indent=4, ensure_ascii=False)