import json,zipfile
from fractions import Fraction
with zipfile.ZipFile('sources/published_certificates.zip') as z:
 for name in ['c_4.json','c_5.json']:
  data=json.load(z.open('certificates/'+name));b=Fraction(data['bound']);print(name,'bound',str(b),'value',float(b),'n',data['order_of_admissible_graphs'],'types',data['number_of_types'],flush=True)
