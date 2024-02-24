from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
import hashlib

app = Flask(__name__)

# MongoDB konfigürasyonu
app.config["MONGO_URI"] = "mongodb://localhost:27017/anketUygulamasi"
mongo = PyMongo(app)

sorular_ve_cevaplar = [
    {
        'soru': 'Soru 1',
        'metin': 'Aşağıdaki şıklardan hangisi fillna() metodunu ifade eder?',
        'secenekler': {
            'A': 'Fillna metodu, bir DataFramedeki eksik (NaN) değerleri belirli bir değerle doldurmak için kullanılır.',
            'B': 'Fillna, bir veri setindeki tüm değerleri belirli bir değerle değiştirmek için kullanılır.',
            'C': 'Fillna fonksiyonu, bir veri çerçevesindeki tüm sütunlardaki değerleri toplar ve toplam değeri döndürür.',
            'D': 'Fillna() fonksiyonu, veri setindeki sayısal değerleri rasgele seçilmiş başka bir değerle değiştirmek için kullanılır.'
        },
        'dogru_cevap': 'A'
    },
    {
        'soru': 'Soru 2',
        'metin': 'Aşağıdaki şıklardan hangisi melt() metodunu ifade eder?',
        'secenekler': {
            'A': 'Melt metodu, bir DataFrame i diğerine dönüştürmek için kullanılır',
            'B': 'Melt, geniş formatlı veriyi uzun formata çevirmek için kullanılan bir işlemdir.',
            'C': 'Pandas melt fonksiyonu, veri setini yeniden düzenlemek ve sütunları satırlara dönüştürmek için kullanılır.',
            'D': 'Melt() fonksiyonu, genellikle veri analizi ve görselleştirmelerinde kullanılan bir veri dönüştürme işlemidir.'
        },
        'dogru_cevap': 'B'
    },
    {
        'soru': 'Soru 3',
        'metin': 'Pandas kütüphanesinde bir dosyayı okuma işlemi nasıl gerçekleştirilir?',
        'secenekler': {
            'A': 'pd.open_file(dosya.csv) komutu kullanılarak dosya okuma işlemi gerçekleştirilir.',
            'B': 'pd.read_csv(dosya.csv) fonksiyonu kullanılarak dosya okuma işlemi gerçekleştirilir.',
            'C': 'open(dosya.csv) komutu ile dosya açılıp, ardından pd.read() fonksiyonu ile okuma işlemi yapılır.',
            'D': 'pandas.read_file(dosya.csv) fonksiyonu kullanılarak dosya okuma işlemi gerçekleştirilir.'
        },
        'dogru_cevap': 'B'
    },
    {
        'soru': 'Soru 4',
        'metin': 'Makine öğrenimi nedir?',
        'secenekler': {
            'A': 'Yapay zeka ile ilgili bir programlama dilidir.',
            'B': 'Bilgisayarların öğrenme yeteneğini geliştiren bir alanı ifade eder.',
            'C': 'Bilgisayar donanımının bir türüdür.',
            'D': 'Bir matematik teoremi türüdür.'
        },
        'dogru_cevap': 'B'
    },
    {
        'soru': 'Soru 5',
        'metin': 'Hangi aşama, bir makine öğrenimi modelinin performansını ölçmek için kullanılır?',
        'secenekler': {
            'A': 'Eğitim',
            'B': 'Doğrulama',
            'C': 'Tahmin',
            'D': 'Test'
        },
        'dogru_cevap': 'D'
    },
    {
        'soru': 'Soru 6',
        'metin': '"Denetimli öğrenme" nedir?',
        'secenekler': {
            'A': 'Veri kümesinin etiketlenmiş örnekleri kullanılarak modelin eğitildiği bir öğrenme yöntemidir.',
            'B': 'Modelin tamamen kendiliğinden öğrenmesini sağlayan bir öğrenme yöntemidir.',
            'C': 'İnsanların öğrenme süreçlerini modelleyen bir öğrenme yöntemidir.',
            'D': 'Veri kümesindeki boşlukları doldurarak öğrenilen bir yöntemdir.'
        },
        'dogru_cevap': 'A'
    },
    {
        'soru': 'Soru 7',
        'metin': 'Hangisi regresyon analizi için kullanılan bir makine öğrenimi algoritmasıdır?',
        'secenekler': {
            'A': 'K-Means',
            'B': 'Decision Tree',
            'C': 'Linear Regression',
            'D': 'Naive Bayes'
        },
        'dogru_cevap': 'C'
    },
    {
        'soru': 'Soru 8',
        'metin': '"Overfitting" nedir?',
        'secenekler': {
            'A': 'Modelin eğitim verilerine aşırı derecede uyum sağlaması durumudur.',
            'B': 'Modelin eğitim verilerini ihmal etmesi durumudur.',
            'C': 'Modelin eğitim sürecini hızlandıran bir tekniktir.',
            'D': 'Modelin öğrenme yeteneğini kaybetmesi durumudur.'
        },
        'dogru_cevap': 'A'
    },
    {
        'soru': 'Soru 9',
        'metin': 'Hangisi "unsupervised learning" için bir örnektir?',
        'secenekler': {
            'A': 'Spam filtresi oluşturma',
            'B': 'Haber başlıklarını kategorize etme',
            'C': 'El yazısı sayıları tanıma',
            'D': 'Film önerileri yapma'
        },
        'dogru_cevap': 'C'
    },
    {
        'soru': 'Soru 10',
        'metin': 'Hangisi "convolutional neural network (CNN)" ile ilgili doğrudur?',
       'secenekler': {
            'A': 'Ses verilerini işlemek için kullanılır.',
            'B': 'Seri veriler üzerinde etkilidir, örneğin metin analizi için kullanılır.',
            'C': 'Görüntü verilerinde lokal özellikleri vurgulamak için tasarlanmıştır.',
            'D': 'Yapay sinir ağlarının eğitim sürecini hızlandırmak için kullanılır.'
        },
        'dogru_cevap': 'C'
    }
]
@app.route('/', methods=['GET', 'POST'])
def index():
    hata_mesaji = None
    if request.method == 'POST':
        kullanici_adi = request.form.get('kullanici_adi')
        sifre = request.form.get('sifre')
        # Güvenlik için şifreyi hash'leyin
        hashed_sifre = hashlib.sha256(sifre.encode()).hexdigest()

        # Kullanıcı zaten var mı kontrol et
        kullanici_var_mi = mongo.db.kullanicilar.find_one({'kullanici_adi': kullanici_adi})
        if kullanici_var_mi:
            hata_mesaji = 'Bu kullanıcı adıyla daha önce giriş yapılmış.'
        else:
            # Kullanıcıyı kaydet
            mongo.db.kullanicilar.insert_one({'kullanici_adi': kullanici_adi, 'sifre': hashed_sifre})
            # Anket sayfasına yönlendir
            return redirect(url_for('anket', kullanici_id=kullanici_adi))

    return render_template('index.html', hata=hata_mesaji)


@app.route('/anket/<kullanici_id>', methods=['GET', 'POST'])
def anket(kullanici_id):
    if request.method == 'POST':
        cevaplar = request.form
        dogru_sayisi = 0
        yanlis_sayisi = 0
        for soru in sorular_ve_cevaplar:
            kullanici_cevabi = cevaplar.get(soru['soru'])
            if kullanici_cevabi == soru['dogru_cevap']:
                dogru_sayisi += 1
            else:
                yanlis_sayisi += 1
        
        # Kullanıcı cevaplarını ve sonuçları veritabanında sakla
        mongo.db.cevaplar.insert_one({
            'kullanici_id': kullanici_id,
            'dogru': dogru_sayisi,
            'yanlis': yanlis_sayisi
        })
        
        return redirect(url_for('sonuclar', kullanici_id=kullanici_id))

    # Anket sorularını ve seçeneklerini bir liste içinde tanımla
    sorular = [
        {'soru': 'Soru 1:Aşağıdaki şıklardan hangisi fillna() metodunu ifade eder?', 'secenekler': {'A': 'Fillna metodu, bir DataFramedeki eksik (NaN) değerleri belirli bir değerle doldurmak için kullanılır.', 'B': 'Fillna, bir veri setindeki tüm değerleri belirli bir değerle değiştirmek için kullanılır.', 'C': ' Fillna fonksiyonu, bir veri çerçevesindeki tüm sütunlardaki değerleri toplar ve toplam değeri döndürür.', 'D': 'Fillna() fonksiyonu, veri setindeki sayısal değerleri rasgele seçilmiş başka bir değerle değiştirmek için kullanılır.'}},
        {'soru': 'Soru 2:Aşağıdaki şıklardan hangisi melt() metodunu ifade eder?', 'secenekler': {'A': 'Melt metodu, bir DataFrame i diğerine dönüştürmek için kullanılır', 'B':  'Melt, geniş formatlı veriyi uzun formata çevirmek için kullanılan bir işlemdir.', 'C': 'Pandas melt fonksiyonu, veri setini yeniden düzenlemek ve sütunları satırlara dönüştürmek için kullanılır.', 'D': ' Melt() fonksiyonu, genellikle veri analizi ve görselleştirmelerinde kullanılan bir veri dönüştürme işlemidir.'}},
        {'soru': 'Soru 3:Pandas kütüphanesinde bir dosyayı okuma işlemi nasıl gerçekleştirilir?', 'secenekler': {'A': 'pd.open_file(dosya.csv) komutu kullanılarak dosya okuma işlemi gerçekleştirilir.', 'B': 'pd.read_csv(dosya.csv) fonksiyonu kullanılarak dosya okuma işlemi gerçekleştirilir.', 'C': 'open(dosya.csv) komutu ile dosya açılıp, ardından pd.read() fonksiyonu ile okuma işlemi yapılır.', 'D': 'pandas.read_file(dosya.csv) fonksiyonu kullanılarak dosya okuma işlemi gerçekleştirilir.'}},
        {'soru': 'Soru 4:Makine öğrenimi nedir?', 'secenekler': {'A': ' Yapay zeka ile ilgili bir programlama dilidir.', 'B': 'Bilgisayarların öğrenme yeteneğini geliştiren bir alanı ifade eder.', 'C': 'Bilgisayar donanımının bir türüdür.', 'D': 'Bir matematik teoremi türüdür.'}},
        {'soru': 'Soru 5:Hangi aşama, bir makine öğrenimi modelinin performansını ölçmek için kullanılır?', 'secenekler': {'A': 'Eğitim', 'B': 'Doğrulama', 'C': 'Tahmin', 'D': 'Test'}},
        {'soru': 'Soru 6:"Denetimli öğrenme" nedir?', 'secenekler': {'A': 'Veri kümesinin etiketlenmiş örnekleri kullanılarak modelin eğitildiği bir öğrenme yöntemidir.', 'B': 'Modelin tamamen kendiliğinden öğrenmesini sağlayan bir öğrenme yöntemidir.', 'C': ' İnsanların öğrenme süreçlerini modelleyen bir öğrenme yöntemidir.', 'D': 'Veri kümesindeki boşlukları doldurarak öğrenilen bir yöntemdir.'}},
        {'soru': 'Soru 7:Hangisi regresyon analizi için kullanılan bir makine öğrenimi algoritmasıdır?', 'secenekler': {'A': 'K-Means', 'B': 'Decision Tree', 'C': 'Linear Regression', 'D': 'Naive Bayes'}},
        {'soru': 'Soru 8:"Overfitting" nedir?', 'secenekler': {'A': 'Modelin eğitim verilerine aşırı derecede uyum sağlaması durumudur.', 'B': 'Modelin eğitim verilerini ihmal etmesi durumudur.', 'C': ' Modelin eğitim sürecini hızlandıran bir tekniktir.', 'D': ' Modelin öğrenme yeteneğini kaybetmesi durumudur.'}},
        {'soru': 'Soru 9:Hangisi "unsupervised learning" için bir örnektir?', 'secenekler': {'A': 'Spam filtresi oluşturma', 'B': 'Haber başlıklarını kategorize etme', 'C': 'El yazısı sayıları tanıma', 'D': 'Film önerileri yapma'}},
        {'soru': 'Soru 10:Hangisi "convolutional neural network (CNN)" ile ilgili doğrudur?', 'secenekler': {'A': 'Ses verilerini işlemek için kullanılır.', 'B': 'Seri veriler üzerinde etkilidir, örneğin metin analizi için kullanılır.', 'C': 'Görüntü verilerinde lokal özellikleri vurgulamak için tasarlanmıştır.', 'D': 'Yapay sinir ağlarının eğitim sürecini hızlandırmak için kullanılır.'}}   # Diğer soruları da aynı şekilde güncelleyin
    ]


    # Şablonu bu sorular listesi ile render et
    return render_template('anket.html', sorular=sorular_ve_cevaplar, kullanici_id=kullanici_id)

@app.route('/sonuclar/<kullanici_id>')
def sonuclar(kullanici_id):
    sonuclar = mongo.db.cevaplar.find_one({'kullanici_id': kullanici_id})
    return render_template('sonuclar.html', dogru=sonuclar['dogru'], yanlis=sonuclar['yanlis'])

if __name__ == '__main__':
    app.run(debug=True)
