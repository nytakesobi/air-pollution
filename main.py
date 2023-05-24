import pandas as pd
import folium
import streamlit as st
import feedparser
import seaborn as sns
from PIL import Image
from matplotlib import pyplot as plt
from folium import plugins
from streamlit_folium import st_folium, folium_static


sidebar_options = ['Головна сторінка', 'Новини', 'Візуалізація', 'Рекомендації']
select_page = st.sidebar.selectbox('Оберіть сторінку', sidebar_options)


# "ГОЛОВНА СТОРІНКА"
if select_page == 'Головна сторінка':
    st.title('Забруднення повітря')

    st.write(
    """
    Забруднення повітря складається з хімічних речовин або частинок у повітрі, які можуть завдати шкоди здоров’ю людей, тварин і рослин
    """
    )

    img1 = Image.open('C:/Users/kalok/PycharmProjects/mkalokhina/air_pollution.jpg')
    img2 = Image.open('C:/Users/kalok/PycharmProjects/mkalokhina/air_pollution4.jpg')

    col1, col2 = st.columns(2)
    with col1:
        st.image(img1, use_column_width=True)
    with col2:
        st.image(img2, use_column_width=True)


    st.subheader('Джерела забруднення повітря')
    st.write(
    """
    Забруднення потрапляє в атмосферу Землі різними шляхами. Більшість забруднень повітря створюється людьми у формі викидів заводів, автомобілів, літаків або аерозольних балонів. Пасивний сигаретний дим також вважається забрудненням повітря. Ці техногенні джерела забруднення називають антропогенними.

    Деякі типи забруднення повітря, такі як дим від лісових пожеж або попіл від вулканів, є природними. Це так звані природні джерела.

    Забруднення повітря найбільш поширене у великих містах, де зосереджені викиди з багатьох різних джерел. Іноді гори або високі будівлі перешкоджають поширенню забруднення повітря. Це забруднення повітря часто виглядає як хмара, яка робить повітря каламутним. Його називають смогом. Слово «смог» походить від поєднання слів «дим» і «туман».

    Великі міста бідних країн і країн, що розвиваються, як правило, мають більше забруднення повітря, ніж міста розвинених країн. За даними Всесвітньої організації охорони здоров’я (ВООЗ), одними з найбільш забруднених міст світу є Карачі, Пакистан; Нью-Делі, Індія; Пекін, Китай; Ліма, Перу; і Каїр, Єгипет. Проте багато розвинених країн також мають проблеми із забрудненням повітря. Лос-Анджелес, штат Каліфорнія, називають Містом Смогу.
    """
    )


    st.subheader('Вплив на людину')
    image_human = Image.open('C:/Users/kalok/PycharmProjects/mkalokhina/human_air.jpg')
    st.image(image_human)
    st.write(
    """
    Люди відчувають широкий спектр наслідків для здоров'я від впливу забрудненого повітря. Ефекти можна розбити на короткострокові та довгострокові.

    Короткочасні наслідки, які є тимчасовими, включають такі захворювання, як пневмонія або бронхіт. Вони також включають дискомфорт, такий як подразнення носа, горла, очей або шкіри. Забруднене повітря також може викликати головний біль, запаморочення та нудоту. Неприємні запахи, які створюють заводи, сміття чи каналізаційні системи, також вважаються забрудненням повітря. Ці запахи менш серйозні, але все одно неприємні.

    Довгостроковий вплив забруднення повітря може тривати роками або все життя. Вони можуть призвести навіть до смерті людини. Довгострокові наслідки забруднення повітря для здоров’я включають хвороби серця, рак легенів і респіраторні захворювання, такі як емфізема. Забруднення повітря також може завдати довгострокової шкоди нервам, мозку, ниркам, печінці та іншим органам людей. Деякі вчені підозрюють, що забруднювачі повітря спричиняють вроджені дефекти. Майже 2,5 мільйона людей щороку помирають у світі від наслідків забруднення повітря на вулиці чи всередині приміщень.
    """
    )


# СТОРІНКА "НОВИНИ"
if select_page == 'Новини':
    st.title('Latest News on Air Pollution from The Guardian')

    # загружаємо новини з The Guardian
    feed_url = 'https://www.theguardian.com/environment/air-pollution/rss'
    feed = feedparser.parse(feed_url)

    for post in feed.entries:
        st.write('##', post.title)
        st.write(post.link)
        st.write(post.published)


# СТОРІНКА "КАРТА ТА ГРАФІК"
if select_page == 'Візуалізація':
    st.sidebar.info(
        """
        На цій сторінці можна на власні очі можете побачити та проаналізувати одну з глобальних проблем людства 
        """
    )
    st.sidebar.title('Фільтри')

    with st.container():
        st.header("Назви забруднювачів")

    col1, col2 = st.columns(2)

    with col1:
        st.text("1.  NO2 - діоксид азоту \n2.  NO - оксид азоту \n3.  CO - вуглекислий газ \n4.  BC - чорний вуглець \n5.  O3 - озон \n6.  PM2.5 - частки розміром менше 2.5 мікрометрів (забруднювачі повітря)")

    with col2:
        st.text("7.  SO2 - діоксид сірки \n8.  NOX - суміш оксидів азоту \n9.  PM1 - частки розміром менше 1 мікрометра (забруднювачі повітря) \n10.  PM10 - частки розміром менше 10 мікрометрів (забруднювачі повітря)")


    # загрузка даних
    @st.cache_data
    def load_data():
        df_air = pd.read_excel("C:/Users/kalok/PycharmProjects/mkalokhina/openaq.xlsx")
        df_geo = pd.read_excel("C:/Users/kalok/PycharmProjects/mkalokhina/worldcities1.xlsx")
        df = pd.merge(df_air, df_geo, left_on=['Country Code', 'City'], right_on=[
            'iso2', 'City'], how='left')
        df = df.dropna(subset=['Coordinates'])
        df[['Lat', 'Lon']] = df['Coordinates'].str.split(
            ',', expand=True).astype(float)
        df['Last Updated'] = pd.to_datetime(df['Last Updated'], utc=True)
        return df


    df = load_data()

    country = st.sidebar.multiselect("Оберіть країну", df["Country Label"].unique())
    year_options = df[df["Country Label"].isin(country)]["Last Updated"].dt.year.unique()
    year = st.sidebar.selectbox("Оберіть рік", year_options)
    pollutant_options = df['Pollutant'].unique()
    pollutant = st.sidebar.multiselect("Оберіть забруднювач", pollutant_options)
    save_data_button = st.sidebar.checkbox('Зберегти дані')
    show_data = st.sidebar.checkbox('Показати дані')
    button1 = st.sidebar.checkbox("Показати карту")
    button2 = st.sidebar.checkbox("Показати графіки")


    if save_data_button:

        # відображення ексель данних + скачування
        filtered_df = df[df['Country Label'] == country[0]]
        columns_to_display = ['Country Label', 'Last Updated', 'City', 'Pollutant', 'Value']

        if show_data:
            st.subheader('Дані ро забруднення повітря у вибраній країні')
            st.table(filtered_df[columns_to_display])
            csv = filtered_df[columns_to_display].to_csv(index=False)
            st.download_button("Download CSV", data=csv, file_name='data.csv', mime='text/csv')

        # фільтруємо обрані дані

        inCountry = df["Country Label"].isin(country)
        withCords = df['Lon'].notna() & df['Lat'].notna()
        selectedPollutants = df['Pollutant'].isin(pollutant)
        selectedYear = df['Last Updated'].dt.year == year
        filtered_df = df[inCountry & withCords & selectedPollutants & selectedYear]

        if button1:
            st.subheader("{} в {}".format(", ".join(pollutant), ", ".join(country)))

            high_threshold = 5.0
            medium_threshold = 3.0
            map_air = folium.Map()
            heat_data = []

            # позначки на карті
            for index, row in filtered_df.iterrows():
                if row['Pollutant'] in pollutant:
                    heat_data.append([row['Lat'], row['Lon'], row['Value']])
            plugins.HeatMap(heat_data).add_to(map_air)

            # додаємо позначки на місца
            cities_data = filtered_df[['Lat', 'Lon', 'City']].drop_duplicates()
            for _, city_row in cities_data.iterrows():
                city_location = [city_row['Lat'], city_row['Lon']]
                city_name = city_row['City']
                folium.Marker(city_location, popup=city_name).add_to(map_air)

            marker_cluster = plugins.MarkerCluster().add_to(map_air)

            for _, heat_row in filtered_df.iterrows():
                heat_location = [heat_row['Lat'], heat_row['Lon']]
                heat_value = heat_row['Value']
                radius = 5

                # колір позначок
                if heat_value >= high_threshold:
                    color = 'red'
                elif heat_value >= medium_threshold:
                    color = 'yellow'
                else:
                    color = 'blue'

            st_data = st_folium(map_air, width=700)

        if button2:

            # графік для відображення забруднення повітря в містах обраних країн
            st.subheader("Відображення забруднювачів {} в містах {}".format(", ".join(pollutant), ", ".join(country)))

            if len(filtered_df) > 0:
                filtered_df[['Country Label', 'City', 'Pollutant', 'Value']].groupby(
                    ['Country Label', 'City', 'Pollutant']).max().unstack('Pollutant').plot.bar()
                plt.xlabel('Місто')
                plt.ylabel('Рівень забруднення')
                plt.xticks(rotation=90)
                st.pyplot(plt)

            # 2 графік для порівнянь обраних країн по рівню забруднення повітря
            st.subheader("Порівння забруднення повітря в {} ".format(", ".join(country)))
            if len(filtered_df) > 0:
                df_selected = filtered_df[filtered_df['Country Label'].isin(country)][
                    ['Country Label', 'Pollutant', 'Value']]
                df_agg = df_selected.groupby(['Country Label', 'Pollutant']).max().reset_index()
                sns.set(style="whitegrid")
                plt.figure(figsize=(12, 6))
                ax = sns.barplot(x='Country Label', y='Value', hue='Pollutant', data=df_agg)
                ax.set_xlabel('Країни')
                ax.set_ylabel('Рівень забруднення повітря')
                plt.xticks(rotation=45)
                st.pyplot(plt)

            # кругова діаграма
            st.subheader("Діграма з порівнянням обраних забруднювачів")

            if len(filtered_df) > 0:
                pollutant_counts = filtered_df['Pollutant'].value_counts()
                plt.figure(figsize=(8, 8))
                plt.pie(pollutant_counts, labels=pollutant_counts.index, autopct='%1.1f%%')
                plt.axis('equal')
                st.pyplot(plt)




# СТОРІНКА "РЕКОМЕНДАЦІЇ"
if select_page == 'Рекомендації':
    st.title('Як вберегти себе та довкілля від забруднення повітря?')
    st.write(
        """
        Забруднення повітря є серйозною проблемою, яка впливає на здоров'я людей та навколишнє середовище. Ось кілька рекомендацій, які можуть допомогти знизити рівень забруднення повітря:
        
        1. Використовуйте громадський транспорт, велосипед або йдіть пішки замість того, щоб їздити на автомобілі. Транспортні засоби є одним із основних джерел забруднення повітря, особливо у містах.
        """)

    photo1 = Image.open('C:/Users/kalok/PycharmProjects/mkalokhina/photo1.jpg')
    st.image(photo1)
        
    st.write(
        """
        2. Використовуйте електромобілі або гібридні автомобілі, які виділяють менше шкідливих речовин в атмосферу.
        """)

    photo2 = Image.open('C:/Users/kalok/PycharmProjects/mkalokhina/photo2.jpg')
    st.image(photo2)

    st.write(
        """
        3. Слідкуйте за тим, що спалюєте. Уникайте спалювання сміття, листя, гілок та інших відходів, оскільки це є одним із джерел викидів в атмосферу.
        """)
    photo3 = Image.open('C:/Users/kalok/PycharmProjects/mkalokhina/photo3.jpg')
    st.image(photo3)

    st.write(
        """
        4. Використовуйте енергоефективні та екологічно чисті системи опалення та кондиціювання повітря. Зверніть увагу на енергоефективність при покупці нових пристроїв.
        """)
    photo4 = Image.open('C:/Users/kalok/PycharmProjects/mkalokhina/photo4.jpg')
    st.image(photo4)

    st.write(
        """
        5. Намагайтеся заощаджувати електроенергію. Вимикайте світло та електроприлади, коли вони не використовуються.
        """)
    photo5 = Image.open('C:/Users/kalok/PycharmProjects/mkalokhina/photo5.jpg')
    st.image(photo5)

    st.write(
        """
        6. Підтримуйте та дотримуйтесь екологічних вимог та законів, які спрямовані на скорочення викидів шкідливих речовин в атмосферу.
        """)
    photo6 = Image.open('C:/Users/kalok/PycharmProjects/mkalokhina/photo6.jpg')
    st.image(photo6)

    st.write(
        """
        Ці рекомендації допоможуть знизити рівень забруднення повітря та покращити якість життя.
        """)
