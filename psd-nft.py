# -*-coding:utf-8 -*-
from psd_tools import PSDImage
import PIL.Image as Image
import json
import os
import sys
import random
import math
from multiprocessing.dummy import Pool as ThreadPool, Lock
from tqdm import tqdm

components = {}

pos = {}

config = {}

records = {}

meta_data = {}

ID = 0

pbar = None

lock = Lock()


def layer_info(layer):
    print(f'{"Group" if layer.is_group() else "Element"} {layer.name} size-{layer.size} offset-{layer.offset} opacity-{layer.opacity}')


def go_through(file):
    total_elements = 1
    psd = PSDImage.open(file)
    layer_level = 0

    for layer in psd:
        layer_info(layer)
        if layer.is_group():
            total_elements *= len(layer)

            components[layer.name] = []
            pos[layer.name] = []
            config[layer.name] = []

            id = 0
            for child in layer:
                layer_info(child)

                components[layer.name].append(child.topil())
                pos[layer.name].append(child.offset)
                config[layer.name].append(
                    (child.name, id * (1000//len(layer)), layer_level))
                id += 1
            layer_level += 1
        else:
            print(f"Warning, element not in group: {layer.name} ignored")

    return total_elements, psd.size


def gen_meta(id, project):
    meta = {}
    if id == -1:
        # generate template
        # "name": "Cute Squares #1",
        # "symbol": "CS",
        # "description": "Cutest squares on Solana Network!!",
        # "seller_fee_basis_points": 500,
        # "image": "0.png",
        # "external_url": "YOUR WEBPAGE",
        meta['name'] = project
        meta['symbol'] = "SYM"
        meta['description'] = "Description ..."
        meta['image'] = "URL"
        meta['attributes'] = []

        for feature in components.keys():
            attr = {}
            attr["trait_type"] = feature
            attr["value"] = "TBD"

            meta['attributes'].append(attr)

            # {
            #     "trait_type": "Background",
            #     "value": "Orange"
            # },
        with open(project+'/meta.json', 'w') as f:
            json.dump(meta, f, indent=4, ensure_ascii=False)

    else:  # generate meta file for each PNG
        meta_data['name'] = project + '#' + str(id)
        meta_data['image'] = str(id) + '.png'
        # attributes ameatdata had been changed in gen_image
        with open(project+'/meta/'+str(id)+'.json', 'w') as f:
            json.dump(meta_data, f, indent=4, ensure_ascii=False)
        # restore name value
        meta_data['name'] = project


def gen_image(elements, size):
    image = Image.new('RGBA', size)  # 创建一个新图
    # print(elements)

    for layer in sorted(list(elements.keys())):
        #print(f"{layer=} {elements[layer][0][2]}")
        for element in elements[layer]:
            image.paste(element[0], element[1], element[0])

    return image


def gen_image_combination():
    record = ''
    elements_with_level = {}
    # print(layers)

    for feature in components.keys():
        matrix = random.randint(0, 1000)
        elements = config[feature]
        elements.reverse()
        elements_size = len(elements)

        for i in range(elements_size):
            if matrix >= elements[i][1]:
                id = elements_size-1-i
                record += feature+elements[i][0] + '+'
                #print(f"config {feature} - {elements[i][0]}")

                if components[feature][id] != None:
                    level = elements[i][2]
                    #print(f"{level=} {feature}-{elements[i][0]}")
                    if not level in elements_with_level:
                        #print(f"{level} first time in {elements_with_level}")
                        elements_with_level[level] = []
                    elements_with_level[level].append(
                        [components[feature][id], pos[feature][id], feature+elements[i][0]])

                    # find the trait_type and change the value
                    for j in range(len(meta_data['attributes'])):
                        if meta_data['attributes'][j]['trait_type'] == feature:
                            meta_data['attributes'][j]['value'] = elements[i][0]

                    if j == len(meta_data['attributes']):
                        print(f"Warning {feature} value had not been set")
                break

    return elements_with_level, record


def gen_nft(ID):
    while True:
        elements, record = gen_image_combination()

        if record in records:
            # print(f"{record} had been generated")
            pass
        else:
            image = gen_image(elements, size)
            records[record] = ID
            # image.show()
            image.save(project + '/png/' + str(ID)+'.png')
            meta_data['image'] = str(ID)+'.png'
            gen_meta(ID, project)

            # print(f"[{ID}] {record}")
            pbar.update(1)
            return


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Uage: psd-nft.py [psd file] [number to generate]")
        exit(0)

    print(f"Loading PSD file: {sys.argv[1]}")
    total, size = go_through(sys.argv[1])
    project = sys.argv[1][:-4]  # remove .psd

    # create directories
    if not os.path.exists(project):
        os.mkdir(project)
    if not os.path.exists(project+'/png'):
        os.mkdir(project+'/png')
    if not os.path.exists(project+'/meta'):
        os.mkdir(project+'/meta')

    # create/load config file
    if not os.path.exists(project+'/config.json'):
        with open(project+'/config.json', 'w') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    else:
        with open(project+'/config.json', 'r') as f:
            config = json.load(f)

    # create/load meta template file
    if not os.path.exists(project+'/meta.json'):
        with open(project+'/meta.json', 'w') as f:
            gen_meta(-1, project)  # template metadata file
    else:
        with open(project+'/meta.json', 'r') as f:
            meta_data = json.load(f)

    if os.path.exists(project+'/records.json'):
        with open(project+'/records.json', 'r') as f:
            records = json.load(f)
            ID = list(records.values())[-1]+1

    if len(sys.argv) <= 2:
        print(f"0/{total} elements had be generated")
        exit(0)

    amount = int(sys.argv[2])

    if amount + ID >= total:
        print(
            f"Total {total} elements, {ID} had been generated, no {amount} left")
        exit(0)

    print(
        f"Total {total} elements, {ID} had been generated, {amount} to be peocessed...")

    threadAmount = max(round(math.sqrt(amount)), 4)
    pool = ThreadPool(threadAmount)
    #list(map(gen_nft, list(range(ID, ID+ int(sys.argv[2])))))
    #[*map(gen_nft, list(range(ID, ID+ int(sys.argv[2]))))]

    pbar = tqdm(desc=project, total=amount)

    pool.map(gen_nft, list(range(ID, ID + amount)))
    pool.close()
    pool.join()

    records = dict(sorted(records.items(), key=lambda x: x[1]))
    with open(project+'/records.json', 'w+') as f:
        json.dump(records, f, indent=4, ensure_ascii=False)

    #print(f"Total {total} elements, {len(records)} had been generated, check records.json for details")
