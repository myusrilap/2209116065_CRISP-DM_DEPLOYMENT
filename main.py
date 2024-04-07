import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import numpy as np

st.title('Online Chess game Analysis & Prediction Results')

url = 'Data_Cleaned.csv'
df = pd.read_csv(url)

st.write(df.head(5))

counts = df["winner"].value_counts()
total_games = sum(counts)
white_win_pct = round(counts.values[0] / total_games * 100, 2)
black_win_pct = round(counts.values[1] / total_games * 100, 2)
draw_pct = round(counts.values[2] / total_games * 100, 2 )

result_df = pd.DataFrame({
    'Winner': ['White', 'Black', 'Draw'],
    'Percentage': [white_win_pct, black_win_pct, draw_pct]
})

st.subheader("Hasil Permainan")
st.text(f'Putih menang: {white_win_pct}%')
st.text(f'Hitam menang: {black_win_pct}%')
st.text(f'Draw: {draw_pct}%')

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x='Winner', y='Percentage', data=result_df, palette='Set1', ax=ax)
ax.set_title("Persentase Kemenangan")
ax.set_xlabel("Pihak yang Menang")
ax.set_ylabel("Persentase")
ax.set_ylim(0, 100)
st.pyplot(fig)
st.write("Grafik menunjukkan bahwa ada keseimbangan antara kemenangan putih dan hitam, dengan putih memiliki sedikit keunggulan dengan 50% kemenangan dibandingkan dengan 45% kemenangan hitam. Hal ini menunjukkan bahwa tidak ada warna tertentu yang secara signifikan lebih unggul daripada yang lain dalam permainan catur online.")
st.write ('Meskipun draw adalah hasil yang mungkin dalam permainan catur, grafik menunjukkan bahwa hasil draw hanya terjadi dalam 4 % dari total permainan. Hal ini menunjukkan bahwa mayoritas permainan catur berakhir dengan kemenangan salah satu pihak')

st.subheader("Permainan Berperingkat")
counts_rated = df["rated"].value_counts()
total_games = sum(counts_rated)
True_pct = round(counts_rated[True] / total_games * 100, 2)
False_pct = round(counts_rated[False] / total_games * 100, 2)

st.text(f'Berperingkat: {True_pct}%')
st.text(f'Tidak Berperingkat: {False_pct}%')
fig_count, ax_count = plt.subplots(figsize=(8, 6))
sns.countplot(x=df['rated'], palette='Set1', ax=ax_count)
ax_count.set_title("Permainan Berperingkat")
ax_count.set_xlabel("Status Permainan dinilai")
ax_count.set_ylabel("Jumlah Permainan")
st.pyplot(fig_count)
st.write("Mayoritas pemain cenderung bermain dalam konteks kompetitif dengan permainan berperingkat, menunjukkan motivasi untuk meningkatkan peringkat dan mencari tantangan yang lebih besar dalam kompetisi, sehingga memerlukan fokus pada pengembangan fitur dan konten yang meningkatkan pengalaman dalam permainan berperingkat.")

# Ubah nilai dalam kolom 'victory_status'
df['victory_status'] = df['victory_status'].replace({0: 'Resign', 1: 'Out of Time', 2: 'Mate', 3: 'Draw'})

# Hitung jumlah masing-masing nilai pada kolom 'victory_status' setelah penggantian
# Hitung jumlah masing-masing nilai pada kolom 'victory_status' setelah penggantian
victory_status_counts = df['victory_status'].value_counts()

# Mengurutkan counts_status berdasarkan index
victory_status_counts = victory_status_counts.sort_index()

# Tampilkan plot pie
total_games = sum(victory_status_counts)
resign_pct = round(victory_status_counts['Resign'] / total_games * 100,2)
outoftime_pct = round(victory_status_counts['Out of Time'] / total_games * 100,2)
mate_pct = round(victory_status_counts['Mate'] / total_games * 100,2)
draw_pct = round(victory_status_counts['Draw'] / total_games * 100,2)

st.subheader("Hasil Permainan")
st.text(f'Resign: {resign_pct}%')
st.text(f'Mate: {mate_pct}%')
st.text(f'Out Of Time: {outoftime_pct}%')
st.text(f'Draw: {draw_pct}%')

fig_pie, ax_pie = plt.subplots()
ax_pie.pie(victory_status_counts, labels=victory_status_counts.index, autopct='%1.1f%%', startangle=140, colors=['skyblue', 'lightgreen', 'lightcoral', 'orange'])
ax_pie.set_title('Hasil Permainan')
ax_pie.set_ylabel('')
ax_pie.axis('equal')  # Memastikan lingkaran berbentuk lingkaran
st.pyplot(fig_pie)
st.write("Tingginya jumlah permainan yang berakhir dengan resign menandakan bahwa banyak pemain cenderung menyerah saat merasa dalam posisi yang tidak menguntungkan atau kehilangan minat dalam permainan.")

df['game_type'] = df['game_type'].replace({0: 'Bullet', 1: 'Blitz', 2: 'Rapid', 3: 'Classical'})

# Hitung jumlah masing-masing nilai pada kolom 'game_type' setelah penggantian
# Menghitung jumlah masing-masing nilai pada kolom 'game_type' setelah penggantian
counts_type = df["game_type"].value_counts()

# Menentukan total permainan
total_games = sum(counts_type)

# Menghitung presentase untuk setiap jenis permainan
bullet_pct = round(counts_type['Bullet'] / total_games * 100, 2)
blitz_pct = round(counts_type['Blitz'] / total_games * 100, 2)
rapid_pct = round(counts_type['Rapid'] / total_games * 100, 2)
classical_pct = round(counts_type['Classical'] / total_games * 100, 2)

# Menampilkan distribusi jenis permainan
st.subheader("Distribusi Jenis Permainan")
st.text(f'Bullet: {bullet_pct}%')
st.text(f'Blitz: {blitz_pct}%')
st.text(f'Rapid: {rapid_pct}%')
st.text(f'Classical: {classical_pct}%')

# Plot distribusi jenis permainan
fig_time, ax_time = plt.subplots(figsize=(8, 6))
sns.countplot(x='game_type', data=df, palette='Set1', ax=ax_time)
ax_time.set_title("Distribusi Jenis Permainan")
ax_time.set_xlabel("Jenis Permainan")
ax_time.set_ylabel("Jumlah Permainan")
st.pyplot(fig_time)
st.write("Distribusi jenis permainan menunjukkan bahwa sebagian besar permainan berada dalam kategori Rapid, dengan persentase sebesar 78%. Hal ini mengindikasikan bahwa mayoritas pemain cenderung memilih untuk bermain dalam mode permainan yang memberikan waktu lebih banyak untuk berpikir dan merencanakan strategi, namun tetap mempertahankan tingkat kecepatan yang relatif tinggi. Sedangkan persentase permainan dalam kategori Blitz sebesar 19%, menunjukkan adanya minat yang cukup signifikan dalam permainan yang lebih cepat dengan batasan waktu yang lebih ketat. Sementara itu, permainan dalam kategori Classical memiliki persentase yang sangat rendah, hanya sebesar 1%, yang mungkin menandakan bahwa permainan dengan waktu yang lebih panjang tidak begitu diminati oleh mayoritas pemain.")
st.write('Dengan persentase permainan yang tinggi dalam kategori Rapid, pengembangan fitur dan konten baru dapat difokuskan pada memperkaya pengalaman bermain dalam mode Rapid, seperti menyediakan panduan strategi khusus untuk mode ini atau mengadakan turnamen dengan aturan permainan Rapid yang menarik.')

df['Skill level'] = df['Skill level'].replace({0: 'Beginner', 1: 'Intermediate', 2: 'Advanced', 3: 'Expert'})

# Menghitung jumlah masing-masing nilai pada kolom 'Skill level' setelah penggantian
skill_level_counts = df['Skill level'].value_counts()

# Menentukan total permainan
total_games = sum(skill_level_counts)

# Menghitung presentase untuk setiap tingkat keahlian
beginner_pct = round(skill_level_counts['Beginner'] / total_games * 100, 2)
intermediate_pct = round(skill_level_counts['Intermediate'] / total_games * 100, 2)
advanced_pct = round(skill_level_counts['Advanced'] / total_games * 100, 2)
expert_pct = round(skill_level_counts['Expert'] / total_games * 100, 2)

# Menampilkan distribusi tingkat keahlian
st.subheader("Distribusi Tingkat Keahlian")
st.text(f'Beginner: {beginner_pct}%')
st.text(f'Intermediate: {intermediate_pct}%')
st.text(f'Advanced: {advanced_pct}%')
st.text(f'Expert: {expert_pct}%')

# Plot distribusi tingkat keahlian
fig_skill, ax_skill = plt.subplots(figsize=(8, 6))
sns.countplot(x='Skill level', data=df, palette='Set1', ax=ax_skill)
ax_skill.set_title("Distribusi Tingkat Keahlian")
ax_skill.set_xlabel("Tingkat Keahlian")
ax_skill.set_ylabel("Jumlah Permainan")
st.pyplot(fig_skill)

st.write("Distribusi tingkat kemampuan pemain menunjukkan bahwa mayoritas pemain berada dalam kategori Intermediate, dengan persentase sebesar 72%. Hal ini mengindikasikan bahwa sebagian besar pemain memiliki tingkat kemampuan yang cukup untuk bermain catur secara kompetitif, namun mungkin masih membutuhkan pengembangan keterampilan tambahan untuk mencapai tingkat lanjut. Sementara itu, persentase pemain dalam kategori Advanced sebesar 20%, menunjukkan bahwa ada sejumlah pemain yang sudah berpengalaman dalam permainan. Persentase yang lebih rendah dari pemain dalam kategori Beginner dan Expert (masing-masing 5% dan 1%) menunjukkan bahwa pemain dengan tingkat kemampuan tinggi dan rendah relatif jarang ditemui, namun masih penting untuk memberikan dukungan dan tantangan tambahan bagi mereka.")
st.write(' Dengan mayoritas pemain berada dalam kategori Intermediate, pengembangan fitur dan konten baru dapat difokuskan pada membantu pemain mencapai tingkat kemampuan yang lebih tinggi. Ini dapat dilakukan melalui penyediaan materi pembelajaran lanjutan, panduan strategi yang lebih mendalam, atau sesi pelatihan khusus yang disesuaikan dengan kebutuhan pemain Intermediate.')

st.subheader('Prediksi Hasil Permainan')
file_path = 'dtc_model.pkl'
clf = joblib.load(file_path)

# Define a function to determine skill level
def determine_skill_level(avg_rating):
    if avg_rating < 1200:
        return 0  # Beginner
    elif 1200 <= avg_rating < 1600:
        return 1  # Intermediate
    elif 1600 <= avg_rating < 2000:
        return 2  # Advanced
    else:
        return 3  # Expert

# Input form for game details
rated_game = st.checkbox('Rated Game')
number_of_turns = st.number_input('Number of Turns', value=0)  # Default value is 0
victory_status = st.selectbox('Victory Status', ["Resign", "Out Of Time",'Mate', 'Draw'])
white_rating = st.number_input('White Rating', value=0)  # Default value is 0
black_rating = st.number_input('Black Rating', value=0)  # Default value is 0
average_rating = (white_rating + black_rating) / 2
game_type = st.selectbox('Game Type', ['Bullet', 'Blitz', 'Rapid', 'Classical'])
skill_level = determine_skill_level (average_rating)

# Input form for selecting opening shortnames
selected_openings = st.selectbox('Pilih Opening Shortnames:', df.columns[8:])
victory_statuses = {'Resign': 0, 'Out Of Time': 1, 'Mate': 2, 'Draw': 3}
victory_status = victory_statuses[victory_status]

game_types = {'Bullet': 0, 'Blitz': 1, 'Rapid': 2, 'Classical': 3}
game_type = game_types[game_type]

# Process selected openings
input_openings = [0] * len(df.columns[8:])  # Initialize all to 0
input_openings[df.columns[8:].tolist().index(selected_openings)] = 1  # Set the selected opening to 1

if st.button('Predict'):
    input_data = [[rated_game, number_of_turns, victory_status, white_rating, black_rating, average_rating, skill_level] + input_openings]
    # Perform prediction
    result = clf.predict(input_data)

    # Display prediction result
    if result.size > 0:
        if result[0] == 0:
            st.write('Hasil Prediksi adalah hitam menang.')
        elif result[0] == 1:
            st.write('Hasil Prediksi adalah putih menang')
        else:
            st.write('Hasil Prediksi adalah Seri.')
    else:
        st.write('Maaf, tidak dapat membuat prediksi. Mohon periksa kembali input Anda.')



