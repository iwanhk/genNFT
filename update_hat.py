import json

with open('亿欧会员卡./records.json', 'r') as f:
    records = json.load(f)

for i in range(800):
    hat = list(records.keys())[i].split('+')[-2].replace('帽子', '')

    with open('亿欧会员卡./meta/'+str(i)+'.json', 'r') as f:
        j = json.load(f)
    j['attributes'][-1]['value'] = hat

    with open('meta/'+str(i)+'.json', 'w') as f:
        json.dump(j, f, indent=4, ensure_ascii=False)
