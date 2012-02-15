import json, ucsv as csv, requests

endpoint = 'http://openspending.org/api/2/aggregate'
dataset = 'de-bund'
drilldown = 'einzelplan'
year_dim = 'data_year'

def load():
	req = requests.get(endpoint+'?dataset='+dataset+'&drilldown='+year_dim+'|'+drilldown)
	if req.status_code != 200:
		return False
	data = json.loads(req.text)
	years = set()
	by_id = {}
	meta = {}
	for e in data['drilldown']:
		amt = e['amount']
		dd = e[drilldown]
		dd_id = dd['id']
		if dd_id not in meta:
			meta[dd_id] = { 'label': dd['label'], 'color': dd['color'] }
			by_id[dd_id] = {}
		yr = e[year_dim]
		years.add(yr)
		if yr not in by_id[dd_id]:
			by_id[dd_id][yr] = amt
		else:
			print 'warning: duplicate cell', dd_id, yr
	years = sorted(years)
	mv = 0
	head = ['id','label','color'] + years
	out = csv.writer(open('result.csv','w'))
	out.writerow(head)
	for dd_id in by_id:
		row = [dd_id, meta[dd_id]['label'], meta[dd_id]['color']]
		for yr in years:
			if yr in by_id[dd_id]:
				row.append(by_id[dd_id][yr])
			else:
				row.append('-')
				mv += 1
		out.writerow(row)

load()
