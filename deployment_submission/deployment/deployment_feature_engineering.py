from datetime import datetime

def complaint_features(complaints, observation_date):
    obs=datetime.fromisoformat(observation_date).date(); rows=[]
    for c in complaints:
        try: date=datetime.fromisoformat(str(c['complaint_date'])[:10]).date()
        except Exception: continue
        if date <= obs: rows.append((date,c))
    def window(days):
        selected=[c for date,c in rows if (obs-date).days < days]
        n=len(selected); neg=sum(float(c.get('customer_rating',5) or 5)<=2 for c in selected); text=sum(bool(str(c.get('complaint_text','')).strip()) for c in selected)
        return n, neg/n if n else 0.0, text/n if n else 0.0
    n7,neg7,text7=window(7); n14,neg14,text14=window(14); n30,neg30,text30=window(30)
    return {'complaint_count_7d':n7,'complaint_count_30d':n30,'negative_review_ratio_14d':round(neg14,6),'negative_review_ratio_30d':round(neg30,6),'text_available_ratio_7d':round(text7,6),'text_available_ratio_14d':round(text14,6),'complaint_acceleration_7_vs_30':round((n7*30/(n30*7)) if n30 else 0.0,6)}
