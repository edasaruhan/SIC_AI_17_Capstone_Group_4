from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from deployment_predict import predict
from deployment_feature_engineering import complaint_features

class Handler(BaseHTTPRequestHandler):
 def reply(self,status,body):
  raw=json.dumps(body,ensure_ascii=False).encode('utf-8'); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Content-Length',str(len(raw))); self.send_header('Access-Control-Allow-Origin','*'); self.send_header('Access-Control-Allow-Headers','Content-Type'); self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS'); self.end_headers(); self.wfile.write(raw)
 def do_OPTIONS(self):
  self.send_response(204); self.send_header('Access-Control-Allow-Origin','*'); self.send_header('Access-Control-Allow-Headers','Content-Type'); self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS'); self.end_headers()
 def do_GET(self):
  if self.path=='/health': self.reply(200,{'status':'ok','service':'ChargeShield','model_version':'chargeshield-logistic-v3'})
  elif self.path=='/': self.reply(200,{'service':'ChargeShield API','endpoints':['GET /health','POST /predict']})
  else: self.reply(404,{'error':'endpoint_not_found'})
 def do_POST(self):
  if self.path not in ['/predict','/score_complaints']: self.reply(404,{'error':'endpoint_not_found'}); return
  try:
   n=int(self.headers.get('Content-Length','0')); payload=json.loads(self.rfile.read(n).decode('utf-8'))
   if self.path=='/score_complaints':
    features=complaint_features(payload.get('complaints',[]),payload['observation_date']); features['days_to_release']=payload.get('days_to_release'); result=predict(features); result['features']=features; self.reply(200,result); return
   self.reply(200,predict(payload))
  except Exception as e: self.reply(400,{'error':'invalid_request','detail':str(e)})
 def log_message(self,fmt,*args): print('[api]',fmt%args)

if __name__=='__main__':
 print('ChargeShield API: http://127.0.0.1:8000'); HTTPServer(('127.0.0.1',8000),Handler).serve_forever()
