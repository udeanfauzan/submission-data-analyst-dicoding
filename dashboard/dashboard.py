import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="dark")
plt.style.use("dark_background")

# Helper function

def create_daygroup_df(df):
    day_group_df = df.groupby(by=["workingday","holiday"]).agg({
        "cnt": "mean"
    }).reset_index() 
    return day_group_df

def create_weathergroup_df(df):
    weathergroup_df = df.groupby(by="weathersit").agg({
        "casual": "mean",
        "registered":"mean"
    })
    return weathergroup_df

def create_hourly_df(df):
    hourly_counts_df = df.groupby(by="hr").agg({
        "cnt": "mean"
    }).reset_index()  
    return hourly_counts_df


# Load data
day_df = pd.read_csv("dashboard/main_data.csv")
hour_df = pd.read_csv("data/hour.csv")

# Filter data
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo 
    st.image("dashboard/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                       (day_df["dteday"] <= str(end_date))]

second_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                       (hour_df["dteday"] <= str(end_date))]


# create dataframe
day_group_df = create_daygroup_df(main_df)
weathergroup_df = create_weathergroup_df(main_df)
hourly_counts_df = create_hourly_df(second_df)


st.header("Bike Sharing Data Dashboard")
# Plot penggunaan sepeda pada hari kerja,akhir pekan, dan hari libur
st.subheader("Statistik Total Penyewaan pada Hari kerja, Akhir pekan, dan Hari Libur Nasional")
fig, ax = plt.subplots()
sns.barplot(data=day_group_df, x="workingday", y="cnt", hue="holiday", palette="Blues")
plt.ylabel("Jumlah rata-rata")
plt.title("Jumlah rata-rata sepeda yang disewa berdasarkan hari Kerja") 
for container in ax.containers:
    ax.bar_label(container, fontsize=10, color='white', weight='bold', label_type='edge')
plt.tight_layout()
st.pyplot(fig)
with st.expander('Keterangan Holiday'):
    st.write(
        """
        `Holiday`: Hari libur Nasional
        
        `Not Holiday`: Akhir pekan
        """
    )

# Scatter plot Hubungan faktor cuaca dengan pengguna
st.subheader("Statistik Hubungan Faktor Cuaca")
fig, ax = plt.subplots()
plt.figure(figsize=(20, 6))

# Memvisualisasikan hubungan suhu
plt.subplot(1, 4, 1)
sns.scatterplot(data=day_df, x="temp", y="casual", label="Casual", color="blue")
sns.scatterplot(data=day_df, x="temp", y="registered", label="Registered", color="orange")
plt.title("Hubungan Suhu dengan Pengguna Sepeda")
plt.xlabel("Suhu")
plt.ylabel("Jumlah Pengguna")

# memvisualisasikan hubungan suhu yang dirasakan
plt.subplot(1, 4, 2)
sns.scatterplot(data=day_df, x="atemp", y="casual", label="Casual", color="blue")
sns.scatterplot(data=day_df, x="atemp", y="registered", label="Registered", color="orange")
plt.title("Hubungan Suhu yang dirasakan dengan Pengguna Sepeda")
plt.xlabel("Suhu")
plt.ylabel("Jumlah Pengguna")

# memvisualisasikan Hubungan kelembaban
plt.subplot(1, 4, 3)
sns.scatterplot(data=day_df, x="hum", y="casual", label="Casual", color="blue")
sns.scatterplot(data=day_df, x="hum", y="registered", label="Registered", color="orange")
plt.title("Hubungan Kelembaban dengan Pengguna Sepeda")
plt.xlabel("Kelembaban")
plt.ylabel("Jumlah Pengguna")

# memvisualisasikan Hubungan kecepatan angin
plt.subplot(1, 4, 4)
sns.scatterplot(data=day_df, x="windspeed", y="casual", label="Casual", color="blue")
sns.scatterplot(data=day_df, x="windspeed", y="registered", label="Registered", color="orange")
plt.title("Hubungan Kecepatan Angin dengan Pengguna Sepeda")
plt.xlabel("Kecepatan Angin")
plt.ylabel("Jumlah Pengguna")
plt.tight_layout()
st.pyplot(plt.gcf())


# Plot jumlah penyewaan berdasarkan kondisi cuaca
# Casual
st.subheader("Statistik Rata-rata Penyewaan Sepeda Pengguna Casual berdasarkan Cuaca")
fig, ax = plt.subplots(figsize=(20,12))
sns.barplot(data=weathergroup_df, x="weathersit", y="casual", palette="Blues")
plt.ylabel("Jumlah Rata-rata Penyewa Sepeda", fontsize=24)
plt.title("Jumlah Rata-rata Penyewa Sepeda Pengguna Casual berdasarkan Cuaca", fontsize=24)
for container in ax.containers:
    ax.bar_label(container, fontsize=24, color='white', weight='bold', label_type='edge')
plt.tight_layout()
st.pyplot(fig)

# Registered
st.subheader("Statistik Rata-rata Penyewaan Sepeda Pengguna Registered berdasarkan Cuaca")
fig, ax = plt.subplots(figsize=(20,12))
sns.barplot(data=weathergroup_df, x="weathersit", y="registered", palette="Oranges")
plt.ylabel("Jumlah Rata-rata Penyewa Sepeda", fontsize=24)
plt.title("Jumlah Rata-rata Penyewa Sepeda Pengguna Registered berdasarkan Cuaca", fontsize=24)
for container in ax.containers:
    ax.bar_label(container, fontsize=24, color='white', weight='bold', label_type='edge')
plt.tight_layout()
st.pyplot(fig)


# Plot jumlah penyewaan tiap jam
st.subheader("Statistik Pola Rata-rata Penyewaan Sepeda Tiap Jam")
fig, ax = plt.subplots()
sns.lineplot(data=hourly_counts_df, x="hr", y="cnt", palette="Blues", marker="o")
plt.xlabel("Jam")
plt.ylabel("Jumlah Rata-rata Penyewaan Sepeda")
plt.title("Jumlah Rata-rata Sepeda yang Disewakan Tiap Jam")
plt.xticks(ticks=hourly_counts_df["hr"], labels=hourly_counts_df["hr"])
plt.tight_layout()
st.pyplot(fig)

st.caption("Copyright © 2024 Muhammad Daffa Fauzan")