# ChargeShield Deployment Prototipi

## Çalıştırma

Terminal 1:

```bash
cd /Users/edavural/Desktop/scapstone/new_version
python3 deployment_artifacts.py
cd deployment
python3 deployment_api.py
```

Terminal 2:

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/predict -H 'Content-Type: application/json' -d @sample_request.json
```

Arayüz için `deployment_ui.html` dosyasını tarayıcıda açın. API açıkken formu doldurup **Tahmin Et** düğmesine basın. Tarayıcı güvenliği nedeniyle dosya doğrudan açılırken istek engellenirse aynı klasörde `python3 -m http.server 8080` çalıştırıp `http://127.0.0.1:8080/deployment_ui.html` adresini açın.

## API

- `GET /health`: servis ve model sürümü kontrolü
- `POST /predict`: önceden hesaplanmış yedi proaktif özelliği ve bankadan gelen `days_to_release` bilgisini alır; risk olasılığı, risk seviyesi, aciliyet ve öneri döndürür.
- `POST /score_complaints`: ham merchant şikâyetlerini, observation_date ve `days_to_release` bilgisini alır; 7/14/30 günlük özellikleri otomatik hesaplayıp model tahmini ve hakediş aciliyeti döndürür.

Model gerçek banka sistemine bağlanmamıştır. Deneme arayüzündeki manuel alanlar, gerçek veri kaynağı olmadığı için kullanılır. Gerçek sistemde `days_to_release` bankanın hakediş/release kaydından gelir; sistem bunu şikâyetlerden tahmin etmez. `score_complaints` endpoint'i ham şikâyet listesinden özellikleri otomatik hesaplar, `days_to_release` ile aciliyeti ayrıca belirler. 7 gün sınırı modelin bekleme süresi değil, prototipteki operasyonel öncelik kuralıdır ve banka politikasıyla kalibre edilmelidir. Artifact JSON; model ağırlıklarını, bias değerini, eğitim standardizasyonunu, özellik listesini ve validation eşiğini birlikte taşır.

## Güvenlik ve izleme

Bu lokal PoC'de kimlik doğrulama yoktur. Gerçek deploymentta API gateway, mTLS/TLS, OAuth2/JWT, rol tabanlı yetkilendirme, KVKK uyumlu maskeleme ve hassas verileri loglamama uygulanmalıdır. İzlenecek metrikler risk alarm oranı, precision/recall, veri drift'i, kalibrasyon, yanıt süresi ve API hata oranıdır.
