# ChargeShield — Deployment Prototype

ChargeShield, sanal POS kullanan işyerlerinde müşteri şikâyetlerindeki artışı analiz ederek bankaya erken inceleme sinyali üretir. Bu klasör, projenin deployment ödevi için hazırlanmış çalıştırılabilir prototipidir.

> Not: Model artefact’ı sentetik/prototip verisiyle oluşturulmuştur. Gerçek banka verisi değildir ve üretim kararı için kullanılmamalıdır.

## İçerik

- `deployment/deployment_api.py` — HTTP API
- `deployment/deployment_predict.py` — model tahmini
- `deployment/deployment_feature_engineering.py` — ham şikâyetlerden 7/14/30 günlük sinyalleri çıkarır
- `deployment/model_artifact.json` — kayıtlı model katsayıları ve eşik
- `deployment/deployment_ui.html` — yerel demo arayüzü
- `deployment/sample_request.json` — örnek istek
- `ChargeShield_Deployment_Submission_TR.docx` — deployment raporu

## Çalıştırma

Terminal 1:

```bash
cd deployment
python3 deployment_api.py
```

Terminal 2:

```bash
cd deployment
python3 -m http.server 8080
```

Tarayıcıda `http://127.0.0.1:8080/deployment_ui.html` adresini açın. API sağlık kontrolü: `http://127.0.0.1:8000/health`.

## API kullanımı

`POST /predict`, hazır özellikleri ve bankadan gelen `days_to_release` değerini alır. `POST /score_complaints` ise ham şikâyet kayıtlarından özellikleri otomatik hesaplar.

```bash
curl -X POST http://127.0.0.1:8000/score_complaints \
  -H 'Content-Type: application/json' \
  --data @deployment/sample_request.json
```

`days_to_release`, paranın işletmeye aktarılacağı tarihe bankacılık sisteminden kalan gündür; şikâyet verisinden tahmin edilmez. Gerçek sistemde şikâyet akışı düzenli aralıklarla güncellenir ve her güncel kayıt aynı endpoint’e gönderilir.

## Sınırlamalar

Bu sürüm gerçek banka entegrasyonu, kimlik doğrulama, KVKK süreçleri veya otomatik bloke işlemi içermez. Çıktı yalnızca inceleme önceliği önerisidir; nihai karar bankanın yetkili ekiplerine aittir.
