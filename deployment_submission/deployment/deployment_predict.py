from pathlib import Path
import json, math
import numpy as np

ROOT=Path('/Users/edavural/Desktop/scapstone/new_version/deployment')
ART=json.loads((ROOT/'model_artifact.json').read_text())
def predict(payload):
 missing=[f for f in ART['features'] if f not in payload]
 if missing: raise ValueError('Eksik özellikler: '+', '.join(missing))
 x=np.array([(float(payload[f])-ART['mean'][f])/ART['std'][f] for f in ART['features']],dtype=float)
 z=float(np.dot(x,np.array(ART['weights']))+ART['bias'])
 probability=1/(1+math.exp(-max(-35,min(35,z))))
 threshold=ART['threshold']
 level='high' if probability>=threshold else ('medium' if probability>=ART['risk_levels']['low_max'] else 'low')
 recommendation='manual_review' if level=='high' else ('monitor' if level=='medium' else 'no_action')
 days=payload.get('days_to_release')
 if days is None:
  urgency='unknown'; urgency_note='Hakediş tarihi verilmedi; yalnızca şikâyet riski hesaplandı.'
 else:
  days=float(days); urgency='urgent' if days<=7 else ('high' if days<=14 else 'standard')
  urgency_note=f'Hakedişe {days:g} gün kaldı.'
  if urgency=='urgent' and probability>=0.40: recommendation='urgent_manual_review'
 return {'risk_probability':round(probability,6),'threshold':threshold,'risk_level':level,'days_to_release':payload.get('days_to_release'),'urgency':urgency,'urgency_note':urgency_note,'recommendation':recommendation,'model_version':ART['artifact_version']}

if __name__=='__main__':
 sample={f:0 for f in ART['features']}; sample.update({'complaint_count_7d':8,'complaint_count_30d':15,'negative_review_ratio_14d':.72,'negative_review_ratio_30d':.68,'text_available_ratio_7d':.90,'text_available_ratio_14d':.88,'complaint_acceleration_7_vs_30':2.4})
 print(json.dumps(predict(sample),ensure_ascii=False,indent=2))
