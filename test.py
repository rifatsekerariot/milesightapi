import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import base64
import urllib3

# SSL uyarılarını gizle (Yerel ağda HTTPS sertifikası genelde imzalı değildir)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Sabit Ayarlar ---
GATEWAY_IP = "192.168.1.5"
API_PORT = "8080" # Dokümandaki örneklerde port 8080 olarak belirtilmiştir [1]
BASE_URL = f"https://{GATEWAY_IP}:{API_PORT}/api"

st.set_page_config(page_title="UG65 LoRaWAN Analiz", layout="wide")
st.title("Milesight UG65 LoRaWAN Paket Analizi")

# --- Yan Menü: Giriş Bilgileri ---
st.sidebar.header("Oturum Ayarları")
username = st.sidebar.text_input("Kullanıcı Adı", value="admin") 
# Not: Firmware sürümüne göre kullanıcı adı 'apiuser' veya 'admin' olabilir [1]
password = st.sidebar.text_input("Şifre", type="password")
org_id = st.sidebar.text_input("Organization ID", value="1") # API gereksinimi [2]

# --- Fonksiyon: Token Alma (Login) ---
def get_token(user, pwd):
    login_url = f"{BASE_URL}/internal/login" # Doküman 1.1 [1]
    headers = {"Content-Type": "application/json"}
    payload = {
        "username": user,
        "password": pwd
    }
    
    try:
        response = requests.post(login_url, json=payload, headers=headers, verify=False)
        if response.status_code == 200:
            # Yanıttan JWT token'ı al [3]
            return response.json().get("jwt")
        else:
            st.error(f"Giriş Başarısız: {response.text}")
            return None
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")
        return None

# --- Fonksiyon: Paketleri Çekme ---
def get_packets(token):
    packets_url = f"{BASE_URL}/urpackets" # Doküman 10.1 [2]
    headers = {
        "Authorization": f"Bearer {token}", # Token başlıkta gönderilmeli [4]
        "Content-Type": "application/json"
    }
    # Limit ve organizationID parametreleri gereklidir [2]
    params = {
        "limit": 100, 
        "offset": 0,
        "organizationID": org_id
    }
    
    try:
        response = requests.get(packets_url, headers=headers, params=params, verify=False)
        if response.status_code == 200:
            data = response.json()
            return data.get("packets", []) # Paket listesini döndür [2]
        else:
            st.error(f"Veri Çekme Hatası: {response.text}")
            return []
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")
        return []

# --- Ana Uygulama Akışı ---
if st.sidebar.button("Verileri Getir"):
    if not password:
        st.warning("Lütfen şifrenizi girin.")
    else:
        with st.spinner('Ağ geçidine bağlanılıyor...'):
            # 1. Adım: Token al
            token = get_token(username, password)
            
            if token:
                # 2. Adım: Paketleri çek
                packets = get_packets(token)
                
                if packets:
                    st.success(f"{len(packets)} adet paket başarıyla çekildi.")
                    
                    # Veriyi DataFrame'e çevir
                    df = pd.DataFrame(packets)
                    
                    # Zaman damgasını okunabilir formata çevir (ISO 8601)
                    if 'time' in df.columns:
                        df['time'] = pd.to_datetime(df['time'])
                    
                    # Sayısal dönüşümler (Grafik için gerekli)
                    df['rssi'] = pd.to_numeric(df['rssi'], errors='coerce')
                    df['loraSNR'] = pd.to_numeric(df['loraSNR'], errors='coerce') # [2]
                    
                    # --- Görselleştirme ---
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Sinyal Kalitesi (RSSI)")
                        fig_rssi = px.line(df, x='time', y='rssi', color='devEUI', 
                                           title='Cihaz Bazlı RSSI Değerleri', markers=True)
                        st.plotly_chart(fig_rssi, use_container_width=True)
                        
                    with col2:
                        st.subheader("Sinyal Gürültü Oranı (SNR)")
                        fig_snr = px.line(df, x='time', y='loraSNR', color='devEUI', 
                                          title='Cihaz Bazlı SNR Değerleri', markers=True)
                        st.plotly_chart(fig_snr, use_container_width=True)

                    # --- Ham Veri Tablosu ---
                    st.subheader("Detaylı Paket Listesi")
                    # Tabloda gösterilecek sütunları seç (Dokümandaki alanlara göre [2])
                    display_cols = ['time', 'devEUI', 'type', 'frequency', 'rssi', 'loraSNR', 'fCnt', 'payloadBase64']
                    # Mevcut olmayan sütunlar varsa hata vermemesi için filtrele
                    valid_cols = [c for c in display_cols if c in df.columns]
                    st.dataframe(df[valid_cols].sort_values(by='time', ascending=False))
                    
                else:
                    st.info("Görüntülenecek paket bulunamadı veya liste boş.")