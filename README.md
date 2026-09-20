# ChargeShield

## Sanal POS İşyerleri İçin Erken Risk Uyarı Sistemi

ChargeShield, sanal POS kullanan işletmelerin müşterilerden ödeme aldıktan sonra ürün veya hizmeti sunamaması ve bloke süresi sonunda bankayı chargeback zararıyla karşı karşıya bırakması riskini erken tespit etmeyi amaçlayan yapay zekâ destekli bir prototiptir.

Sistem; müşteri şikâyetlerini, negatif yorum oranlarını, şikâyetlerin zaman içindeki artışını, 7/14/30 günlük şikâyet sinyallerini ve ödeme aktarımına kalan gün bilgisini analiz ederek bankaya inceleme önerisi sunar.

## Proje Takımı

- Eda Vural — Yazılım Mühendisliği
- Ayşe Lermi — Endüstri Mühendisliği
- Alperen Manas — Bilgisayar Mühendisliği

## Klasör Yapısı

deployment_submission/
├── README.md
├── ChargeShield_Deployment_Submission_TR.docx
└── deployment/
    ├── deployment_api.py
    ├── deployment_predict.py
    ├── deployment_feature_engineering.py
    ├── model_artifact.json
    ├── sample_request.json
    ├── deployment_ui.html
    └── README_TR.md

## Çalıştırma

Terminalde deployment klasörüne girin: `cd deployment_submission/deployment`

API’yi başlatın: `python3 deployment_api.py`

İkinci bir terminal açarak arayüzü yayınlayın: `python3 -m http.server 8080`

Tarayıcıdan şu adresi açın: `http://127.0.0.1:8080/deployment_ui.html`

API adresi: `http://127.0.0.1:8000`

## API Endpoint’leri

`GET /health` API durumunu kontrol eder.

`POST /predict` hazır özelliklerle risk tahmini yapar.

`POST /score_complaints` ham şikâyetlerden özellikleri otomatik hesaplar ve risk tahmini üretir.

Örnek istek: `curl -X POST http://127.0.0.1:8000/score_complaints -H "Content-Type: application/json" --data @sample_request.json`

## Önemli Not

Bu sürüm sentetik/prototip verisiyle hazırlanmıştır ve gerçek banka verisi içermez. Sistem otomatik bloke işlemi yapmaz; yalnızca bankaya inceleme önceliği önerir. Gerçek kullanım için banka entegrasyonu, KVKK uyumu, güvenlik kontrolleri ve yetkili personel onayı gereklidir.
