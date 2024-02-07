import streamlit as st
from streamlit_gsheets import GSheetsConnection
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import yfinance as yf  
import plotly.graph_objs as go
import riskfolio as rp
#from gspread_dataframe import get_as_dataframe, set_with_dataframe
from streamlit_option_menu import option_menu
import pandas as pd
from yahooquery import Screener
from yahooquery import Ticker
import yahooquery as yq
import yesg
import ast

dict_industry = { 'Basic Materials' : ['agricultural_inputs', 'aluminum', 'building_materials', 'chemicals', 'coking_coal', 'copper', 'gold', 'high_yield_high_return', 'high_yield_high_return_asia', 'high_yield_high_return_europe',
 'lumber_wood_production', 'most_visited_basic_materials', 'ms_basic_materials', 'other_industrial_metals_mining', 'other_precious_metals_mining', 'paper_paper_products',
 'silver', 'specialty_chemicals', 'steel'],
                'Communication Services': ['advertising_agencies', 'broadcasting', 'electronic_gaming_multimedia', 'entertainment', 'high_yield_high_return', 'high_yield_high_return_asia', 'high_yield_high_return_europe', 'internet_content_information',
 'most_visited_communication_services', 'ms_communication_services', 'publishing', 'telecom_services'],
                'Consumer Cyclical' : ['apparel_manufacturing',
 'apparel_retail', 'auto_manufacturers', 'auto_parts', 'auto_truck_dealerships', 'department_stores', 'footwear_accessories', 'furnishings_fixtures_appliances', 'gambling',
 'high_yield_high_return', 'high_yield_high_return_asia', 'high_yield_high_return_europe', 'home_improvement_retail', 'internet_retail', 'leisure', 'lodging', 'luxury_goods', 'most_visited_consumer_cyclical', 'ms_consumer_cyclical', 'packaging_containers', 'personal_services', 'recreational_vehicles',
 'residential_construction', 'resorts_casinos', 'restaurants', 'specialty_retail', 'textile_manufacturing', 'travel_services'],
                'Consumer Defensive' : ['beverages_brewers', 'beverages_non_alcoholic', 'beverages_wineries_distilleries', 'confectioners', 'discount_stores', 'education_training_services',
 'farm_products', 'food_distribution', 'grocery_stores', 'high_yield_high_return', 'high_yield_high_return_asia', 'high_yield_high_return_europe', 'household_personal_products',
 'most_visited_consumer_defensive', 'ms_consumer_defensive', 'packaged_foods', 'tobacco'],
                'Energy' : ['high_yield_high_return', 'high_yield_high_return_asia', 'high_yield_high_return_europe', 'most_visited_energy', 'ms_energy', 'oil_gas_drilling',
 'oil_gas_e_p', 'oil_gas_equipment_services', 'oil_gas_integrated', 'oil_gas_midstream', 'oil_gas_refining_marketing', 'thermal_coal', 'top_energy_us', 'uranium'],
                'Financial Services' : ['asset_management', 'banks_diversified', 'banks_regional', 'capital_markets', 'credit_services', 'financial_conglomerates', 'financial_data_stock_exchanges',
 'insurance_brokers', 'insurance_diversified', 'insurance_life', 'insurance_property_casualty', 'insurance_reinsurance', 'insurance_specialty', 'mortgage_finance',
 'most_visited_financial_services', 'ms_financial_services', 'shell_companies'],
                'Healthcare' : ['biotechnology', 'diagnostics_research', 'drug_manufacturers_general', 'drug_manufacturers_specialty_generic', 'health_information_services', 'healthcare_plans', 'high_yield_high_return', 'high_yield_high_return_asia', 'high_yield_high_return_europe', 'medical_care_facilities',
 'medical_devices', 'medical_distribution', 'medical_instruments_supplies', 'mega_cap_hc', 'most_visited_healthcare', 'ms_healthcare', 'pharmaceutical_retailers'],
                'Industrials' : ['aerospace_defense', 'airlines', 'airports_air_services', 'building_products_equipment', 'business_equipment_supplies', 'conglomerates',
 'consulting_services', 'electrical_equipment_parts', 'engineering_construction', 'farm_heavy_construction_machinery', 'high_yield_high_return', 'high_yield_high_return_asia',
 'high_yield_high_return_europe', 'industrial_distribution', 'infrastructure_operations', 'integrated_freight_logistics', 'marine_shipping', 'metal_fabrication',
 'most_visited_industrials', 'ms_industrials', 'pollution_treatment_controls', 'railroads', 'rental_leasing_services', 'security_protection_services', 'specialty_business_services',
 'specialty_industrial_machinery', 'staffing_employment_services', 'tools_accessories', 'trucking', 'waste_management'],
                'Real Estate' : ['high_yield_high_return', 'high_yield_high_return_asia', 'high_yield_high_return_europe', 'most_visited_real_estate', 'ms_real_estate',
 'real_estate_development', 'real_estate_diversified', 'real_estate_services', 'reit_diversified', 'reit_healthcare_facilities', 'reit_hotel_motel', 'reit_industrial',
 'reit_mortgage', 'reit_office', 'reit_residential', 'reit_retail', 'reit_specialty'],
                'Technology' : ['communication_equipment', 'computer_hardware', 'consumer_electronics', 'electronic_components', 'electronics_computer_distribution',
 'growth_technology_stocks', 'high_yield_high_return', 'high_yield_high_return_asia', 'high_yield_high_return_europe', 'information_technology_services', 'most_visited_technology',
 'ms_technology', 'scientific_technical_instruments', 'semiconductor_equipment_materials', 'semiconductors', 'software_application', 'software_infrastructure', 'solar'],
                'Utilities' : ['most_visited_utilities', 'ms_utilities', 'utilities_diversified', 'utilities_independent_power_producers', 'utilities_regulated_electric',
 'utilities_regulated_gas', 'utilities_regulated_water', 'utilities_renewable']}

def show_home_page():

    col1, colm, col2 = st.columns([1,0.5, 1], gap="large")

    with col1 :
        st.markdown(
            """
            <style>
                .welcome-to-quantuminvestpro {
                color: #618fc6;
                text-align: left;
                font-family: "Inter-Bold", sans-serif;
                font-size: 42px;
                font-weight: 700;
                position: absolute;
                left: 10px;
                top: 50px;
                width: 766px;
                height: 78px;
                }
                .navigate-the-markets-with-quantum-precision {
                color: #464646;
                text-align: left;
                font-family: "Inter-ExtraBold", sans-serif;
                font-size: 24px;
                font-weight: 800;
                position: absolute;
                left: 10px;
                top : 100px;
                width: 1106px;
                height: 84px;
                }
                .discover_portfolio{
                color: #000000;
                text-align: left;
                font-family: "Inter-Regular", sans-serif;
                font-size: 18px;
                line-height: 35px;
                font-weight: 400;
                position: absolute;
                left: 10px;
                top: 150px;
                width: 709px;
                height: 231px;
                }
            </style>
            """, 
            unsafe_allow_html=True
        )

        st.markdown("<p class='welcome-to-quantuminvestpro'>Welcome to QuantumInvestPro</p>", unsafe_allow_html=True)
        st.markdown("<p class='navigate-the-markets-with-quantum-precision'>Navigate the markets with Quantum precision</p>", unsafe_allow_html=True)
        st.markdown("""
        <p class='discover_portfolio'>Discover our revolutionary portfolio management platform, reshaping
        investment for everyone. With unparalleled financial and technological
        expertise, we offer personalized and accessible advice to optimize your
        investments. Simplify your financial journey, maximize returns, and
        minimize risks, all with an intuitive user experience. Join us now to
        shape your financial future with confidence.</p>
        """, unsafe_allow_html=True)

    

    # Bouton pour effacer le contenu précédent

    with col2 :
        st.image("man.png")

    col4, col5, col6 = st.columns([0.2, 5, 0.2], gap="large")
    with col5:

        selected2 = option_menu(
            menu_title=None,
            options=["Financial products", "About us", "Contact","Prices"],
            icons=[" ", " ", " ", " ", " "," "],
            orientation="horizontal",
            styles={
            "container": {"background-color": "light-grey","border-radius": "1px;"},
            "nav-link": {"color": "#293133", }, 
            "nav-link-selected": {
                "background-color": "#BCBDBD"
                },

               }
            
            )
        
    if selected2 == "Financial products" :
        various_financial()
    if selected2 == "About us" :
        about_us()
    if selected2 == "Saved PF" :
        view_existing_portfolios()  
    if selected2 == "Log in" :
        sign_in()  
    if selected2 == "Register" :
        Register()  

def various_financial():
    st.markdown(
            """
            <style>
                .crypto{
                color: #000000;
                font-family: "Inter-Bold", sans-serif;
                font-size: 18px;
                line-height: 35px;
                font-weight: 700;
                position: absolute;
                left: 10px;
                top: 50px;
                width: 1335px;
                height: 113px;

                }
                .crypto_def{
                color: #000000;
                text-align: left;
                font-family: "-", sans-serif;
                font-size: 18px;
                line-height: 35px;
                font-weight: 400;
                position: absolute;
                left: 10px;
                top: 60px;
                width: 1335px;
                height: 113px;

                }
                .equity{
                color: #000000;
                font-family: "Inter-Bold", sans-serif;
                font-size: 18px;
                line-height: 35px;
                font-weight: 700;
                position: absolute;
                left: 10px;
                top: 150px;
                width: 1335px;
                height: 113px;
                }

                .equity_def{
                color: #000000;
                text-align: left;
                font-family: "-", sans-serif;
                font-size: 18px;
                line-height: 35px;
                font-weight: 400;
                position: absolute;
                left: 10px;
                top: 160px;
                width: 1335px;
                height: 113px;

                }
                .etf{
                color: #000000;
                font-family: "Inter-Bold", sans-serif;
                font-size: 18px;
                line-height: 35px;
                font-weight: 700;
                position: absolute;
                left: 10px;
                top: 240px;
                width: 1335px;
                height: 113px;
                }

                .etf_def{
                color: #000000;
                text-align: left;
                font-family: "-", sans-serif;
                font-size: 18px;
                line-height: 35px;
                font-weight: 400;
                position: absolute;
                left: 10px;
                top: 250px;
                width: 1335px;
                height: 113px;

                }
                .option{
                color: #000000;
                font-family: "Inter-Bold", sans-serif;
                font-size: 18px;
                line-height: 35px;
                font-weight: 700;
                position: absolute;
                left: 10px;
                top: 340px;
                width: 1335px;
                height: 113px;
                }

                .option_def{
                color: #000000;
                text-align: left;
                font-family: "-", sans-serif;
                font-size: 18px;
                line-height: 35px;
                font-weight: 400;
                position: absolute;
                left: 10px;
                top: 350px;
                width: 1335px;
                height: 113px;

                }
                .mutual_fund{
                color: #000000;
                font-family: "Inter-Bold", sans-serif;
                font-size: 18px;
                line-height: 35px;
                font-weight: 700;
                position: absolute;
                left: 10px;
                top: 460px;
                width: 1335px;
                height: 113px;
                }

                .mutual_fund_def{
                color: #000000;
                text-align: left;
                font-family: "-", sans-serif;
                font-size: 18px;
                line-height: 35px;
                font-weight: 400;
                position: absolute;
                left: 10px;
                top: 470px;
                width: 1335px;
                height: 113px;

                }
            </style>
            """, 
            unsafe_allow_html=True
        )
    st.markdown("<p class='crypto'>Cryptocurrency</p>", unsafe_allow_html=True)
    st.markdown("<p class='crypto_def'>Cryptocurrencies are digital assets based on blockchain technology, offering a decentralized alternative to traditional currencies. They are known for their volatility and high potential returns but also carry significant risks due to their speculative nature and evolving regulations.</p>", unsafe_allow_html=True)
    st.markdown("<p class='equity'>Equity</p>", unsafe_allow_html=True)
    st.markdown("<p class='equity_def'>Equities represent ownership stakes in a publicly traded company. Investors can buy shares to participate in company profits through dividends and share price appreciation. However, stocks can also be subject to market volatility and fluctuations in company performance.</p>", unsafe_allow_html=True)
    st.markdown("<p class='etf'>ETF</p>", unsafe_allow_html=True)
    st.markdown("<p class='etf_def'>ETFs are investment funds traded on stock exchanges like stocks. They offer diversified exposure to a basket of assets, such as stocks, bonds, or commodities, with generally lower management fees compared to traditional mutual funds. ETFs provide investors with increased flexibility and liquidity in the market.</p>", unsafe_allow_html=True)
    st.markdown("<p class='option'>Option</p>", unsafe_allow_html=True)
    st.markdown("<p class='option_def'>Options are contracts that give the buyer the right, but not the obligation, to buy (call option) or sell (put option) an asset at a predetermined price on a future date. Options are widely used for speculation, hedging, or risk management purposes. They can offer investors flexibility and profit opportunities but require a deep understanding of financial markets and investment strategies.</p>", unsafe_allow_html=True)
    st.markdown("<p class='mutual_fund'>Mutual Fund</p>", unsafe_allow_html=True)
    st.markdown("<p class='mutual_fund_def'>Mutual funds are pools of money collected from many investors and managed by professionals. They offer instant diversification by investing in a variety of assets, which can help reduce risk for individual investors. Mutual funds can be used to achieve various financial goals, such as capital growth, income, or capital preservation.</p>", unsafe_allow_html=True)

def about_us():
    st.markdown(
        """
        <style>
            .title{
                color: #464646;
                text-align: left;
                font-family: "Inter-ExtraBold", sans-serif;
                font-size: 20px;
                font-weight: 800;
                position: absolute;
                left: 10px;
                top : 10px;
                width: 1106px;
                height: 84px;
            }
            .text{
                color: #000000;
                text-align: left;
                font-family: "Inter-Regular", sans-serif;
                font-size: 18px;
                line-height: 35px;
                font-weight: 400;
                position: absolute;
                left: 10px;
                top: 70px;
            }
        </style>
        """, 
        unsafe_allow_html=True
        )
    
    st.markdown("<p class='title'>Simplifying investing for everyone</p>", unsafe_allow_html=True)
    st.markdown("<p class='text'>Explore the world of Quantuminvestpro, where investing becomes simple and accessible. You have likely noticed that, despite the rise of investing, it can still be confusing at times. Technical terms, complex charts, and the hustle of financial markets may seem daunting. <br /> <br /> That is why we, Gabriel, PierreAntoine, Chaïma, Anwar, Sonia, and Yohann, decided to take action. In 2024, we created Quantuminvestpro, a clear and transparent platform in the complex world of investing. Our goal? To make investing accessible to everyone, but above all, to make it BETTER for everyone. </br> </br> Quantuminvestpro is more than just a platform; it is your ally, your guide in your financial journey. Whether you want to keep an eye on your investments, discover new opportunities, or connect with a community of like-minded investors, Quantuminvestpro is here to support you wherever you are in your financial adventure. </br> </br> At Quantuminvestpro, we believe in a world where everyone can take control  of their financial future, where investing becomes an enlightening experience rather than an intimidating one. Join us in this quest for clarity and financial success. Your adventure starts here..</p>", unsafe_allow_html=True)
    for i in range(20):
        st.write(" ")


def get_symbols(inst_type, sectors, industry, region, currency, exchange, esg_score):
    
    s = Screener()

    all_screener = s.available_screeners
    
    tri1 = s.get_screeners(all_screener,0)

    tri2 = {}
    for key, elem in tri1.items() :
        if 'criteriaMeta' in tri1[key]:
            if 'quoteType' in tri1[key]['criteriaMeta']:
                
                if tri1[key]['criteriaMeta']['quoteType'] in inst_type:  
                    
                    tri2[key] = elem  


    tri3 = {}
    for key, elem in tri2.items() :
        if 'criteriaMeta' in tri2[key]:
            if 'criteria' in tri2[key]['criteriaMeta']:
                for i in range(len(tri2[key]['criteriaMeta']['criteria'])):
                    if tri2[key]['criteriaMeta']['criteria'][i]['field'] == 'sector':
                        
                        if set(tri2[key]['criteriaMeta']['criteria'][i]['dependentValues']) & set(sector):
                            
                            tri3[key] = elem                      
    
    if industry == []:
        industry = list(tri3.keys())

    filtre = s.get_screeners(industry,5)
    symbols = []

    for ind in industry:
        for i in range(len(filtre[ind]['quotes'])):
            #print(filtre[ind]['quotes'][i]['symbol'], " : ", filtre[ind]['quotes'][i]['shortName'], filtre[ind]['quotes'][i]['region'])
            symbols.append(filtre[ind]['quotes'][i]['symbol'])
    
    #symbols = ["AAPL", "TSLA", "GOOGL"]
    print(symbols)
    return symbols

def create_portfolio():

    st.markdown(
        """
        <style>
            .Create{
                color: #618fc6;
                text-align: left;
                font-family: "Inter-Bold", sans-serif;
                font-size: 42px;
                font-weight: 700;
                position: absolute;
                left: 10px;
                top: 10px;
                width: 766px;
                height: 78px;
            }
            .build{
                color: #464646;
                text-align: left;
                font-family: "Inter-ExtraBold", sans-serif;
                font-size: 24px;
                font-weight: 800;
                position: absolute;
                left: 10px;
                top : 60px;
                width: 1106px;
                height: 84px;
            }
            .stButton>button {
                background-color: #618fc6; /* couleur bleue */
                color: #fff; /* couleur du texte blanc */
                font-weight: bold;
                border : none;
                border-radius: 8px; /* bords arrondis */
                padding: 10px 20px; /* espace à l'intérieur du bouton */
                font-size: 16px;
                cursor: pointer;
            }
            .stButton>button :hover {
                color: white; /* couleur bleue plus foncée au survol */
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<p class='Create'>Create a New Portfolio</p>", unsafe_allow_html=True)
    st.markdown("<p class='build'>Build your financial future with a new portfolio</p>", unsafe_allow_html=True)
    for i in range(8):
        st.write(" ")
    
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Input Fields
    col1, col2 = st.columns([1, 1.2], gap="large")

    # Display portfolio name in the left column
    with col1:       
        portfolio_name = st.text_input("Portfolio Name:")
        budget = st.number_input("Budget:", min_value=0)
        inst_type = st.multiselect("Select asset types:",["Cryptocurrency", "Equity", "ETF", "Mutual Fund", "Option"])
        sectors = st.multiselect("Sector:", ['Basic Materials', 'Communication Services', 'Consumer Cyclical','Consumer Defensive', 'Energy','Financial Services','Healthcare','Industrials','Real Estate','Technology','Utilities'])
        list_industry =[]
        for sector in sectors:
            list_industry.extend(dict_industry[sector])
        industry = st.multiselect('Industry :', list_industry)
        region = st.multiselect('Region :', ['United States','France'])
        currency = st.multiselect('currency : ', ['USD','EUR'])
        exchange = st.multiselect('exchange :', ['NYQ'])
        esg_score = st.number_input('ESG Score', value = 80, min_value = 0, max_value = 100)
        
        try :
            if st.button("Apply filter", key="filter_button"):
                # stock les symbols des actifs filtrés dans session state pour pouvoir les récupérer ailleur
                if 'symboles' not in st.session_state:
                    st.session_state.symbols = get_symbols(inst_type, sectors, industry, region, currency, exchange, esg_score)
        except:
            pass
    with col2:
        
        # dataframe qui permet de séléctionner les actifs un a un 
        df = pd.DataFrame(columns=['Symbols','Compagny name', 'Price', 'Select'])
        try :
            df['Symbols'] = st.session_state.symbols
        except :
            pass
        df['Select'] = True
        df = st.data_editor(df, width = 700, hide_index=True)
        edited_df = df[(df == True).any(axis=1)]
        print(edited_df)
        
        if st.button("Save Portfolio", key="save_button"):
            # ajoute le portefeuille crée à la liste des portefeuilles existants
            conn = st.connection("gsheets", type=GSheetsConnection)
            bdd = conn.read(worksheet="client_ptf").dropna(axis=1, how='all')
            bdd[portfolio_name] = edited_df['Symbols']
            conn.update(worksheet='client_ptf', data=bdd)

            # ajoute le nom du portefeuille nouvelement crée à l'utilisateur connecté
            update_user = conn.read(worksheet="user").dropna(axis=1, how='all')
            update_user.dropna(subset=st.session_state.user['mail'], inplace=True)
            update_user.loc[len(update_user), st.session_state.user['mail']] = portfolio_name
            conn.update(worksheet='user', data=update_user)

def view_existing_portfolios():
    
    col1, col2 = st.columns([0.7, 1], gap="large")
    with col1:
        
        from datetime import datetime

        start = "2019-01-01"    
        end = "2024-01-01"
        nom = "Hi " + st.session_state.user['name']
        st.header(nom)
        ptf_name = st.selectbox('Your portfolio : ', st.session_state.user['ptf_list'])
        
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(worksheet="client_ptf").dropna(axis=1, how='all').dropna(axis=0, how='all')

        assets = list(df[ptf_name].dropna())
        #assets = ['OMC', 'IPG', 'WPP', 'ZD', 'IAS', 'CMPR', 'STGW', 'CRTO', 'MGNI', 'DLX', 'FMX', 'BUD', 'TAP-A', 'TAP']
        print(assets)

        
        # df[portfolio_name]
        data = yf.download(assets, start = start, end = end)  #telecharger les assets de yahoo finance

        returns = data['Adj Close'].pct_change().dropna()

        #we use historical data to predict the future
        hist = True
        methode_mu = 'hist' #mu : la moyenne des données historique, expected return en fonction des données hist
        methode_cov = 'hist'  #calcul de la covariance avec les données historiques
        model = 'Classic'
        rm = 'MV'  #risk model/ risk measure : MV standard deviation : variance / proxi for risk
        obj = 'Sharpe'  #objectif function : maximize the sharpe ratio
        rf = 0  #risk free rate
        l = 0 #risk eversion factor

        #création du portefeuille
        port = rp.Portfolio(returns = returns)
        port.assets_stats(method_mu = methode_mu, method_cov = methode_cov) #calcul de quelques stat sur le portefeuille 
        w = port.optimization(model =  model, rm = rm, obj = obj, rf = rf, l = l, hist = hist)

        #Création de la frontière
        frontier = port.efficient_frontier(model = model, rm = rm, points = 50, rf = rf, hist = hist)
        
        df_display = pd.DataFrame()
        df_display['Symbols'] = df[ptf_name].dropna()

        def obtenir_prix_fermeture(symbole):
            try:
                data = yf.download(symbole)
                prix_cloture = data['Close'].iloc[-1]  # Dernier prix de clôture
                return prix_cloture
            except Exception as e:
                print(f"Erreur lors de la récupération des données pour {symbole}: {e}")
                return None

        # Appliquer la fonction à chaque symbole dans la colonne 'Symbole'
        # df_display['Prix_Fermeture'] = df_display['Symbols'].apply(obtenir_prix_fermeture)
        #df_display = yf.download(df[ptf_name], start="2024-01-01", end="2024-02-01")
        
        #st.header("Your Portfolio : ")
        st.data_editor(df_display, num_rows="fixed", use_container_width=True, hide_index=True)
        
    with col2:
        st.markdown(
            """
            <div style="text-align: center;">
                <h1>Indicators</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

        
        ax7 = rp.plot_table(returns = returns, w = w, MAR = 0, alpha = 0.05)
        st.pyplot(ax7.figure)
        plt.close('all')

        
        st.divider()   #separateur

        '''ax4 = rp.plot_drawdown( returns = returns, w = w, alpha = 0.05, height = 8, width = 10, ax = None)
        st.pyplot(ax4)
        plt.close('all')'''

        ax = rp.plot_series(returns = returns, w = w, cmap = 'tab20', height = 6, width = 10)
        st.pyplot(ax.figure)
        plt.close('all')

        st.divider()   #separateur
        
        ax2 = rp.plot_frontier(w_frontier = frontier, mu = port.mu, cov = port.cov, returns = returns, rm = rm, height = 6, width = 10, rf = rf, cmap = 'viridis', w = w)
        st.pyplot(ax2.figure)
        plt.close('all')

        st.divider()

        ax3 = rp.plot_pie(w=w, title = "Optimum Portfolio", others = 0.05, cmap = 'tab20', height = 6, width = 10)
        st.pyplot(ax3.figure)
        plt.close('all')

        st.divider()
        
        ax5 = rp.plot_frontier_area(w_frontier = frontier, cmap = 'tab20')
        st.pyplot(ax5.figure)
        plt.close('all')

        ax6 = rp.plot_hist(returns = returns, w = w, alpha = 0.05, bins = 50, height = 6, width = 10, ax = None)
        st.pyplot(ax6.figure)
        plt.close('all')

def sign_in():
    
    st.markdown(
            """
            <style>
                /* Changer la couleur du bouton */

            .element-container:has(#button-after) + div button {
                        background-color: #618FC6;
                        color: white;
                        font-weight: bold;
                        display: block;
                        margin: auto;
                        width : 45%;
            }
            .element-container:has(#login-button) + div button {
                        background-color: none;
                        color: lightgray;
                        font-style: italic;
                        border: none;
                        display: block;
                        margin: auto;
                        
            }
            .element-container:has(#not-register) + div button {
                        background-color: none;
                        color: black;
                        border: none;
                        display: block;
                        margin: auto;
                        text-decoration: underline;
            }
            </style>
            """, 
            unsafe_allow_html=True
            )
    
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        
        col6, col7, col8 = st.columns([0.60, 3, 0.60], gap="large")
        
        with col7: 
           
            placeholder = st.empty()


            # Insert a form in the container
            with placeholder.form("login"):
                st.write(" ")
                st.write(" ")
                current_mail = st.text_input("Email")
                st.write(" ")
                st.write(" ")
                current_password = st.text_input("Password", type="password")
                st.write(" ")
                st.write(" ")
                st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)
                submit = st.form_submit_button("Login")
                st.markdown('<span id="login-button"></span>', unsafe_allow_html=True)
                st.form_submit_button("*Forgot password ?*")
            
            st.markdown('<span id="not-register"></span>', unsafe_allow_html=True)
            st.button("Not registered yet ? _Sign up_")

        conn = st.connection("gsheets", type=GSheetsConnection)
        user_data = conn.read(worksheet="user").dropna(axis=1, how='all')
        #st.write(user_data)
        try:
            name = user_data.at[0, current_mail]
            ptf_list = user_data[current_mail][3:].dropna(axis=0, how='all')
        
            if submit:
                current_user = {'mail' : current_mail,
                                'name' : name,
                                'password' : current_password,
                                'ptf_list' : ptf_list,
                                'signed_in' : True}
            # stock les paramètres de l'utilisateur dans session state pour pouvoir les utiliser ailleur
            if 'user' not in st.session_state:
                st.session_state.user = current_user

            st.write(name)
        except Exception:
            pass
        #st.write(st.session_state.user)
    with col2:
        
        for i in range(10):
            st.write(" ")
        st.markdown(
            """
            <style>
                .login {
                color: #618fc6;
                text-align: left;
                font-family: "Inter-Bold", sans-serif;
                font-size: 42px;
                font-weight: 700;
                position: absolute;
                width: 766px;
                height: 78px;
                left : 10 px;
                }
            </style>
            """, 
            unsafe_allow_html=True
        )
        st.markdown("<p class='login'>Nice to see you again !</p>", unsafe_allow_html=True)

def Register():
    st.markdown(
        """
        <style>
            /* Changer la couleur du bouton */

        .element-container:has(#register) + div button {
                    background-color: #618FC6;
                    color: white;
                    font-weight: bold;
                    display: block;
                    margin: auto;
                    width : 45%;
        }
        .element-container:has(#not-register) + div button {
                    background-color: none;
                    color: black;
                    border: none;
                    display: block;
                    margin: auto;
                    text-decoration: underline;
        }
        </style>
        """, 
        unsafe_allow_html=True
        )
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        for i in range(8):
            st.write(" ")
        st.markdown(
            """
            <style>
                .register-title {
                color: #618fc6;
                text-align: left;
                font-family: "Inter-Bold", sans-serif;
                font-size: 42px;
                font-weight: 700;
                position: absolute;
                width: 766px;
                height: auto;
                left : 10 px;
                }
                .register {
                color: #464646;
                text-align: left;
                font-family: "Inter-ExtraBold", sans-serif;
                font-size: 20px;
                font-weight: 800;
                position: absolute;
                left: 10px;
                top : 100px;
                width: 1000px;
                height: 84px;
                }
            </style>
            """, 
            unsafe_allow_html=True
        )
        st.markdown("<p class='register-title'>Join the financial revolution, </br> sign up now !</p>", unsafe_allow_html=True)
        st.markdown("<p class='register'>Bengin your financial adventure here.</p>", unsafe_allow_html=True)
            
    with col2:
        for i in range(4):
            st.write(" ")
        placeholder = st.empty()

        # Insert a form in the container
        with placeholder.form("register"):
            c1,c2 = st.columns(2)
                    
            with c1:
                first_name = st.text_input("First Name")
            with c2:
                last_name = st.text_input("Last Name")
            
            mail = st.text_input("e-mail")

            Password = st.text_input("Password", type="password")

            st.markdown('<span id="register"></span>', unsafe_allow_html=True)
            submit = st.form_submit_button("Register")
            
        st.markdown('<span id="not-register"></span>', unsafe_allow_html=True)
        st.button("Already have an account ? _Login_")



        new_data = pd.Series([first_name, last_name, Password])
        user_data = pd.DataFrame()
        
        conn = st.connection("gsheets", type=GSheetsConnection)
        user_data = conn.read(worksheet="user").dropna(axis=1, how='all')
        print(user_data)
    
        if submit:
            user_data[mail] = new_data.reindex(new_data.index)
            conn.update(worksheet="user", data=user_data)
            st.success("Registration done")
            print(conn.read(worksheet="user").dropna(axis=1, how='all'))

def main():
    
    st.set_page_config(layout="wide", )
    # Custom Styling
    #set_custom_style()

    col3, col4 = st.columns([0.5, 1.5],)

    with col3 :
        st.image("logo.jpg")

    with col4 :
        selected = option_menu(
        menu_title=None,
        options=["Home", "Create", "Saved PF","---", "Log in", "Register"],
        icons=[" ", " ", " ", " ", " "," "],
        orientation="horizontal",
        styles={
            "container": {"background-color": "#618FC6","border-radius": "1px;"},
            "nav-link": {"color": "white", }, 
            "nav-link-selected": {
                "background-color": "#618FC6"
                },

               }
        )

        
    
        
    #F0C300
    if selected == "Home" :
         show_home_page()
    if selected == "Create" :
        create_portfolio()
    if selected == "Saved PF" :
        view_existing_portfolios()  
    if selected == "Log in" :
        sign_in()  
    if selected == "Register" :
        Register()  

if __name__ == "__main__":
    main()