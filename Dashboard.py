# dashboard_shady_records.py
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
from datetime import datetime
import warnings
import base64
import io
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="ANALYSE STRATÉGIQUE - SHADY RECORDS",
    page_icon="👻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avec thème Shady (noir, vert, argent)
st.markdown("""
<style>
    .main {
        color: #ffffff !important;
        background-color: #000000 !important;
    }
    
    .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    
    .main-header {
        font-size: 3rem;
        color: #00FF00 !important;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        border-bottom: 3px solid #00FF00;
        padding-bottom: 1rem;
        text-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
        background: linear-gradient(90deg, #000000, #003300, #000000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Courier New', monospace;
    }
    
    .academic-card {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        border: 1px solid #444444;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0, 255, 0, 0.1);
        color: #ffffff !important;
        transition: all 0.3s ease;
    }
    
    .academic-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 255, 0, 0.3);
        border-color: #00FF00;
    }
    
    .eminem-card { 
        border-left: 5px solid #00FF00; 
        background: linear-gradient(135deg, #0a1a0a 0%, #1a2d1a 100%);
    }
    .fifty-card { 
        border-left: 5px solid #FF4500; 
        background: linear-gradient(135deg, #1a0a0a 0%, #2d1a1a 100%);
    }
    .obietrice-card { 
        border-left: 5px solid #9370DB; 
        background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2d 100%);
    }
    .cashis-card { 
        border-left: 5px solid #FFD700; 
        background: linear-gradient(135deg, #1a1a0a 0%, #2d2d1a 100%);
    }
    .yellawolf-card { 
        border-left: 5px solid #FF69B4; 
        background: linear-gradient(135deg, #1a0a1a 0%, #2d1a2d 100%);
    }
    .slaughterhouse-card { 
        border-left: 5px solid #C0C0C0; 
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #00FF00 !important;
        margin: 0.5rem 0;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
        font-family: 'Courier New', monospace;
    }
    
    .section-title {
        color: #ffffff !important;
        border-bottom: 2px solid #00FF00;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
        font-size: 1.6rem;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.2);
        font-family: 'Courier New', monospace;
    }
    
    .subsection-title {
        color: #ffffff !important;
        border-left: 4px solid #00FF00;
        padding-left: 1rem;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        font-family: 'Courier New', monospace;
    }
    
    .stMarkdown {
        color: #ffffff !important;
    }
    
    p, div, span, h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    .secondary-text {
        color: #cccccc !important;
    }
    
    .light-text {
        color: #999999 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #0a0a0a;
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1a1a1a;
        border-radius: 5px;
        color: #ffffff !important;
        font-weight: 500;
        border: 1px solid #444444;
        transition: all 0.3s ease;
        font-family: 'Courier New', monospace;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2d2d2d;
        border-color: #00FF00;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #00FF00 !important;
        color: #000000 !important;
        font-weight: 600;
        border-color: #00FF00;
    }
    
    .card-content {
        color: #ffffff !important;
    }
    
    .card-secondary {
        color: #cccccc !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00FF00 0%, #00CC00 100%);
        color: #000000;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 255, 0, 0.3);
        font-family: 'Courier New', monospace;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #33FF33 0%, #00FF00 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 255, 0, 0.5);
    }
    
    .stDataFrame {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    
    .stSelectbox > div > div {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    .stSlider > div > div > div {
        background-color: #00FF00;
    }
    
    /* Style pour les graphiques Plotly */
    .js-plotly-plot .plotly .modebar {
        background-color: rgba(10, 10, 10, 0.8) !important;
    }
    
    .js-plotly-plot .plotly .modebar-btn {
        background-color: transparent !important;
        color: #ffffff !important;
    }
    
    /* Shady Records Badge */
    .shady-badge {
        display: inline-block;
        background: #000000;
        color: #00FF00;
        padding: 5px 15px;
        border-radius: 20px;
        border: 2px solid #00FF00;
        font-weight: bold;
        font-size: 0.9rem;
        margin: 0 5px 10px 0;
        font-family: 'Courier New', monospace;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #444444;
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555555;
    }
    
    /* Matrix effect for header */
    .matrix-text {
        position: relative;
        overflow: hidden;
        background: linear-gradient(to bottom, #000000, #001100);
    }
    
    /* Typography */
    .monospace {
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

class ShadyAnalyzer:
    def __init__(self):
        # Définition de la palette de couleurs pour Shady Records
        self.color_palette = {
            'EMINEM': '#00FF00',        # Vert néon
            '50 CENT': '#FF4500',       # Orange rougeâtre
            'OBIE TRICE': '#9370DB',    # Violet
            'CASHIS': '#FFD700',        # Or
            'YELAWOLF': '#FF69B4',      # Rose vif
            'SLAUGHTERHOUSE': '#C0C0C0',# Argent
            'D12': '#4169E1',           # Bleu royal
            'Période Classique': '#00FF00',
            'Période Moderne': '#FF4500'
        }
        
        # Couleurs pour les types de données
        self.data_colors = {
            'Ventes': '#00FF00',
            'Albums': '#FF4500',
            'Artistes': '#9370DB',
            'Revenus': '#FFD700',
            'Croissance': '#FF69B4'
        }
        
        self.initialize_data()
        
    def initialize_data(self):
        """Initialise les données complètes sur Shady Records"""
        
        # Données principales sur le label
        self.label_data = {
            'fondation': 1999,
            'fondateur': 'Eminem, Paul Rosenberg',
            'statut': 'Label indépendant (filiale de Interscope/Universal)',
            'siege': 'Detroit, Michigan, USA',
            'specialisation': 'Hip-hop, Rap hardcore, Horrorcore',
            'philosophie': "Raw talent, lyrical prowess, no compromise",
            'distribution': 'Interscope Records, Universal Music Group'
        }

        # Données des artistes principaux
        self.artists_data = {
            'EMINEM': {
                'debut': 1999,
                'genre': 'Hip-hop, Horrorcore, Rap hardcore',
                'albums_shady': 11,
                'ventes_totales': 220000000,
                'succes_principal': 'The Marshall Mathers LP (2000)',
                'statut': 'Fondateur et artiste phare',
                'impact': 'Artiste le plus vendu des années 2000',
                'annees_activite': '1999-présent',
                'albums_principaux': ['The Marshall Mathers LP', 'The Eminem Show', 'Recovery'],
                'chiffre_affaires_estime': 500000000,
                'public_cible': 'Global, toutes générations',
                'tournees': 'Mondiales'
            },
            '50 CENT': {
                'debut': 2002,
                'genre': 'Hip-hop, Gangsta rap',
                'albums_shady': 2,
                'ventes_totales': 30000000,
                'succes_principal': 'Get Rich or Die Tryin\' (2003)',
                'statut': 'Artiste à succès phénoménal',
                'impact': 'Icône du rap commercial',
                'annees_activite': '2002-2014',
                'albums_principaux': ['Get Rich or Die Tryin\'', 'The Massacre'],
                'chiffre_affaires_estime': 150000000,
                'public_cible': 'Mainstream, urbain',
                'tournees': 'Mondiales'
            },
            'OBIE TRICE': {
                'debut': 2003,
                'genre': 'Hip-hop, Rap hardcore',
                'albums_shady': 3,
                'ventes_totales': 2000000,
                'succes_principal': 'Cheers (2003)',
                'statut': 'Artiste découvert par Eminem',
                'impact': 'Représentant du son Detroit',
                'annees_activite': '2003-2008',
                'albums_principaux': ['Cheers', 'Second Round\'s on Me'],
                'chiffre_affaires_estime': 10000000,
                'public_cible': 'Hip-hop pur, Detroit',
                'tournees': 'Nationales'
            },
            'CASHIS': {
                'debut': 2006,
                'genre': 'Hip-hop, Gangsta rap',
                'albums_shady': 1,
                'ventes_totales': 500000,
                'succes_principal': 'The County Hound EP (2006)',
                'statut': 'Artiste signé via G-Unit',
                'impact': 'Style West Coast influent',
                'annees_activite': '2006-2009',
                'albums_principaux': ['The County Hound EP', 'Loose Cannon'],
                'chiffre_affaires_estime': 3000000,
                'public_cible': 'Fans de G-Unit, West Coast',
                'tournees': 'Régionales'
            },
            'YELAWOLF': {
                'debut': 2011,
                'genre': 'Hip-hop, Country rap',
                'albums_shady': 2,
                'ventes_totales': 1000000,
                'succes_principal': 'Radioactive (2011)',
                'statut': 'Artiste éclectique',
                'impact': 'Fusion hip-hop/country',
                'annees_activite': '2011-2019',
                'albums_principaux': ['Radioactive', 'Love Story'],
                'chiffre_affaires_estime': 8000000,
                'public_cible': 'Alternative, rock/rap fusion',
                'tournees': 'Nationales'
            },
            'SLAUGHTERHOUSE': {
                'debut': 2009,
                'genre': 'Hip-hop, Rap technique',
                'albums_shady': 1,
                'ventes_totales': 800000,
                'succes_principal': 'Welcome to: Our House (2012)',
                'statut': 'Supergroupe lyrique',
                'impact': 'Renaissance du rap technique',
                'annees_activite': '2009-2015',
                'albums_principaux': ['Welcome to: Our House'],
                'chiffre_affaires_estime': 5000000,
                'public_cible': 'Puristes, fans de rap technique',
                'tournees': 'Nationales'
            },
            'D12': {
                'debut': 2001,
                'genre': 'Hip-hop, Horrorcore',
                'albums_shady': 2,
                'ventes_totales': 6000000,
                'succes_principal': 'Devil\'s Night (2001)',
                'statut': "Groupe d'Eminem",
                'impact': 'Humoristique/horrorcore',
                'annees_activite': '2001-2008',
                'albums_principaux': ['Devil\'s Night', 'D12 World'],
                'chiffre_affaires_estime': 30000000,
                'public_cible': 'Fans d\'Eminem, humoristique',
                'tournees': 'Mondiales'
            }
        }

        # Données chronologiques détaillées
        self.timeline_data = [
            {'annee': 1999, 'evenement': 'Fondation par Eminem et Paul Rosenberg', 'type': 'Structure', 'importance': 10},
            {'annee': 2000, 'evenement': 'Sortie de The Marshall Mathers LP (Eminem)', 'type': 'Album', 'importance': 10},
            {'annee': 2001, 'evenement': 'Sortie de Devil\'s Night (D12)', 'type': 'Album', 'importance': 8},
            {'annee': 2002, 'evenement': 'Signature de 50 Cent', 'type': 'Artiste', 'importance': 9},
            {'annee': 2003, 'evenement': 'Sortie de Get Rich or Die Tryin\' (50 Cent)', 'type': 'Album', 'importance': 10},
            {'annee': 2003, 'evenement': 'Sortie de Cheers (Obie Trice)', 'type': 'Album', 'importance': 7},
            {'annee': 2004, 'evenement': 'Lancement de G-Unit Records (sous-label)', 'type': 'Business', 'importance': 8},
            {'annee': 2009, 'evenement': 'Signature de Slaughterhouse', 'type': 'Artiste', 'importance': 7},
            {'annee': 2011, 'evenement': 'Signature de Yelawolf', 'type': 'Artiste', 'importance': 7},
            {'annee': 2012, 'evenement': 'Sortie de Welcome to: Our House (Slaughterhouse)', 'type': 'Album', 'importance': 7},
            {'annee': 2014, 'evenement': 'Départ de 50 Cent du label', 'type': 'Structure', 'importance': 8},
            {'annee': 2017, 'evenement': 'Shady Records XV (15 ans d\'anniversaire)', 'type': 'Événement', 'importance': 6},
            {'annee': 2020, 'evenement': 'Sortie de Music to Be Murdered By (Eminem)', 'type': 'Album', 'importance': 8},
            {'annee': 2022, 'evenement': 'Curry & The Shady Cuts (compilation)', 'type': 'Album', 'importance': 5}
        ]

        # Données financières et commerciales
        self.financial_data = {
            'EMINEM': {
                'ventes_albums': 220000000,
                'chiffre_affaires': 500000000,
                'rentabilite': 95,
                'cout_production_moyen': 2000000,
                'budget_marketing_moyen': 8000000,
                'roi': 1200
            },
            '50 CENT': {
                'ventes_albums': 30000000,
                'chiffre_affaires': 150000000,
                'rentabilite': 90,
                'cout_production_moyen': 1000000,
                'budget_marketing_moyen': 5000000,
                'roi': 1000
            },
            'OBIE TRICE': {
                'ventes_albums': 2000000,
                'chiffre_affaires': 10000000,
                'rentabilite': 70,
                'cout_production_moyen': 250000,
                'budget_marketing_moyen': 1000000,
                'roi': 300
            },
            'CASHIS': {
                'ventes_albums': 500000,
                'chiffre_affaires': 3000000,
                'rentabilite': 60,
                'cout_production_moyen': 150000,
                'budget_marketing_moyen': 500000,
                'roi': 200
            },
            'YELAWOLF': {
                'ventes_albums': 1000000,
                'chiffre_affaires': 8000000,
                'rentabilite': 65,
                'cout_production_moyen': 300000,
                'budget_marketing_moyen': 800000,
                'roi': 250
            },
            'SLAUGHTERHOUSE': {
                'ventes_albums': 800000,
                'chiffre_affaires': 5000000,
                'rentabilite': 68,
                'cout_production_moyen': 400000,
                'budget_marketing_moyen': 600000,
                'roi': 220
            },
            'D12': {
                'ventes_albums': 6000000,
                'chiffre_affaires': 30000000,
                'rentabilite': 75,
                'cout_production_moyen': 500000,
                'budget_marketing_moyen': 2000000,
                'roi': 400
            }
        }

        # Données de stratégie marketing
        self.marketing_data = {
            'EMINEM': {
                'strategie': 'Controverses maîtrisées, storytelling intense',
                'cibles': 'Global, adolescents rebelles, toutes générations',
                'canaux': ['MTV', 'Radio mondiale', 'Films', 'Réseaux sociaux'],
                'budget_ratio': 30,
                'succes': 'Légendaire',
                'innovations': 'Marketing de personnalité complexe'
            },
            '50 CENT': {
                'strategie': 'Image de bad boy entrepreneur, viral marketing',
                'cibles': 'Mainstream, aspirants entrepreneurs',
                'canaux': ['Mixtapes gratuites', 'Événements', 'Business ventures'],
                'budget_ratio': 25,
                'succes': 'Exceptionnel',
                'innovations': 'Marketing street-to-boardroom'
            },
            'OBIE TRICE': {
                'strategie': 'Authenticité Detroit, rap raw',
                'cibles': 'Hip-hop pur, fans de Detroit',
                'canaux': ['Mixtapes', 'Concerts locaux', 'Collaborations'],
                'budget_ratio': 18,
                'succes': 'Correct',
                'innovations': 'Marketing de fidélité locale'
            },
            'CASHIS': {
                'strategie': 'Association G-Unit, rap gangsta',
                'cibles': 'Fans de 50 Cent, West Coast',
                'canaux': ['Mixtapes G-Unit', 'Radio locale', 'Features'],
                'budget_ratio': 15,
                'succes': 'Modéré',
                'innovations': 'Marketing par affiliation'
            },
            'YELAWOLF': {
                'strategie': 'Image d\'artiste éclectique, fusion country/rap',
                'cibles': 'Alternative, rock/rap fusion',
                'canaux': ['Festivals', 'Radio alternative', 'YouTube'],
                'budget_ratio': 20,
                'succes': 'Bon',
                'innovations': 'Marketing crossover genre'
            },
            'SLAUGHTERHOUSE': {
                'strategie': 'Rap technique pur, élitisme lyrique',
                'cibles': 'Puristes, fans de rap technique',
                'canaux': ['Battles rap', 'Radio underground', 'Internet'],
                'budget_ratio': 22,
                'succes': 'Bon',
                'innovations': 'Marketing niche élitiste'
            },
            'D12': {
                'strategie': 'Humoristique noir, horrorcore',
                'cibles': 'Fans d\'Eminem, humour provocateur',
                'canaux': ['Sketches comiques', 'MTV', 'Features Eminem'],
                'budget_ratio': 20,
                'succes': 'Très bon',
                'innovations': 'Marketing comique dark'
            }
        }

        # Données de production
        self.production_data = {
            'EMINEM': {
                'albums_produits': 11,
                'duree_contrat': 25,
                'rythme_sorties': '2-3 ans',
                'qualite_production': 10,
                'autonomie_artistique': 9,
                'support_label': 10
            },
            '50 CENT': {
                'albums_produits': 2,
                'duree_contrat': 12,
                'rythme_sorties': '2 ans',
                'qualite_production': 9,
                'autonomie_artistique': 8,
                'support_label': 9
            },
            'OBIE TRICE': {
                'albums_produits': 3,
                'duree_contrat': 5,
                'rythme_sorties': '2.5 ans',
                'qualite_production': 7,
                'autonomie_artistique': 7,
                'support_label': 7
            },
            'CASHIS': {
                'albums_produits': 1,
                'duree_contrat': 3,
                'rythme_sorties': '3 ans',
                'qualite_production': 6,
                'autonomie_artistique': 6,
                'support_label': 6
            },
            'YELAWOLF': {
                'albums_produits': 2,
                'duree_contrat': 8,
                'rythme_sorties': '4 ans',
                'qualite_production': 8,
                'autonomie_artistique': 8,
                'support_label': 8
            },
            'SLAUGHTERHOUSE': {
                'albums_produits': 1,
                'duree_contrat': 6,
                'rythme_sorties': '6 ans',
                'qualite_production': 8,
                'autonomie_artistique': 7,
                'support_label': 7
            },
            'D12': {
                'albums_produits': 2,
                'duree_contrat': 7,
                'rythme_sorties': '3.5 ans',
                'qualite_production': 8,
                'autonomie_artistique': 7,
                'support_label': 8
            }
        }

        # Données de gestion et management
        self.management_data = {
            'structure': {
                'type': 'Label indépendant avec backing major',
                'effectif': 35,
                'departements': ['A&R', 'Production', 'Marketing', 'Commercial', 'Legal', 'Digital'],
                'processus_decision': 'Collaboratif (Eminem/Paul Rosenberg)',
                'culture_entreprise': 'Loyalty, talent first, creative freedom'
            },
            'ressources_humaines': {
                'turnover': 'Faible',
                'expertise': 'Production hip-hop, management artistique',
                'reseautage': 'Industrie mondiale',
                'formation': 'Mentorat par Eminem'
            },
            'finances': {
                'model_economique': 'Artist development, long-term investments',
                'marge_nette': '20-25%',
                'investissement_artistes': 'Long terme, développement',
                'risque': 'Modéré'
            },
            'relations_artistes': {
                'approche': 'Familiale, développement artistique',
                'contrats': 'Artist-friendly',
                'communication': 'Directe, honnête',
                'loyaute': 'Très forte (Shady Family)'
            }
        }

    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">👻 SHADY RECORDS - DASHBOARD STRATÉGIQUE</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #cccccc; font-size: 1.2rem; margin-bottom: 2rem; font-family: Courier New, monospace;">Label de hip-hop américain - Analyse complète 1999-2024</p>', unsafe_allow_html=True)
        
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_ventes = sum(self.financial_data[artist]['ventes_albums'] for artist in self.financial_data)
            st.markdown(f"""
            <div class="academic-card eminem-card">
                <div style="color: {self.color_palette['EMINEM']}; font-size: 1rem; font-weight: 600; text-align: center;">📀 VENTES TOTALES</div>
                <div class="metric-value" style="color: {self.color_palette['EMINEM']}; text-align: center;">{total_ventes/1000000:.0f}M</div>
                <div style="color: #cccccc; text-align: center;">Albums vendus mondialement</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_artistes = len(self.artists_data)
            st.markdown(f"""
            <div class="academic-card fifty-card">
                <div style="color: {self.color_palette['50 CENT']}; font-size: 1rem; font-weight: 600; text-align: center;">🎤 ARTISTES</div>
                <div class="metric-value" style="color: {self.color_palette['50 CENT']}; text-align: center;">{total_artistes}</div>
                <div style="color: #cccccc; text-align: center;">Artistes principaux</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_albums = sum(self.artists_data[artist]['albums_shady'] for artist in self.artists_data)
            st.markdown(f"""
            <div class="academic-card obietrice-card">
                <div style="color: {self.color_palette['OBIE TRICE']}; font-size: 1rem; font-weight: 600; text-align: center;">💿 ALBUMS</div>
                <div class="metric-value" style="color: {self.color_palette['OBIE TRICE']}; text-align: center;">{total_albums}</div>
                <div style="color: #cccccc; text-align: center;">Produits par le label</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            chiffre_affaires_total = sum(self.financial_data[artist]['chiffre_affaires'] for artist in self.financial_data)
            st.markdown(f"""
            <div class="academic-card cashis-card">
                <div style="color: {self.color_palette['CASHIS']}; font-size: 1rem; font-weight: 600; text-align: center;">💰 CHIFFRE D'AFFAIRES</div>
                <div class="metric-value" style="color: {self.color_palette['CASHIS']}; text-align: center;">{chiffre_affaires_total/1000000:.0f}M$</div>
                <div style="color: #cccccc; text-align: center;">Estimé sur la période</div>
            </div>
            """, unsafe_allow_html=True)

    def create_artist_analysis(self):
        """Analyse complète des artistes"""
        st.markdown('<h3 class="section-title">🎤 ANALYSE DU PORTFOLIO ARTISTES</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📊 Performance Commerciale</div>', unsafe_allow_html=True)
            self.create_sales_comparison_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">📈 Rentabilité par Artiste</div>', unsafe_allow_html=True)
            self.create_roi_chart()
        
        # Analyse détaillée par artiste
        st.markdown('<div class="subsection-title">🔍 Analyse Détailée par Artiste</div>', unsafe_allow_html=True)
        self.create_detailed_artist_analysis()

    def create_sales_comparison_chart(self):
        """Graphique de comparaison des ventes"""
        artists = list(self.artists_data.keys())
        ventes = [self.financial_data[artist]['ventes_albums'] for artist in artists]
        
        # Convertir en millions pour meilleure lisibilité
        ventes_millions = [v/1000000 for v in ventes]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=artists,
            y=ventes_millions,
            marker_color=[self.color_palette[artist] for artist in artists],
            text=[f"{v:.0f}M" for v in ventes_millions],
            textposition='auto',
            textfont=dict(color='white', size=14, weight='bold')
        ))
        
        fig.update_layout(
            title='Ventes Totalisées par Artiste (en millions)',
            xaxis_title='Artistes',
            yaxis_title="Albums vendus (millions)",
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_roi_chart(self):
        """Graphique du retour sur investissement"""
        artists = list(self.financial_data.keys())
        roi = [self.financial_data[artist]['roi'] for artist in artists]
        rentabilite = [self.financial_data[artist]['rentabilite'] for artist in artists]
        
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[roi[i]],
                y=[rentabilite[i]],
                mode='markers+text',
                marker=dict(
                    size=80, 
                    color=self.color_palette[artist], 
                    opacity=0.9,
                    line=dict(width=3, color='#ffffff')
                ),
                text=[artist],
                textposition="middle center",
                textfont=dict(color='white', size=12, weight='bold'),
                name=artist,
                showlegend=True
            ))
        
        fig.update_layout(
            title='ROI vs Rentabilité',
            xaxis_title='Retour sur Investissement (%)',
            yaxis_title='Taux de Rentabilité (%)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#00FF00',
                borderwidth=1,
                font=dict(color='white', size=10)
            ),
            xaxis=dict(range=[150, 1300], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[55, 100], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_detailed_artist_analysis(self):
        """Analyse détaillée par artiste"""
        artists = list(self.artists_data.keys())
        tabs = st.tabs(artists)
        
        for i, artist in enumerate(artists):
            with tabs[i]:
                couleur = self.color_palette[artist]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Informations générales
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {couleur}20 0%, {couleur}05 100%); padding: 1rem; border-radius: 8px; border-left: 5px solid {couleur}; margin-bottom: 1rem;">
                        <div style="color: {couleur}; font-weight: bold; font-size: 1.5rem; margin-bottom: 0.5rem;">{artist}</div>
                        <div style="color: #cccccc; font-size: 1.1rem; font-weight: 500;">{self.artists_data[artist]['genre']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Métriques clés
                    st.metric("Albums chez Shady", self.artists_data[artist]['albums_shady'])
                    st.metric("Ventes totales", f"{self.financial_data[artist]['ventes_albums']/1000000:.1f}M")
                    st.metric("Chiffre d'affaires", f"{self.financial_data[artist]['chiffre_affaires']/1000000:.1f}M$")
                    
                    # Succès principal
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Succès Principal:</div>
                        <div style="color: #ffffff; font-style: italic; font-size: 1.1rem;">{self.artists_data[artist]['succes_principal']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Caractéristiques commerciales
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Performance Commerciale:</div>
                        <ul style="color: #ffffff; font-weight: 500;">
                            <li>Rentabilité: {self.financial_data[artist]['rentabilite']}%</li>
                            <li>ROI: {self.financial_data[artist]['roi']}%</li>
                            <li>Coût production moyen: {self.financial_data[artist]['cout_production_moyen']/1000:.0f}k$</li>
                            <li>Budget marketing moyen: {self.financial_data[artist]['budget_marketing_moyen']/1000:.0f}k$</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Graphique radar des caractéristiques
                    categories = ['Ventes', 'Rentabilité', 'ROI', 'Impact']
                    valeurs = [
                        min(100, self.financial_data[artist]['ventes_albums'] / 2200000),  # Normalisé par rapport à Eminem
                        self.financial_data[artist]['rentabilite'],
                        min(100, self.financial_data[artist]['roi'] / 13),  # Normalisé
                        100 if self.artists_data[artist]['impact'] in ['Artiste le plus vendu', 'Icône du rap commercial'] else 
                        85 if self.artists_data[artist]['impact'] in ['Renaissance rap technique', 'Fusion hip-hop/country'] else
                        70
                    ]
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatterpolar(
                        r=valeurs + [valeurs[0]],
                        theta=categories + [categories[0]],
                        fill='toself',
                        line=dict(color=couleur, width=3),
                        marker=dict(size=8, color=couleur),
                        name=artist
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            bgcolor='#1a1a1a',
                            radialaxis=dict(
                                visible=True, 
                                range=[0, 100],
                                gridcolor='#333333',
                                tickfont=dict(color='#ffffff', size=12),
                                linecolor='#444444'
                            ),
                            angularaxis=dict(
                                gridcolor='#333333',
                                tickfont=dict(color='#ffffff', size=12),
                                linecolor='#444444'
                            )
                        ),
                        paper_bgcolor='#0a0a0a',
                        font=dict(color='#ffffff', size=14),
                        showlegend=False,
                        height=300,
                        title=f"Profil de Performance - {artist}"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)

    def create_production_analysis(self):
        """Analyse de la production"""
        st.markdown('<h3 class="section-title">🏭 ANALYSE DE LA PRODUCTION</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📅 Cycles de Production</div>', unsafe_allow_html=True)
            self.create_production_timeline()
        
        with col2:
            st.markdown('<div class="subsection-title">⚙️ Qualité et Support</div>', unsafe_allow_html=True)
            self.create_quality_support_chart()
        
        # Analyse des coûts
        st.markdown('<div class="subsection-title">💰 Analyse des Coûts de Production</div>', unsafe_allow_html=True)
        self.create_cost_analysis()

    def create_production_timeline(self):
        """Timeline de la production"""
        artists = list(self.production_data.keys())
        durees = [self.production_data[artist]['duree_contrat'] for artist in artists]
        albums = [self.production_data[artist]['albums_produits'] for artist in artists]
        
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[durees[i]],
                y=[albums[i]],
                mode='markers+text',
                marker=dict(
                    size=60, 
                    color=self.color_palette[artist], 
                    opacity=0.9,
                    line=dict(width=2, color='#ffffff')
                ),
                text=[artist],
                textposition="middle center",
                textfont=dict(color='white', size=10, weight='bold'),
                name=artist
            ))
        
        fig.update_layout(
            title='Durée des Contrats vs Nombre d\'Albums',
            xaxis_title='Durée du contrat (années)',
            yaxis_title="Nombre d'albums produits",
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_quality_support_chart(self):
        """Graphique qualité vs support"""
        artists = list(self.production_data.keys())
        qualite = [self.production_data[artist]['qualite_production'] for artist in artists]
        support = [self.production_data[artist]['support_label'] for artist in artists]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=qualite,
            y=support,
            mode='markers+text',
            marker=dict(
                size=60,
                color=[self.color_palette[artist] for artist in artists],
                opacity=0.9
            ),
            text=artists,
            textposition="top center",
            textfont=dict(color='white', size=10, weight='bold')
        ))
        
        fig.update_layout(
            title='Qualité de Production vs Support du Label',
            xaxis_title='Qualité de Production (1-10)',
            yaxis_title='Support du Label (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(range=[5, 10.5], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[5, 10.5], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_cost_analysis(self):
        """Analyse des coûts de production"""
        artists = list(self.financial_data.keys())
        couts_production = [self.financial_data[artist]['cout_production_moyen'] for artist in artists]
        budgets_marketing = [self.financial_data[artist]['budget_marketing_moyen'] for artist in artists]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Coût Production',
            x=artists,
            y=couts_production,
            marker_color='#00FF00',
            text=[f"{v/1000:.0f}k$" for v in couts_production],
            textposition='auto',
            textfont=dict(color='white', size=10, weight='bold')
        ))
        
        fig.add_trace(go.Bar(
            name='Budget Marketing',
            x=artists,
            y=budgets_marketing,
            marker_color='#FF4500',
            text=[f"{v/1000:.0f}k$" for v in budgets_marketing],
            textposition='auto',
            textfont=dict(color='white', size=10, weight='bold')
        ))
        
        fig.update_layout(
            barmode='group',
            title='Répartition des Coûts par Artiste',
            xaxis_title='Artistes',
            yaxis_title='Montant ($)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#00FF00',
                borderwidth=1,
                font=dict(color='white', size=12)
            ),
            xaxis=dict(tickfont=dict(size=10), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=10), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_marketing_analysis(self):
        """Analyse des stratégies marketing"""
        st.markdown('<h3 class="section-title">🎯 ANALYSE DES STRATÉGIES MARKETING</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📢 Budgets Marketing</div>', unsafe_allow_html=True)
            self.create_marketing_budget_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">🎪 Canaux de Distribution</div>', unsafe_allow_html=True)
            self.create_marketing_channels_analysis()
        
        # Analyse détaillée par stratégie
        st.markdown('<div class="subsection-title">🔍 Analyse par Stratégie Marketing</div>', unsafe_allow_html=True)
        self.create_detailed_marketing_analysis()

    def create_marketing_budget_chart(self):
        """Graphique des budgets marketing"""
        artists = list(self.marketing_data.keys())
        budget_ratios = [self.marketing_data[artist]['budget_ratio'] for artist in artists]
        succes = [10 if self.marketing_data[artist]['succes'] == 'Légendaire' else 
                 9 if self.marketing_data[artist]['succes'] == 'Exceptionnel' else
                 8 if self.marketing_data[artist]['succes'] == 'Très bon' else
                 7 if self.marketing_data[artist]['succes'] == 'Bon' else
                 6 if self.marketing_data[artist]['succes'] == 'Correct' else
                 5 for artist in artists]
        
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[budget_ratios[i]],
                y=[succes[i]],
                mode='markers+text',
                marker=dict(
                    size=80, 
                    color=self.color_palette[artist], 
                    opacity=0.9,
                    line=dict(width=3, color='#ffffff')
                ),
                text=[artist],
                textposition="middle center",
                textfont=dict(color='white', size=10, weight='bold'),
                name=artist
            ))
        
        fig.update_layout(
            title='Budget Marketing vs Succès Commercial',
            xaxis_title='Ratio Budget Marketing (%)',
            yaxis_title='Niveau de Succès (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(range=[14, 35], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[4, 11], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_marketing_channels_analysis(self):
        """Analyse des canaux marketing"""
        # Compter les canaux les plus utilisés
        canaux_count = {}
        for artist_data in self.marketing_data.values():
            for canal in artist_data['canaux']:
                canaux_count[canal] = canaux_count.get(canal, 0) + 1
        
        canaux = list(canaux_count.keys())
        counts = list(canaux_count.values())
        
        fig = go.Figure(go.Bar(
            x=counts,
            y=canaux,
            orientation='h',
            marker_color='#9370DB',
            text=counts,
            textposition='auto',
            textfont=dict(color='white', size=12, weight='bold')
        ))
        
        fig.update_layout(
            title='Canaux Marketing les Plus Utilisés',
            xaxis_title="Nombre d'artistes utilisant le canal",
            yaxis_title='Canaux Marketing',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_detailed_marketing_analysis(self):
        """Analyse marketing détaillée"""
        artists = list(self.marketing_data.keys())
        tabs = st.tabs(artists)
        
        for i, artist in enumerate(artists):
            with tabs[i]:
                couleur = self.color_palette[artist]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Stratégie marketing
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {couleur}20 0%, {couleur}05 100%); padding: 1rem; border-radius: 8px; border-left: 5px solid {couleur}; margin-bottom: 1rem;">
                        <div style="color: {couleur}; font-weight: bold; font-size: 1.5rem; margin-bottom: 0.5rem;">{artist}</div>
                        <div style="color: #cccccc; font-size: 1.1rem; font-weight: 500;">Stratégie Marketing</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.metric("Stratégie", self.marketing_data[artist]['strategie'])
                    st.metric("Budget Ratio", f"{self.marketing_data[artist]['budget_ratio']}%")
                    st.metric("Succès", self.marketing_data[artist]['succes'])
                    
                    # Cibles
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Public Cible:</div>
                        <div style="color: #ffffff; font-weight: 500;">{self.marketing_data[artist]['cibles']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Canaux utilisés
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Canaux Principaux:</div>
                        <ul style="color: #ffffff; font-weight: 500;">
                    """, unsafe_allow_html=True)
                    
                    for canal in self.marketing_data[artist]['canaux']:
                        st.markdown(f"<li>{canal}</li>", unsafe_allow_html=True)
                    
                    st.markdown("</ul></div>", unsafe_allow_html=True)
                    
                    # Innovations
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Innovations:</div>
                        <div style="color: #ffffff; font-weight: 500;">{self.marketing_data[artist]['innovations']}</div>
                    </div>
                    """, unsafe_allow_html=True)

    def create_management_analysis(self):
        """Analyse de la gestion et management"""
        st.markdown('<h3 class="section-title">🏢 ANALYSE DE LA GESTION</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📊 Structure Organisationnelle</div>', unsafe_allow_html=True)
            self.create_org_structure()
        
        with col2:
            st.markdown('<div class="subsection-title">💼 Modèle Économique</div>', unsafe_allow_html=True)
            self.create_economic_model()
        
        # Analyse SWOT
        st.markdown('<div class="subsection-title">🔍 Analyse SWOT du Label</div>', unsafe_allow_html=True)
        self.create_swot_analysis()

    def create_org_structure(self):
        """Structure organisationnelle"""
        # Créer un graphique pour la structure organisationnelle
        fig = go.Figure()
        
        # Ajouter les données pour l'organigramme
        fig.add_trace(go.Scatter(
            x=[1, 2, 3, 4, 5],
            y=[1, 1, 1, 1, 1],
            mode='markers+text',
            marker=dict(
                size=[40, 25, 25, 25, 25],
                color=['#00FF00', '#FF4500', '#9370DB', '#FFD700', '#C0C0C0'],
                opacity=0.9,
                line=dict(width=2, color='#ffffff')
            ),
            text=['Fondateurs', 'A&R', 'Production', 'Marketing', 'Digital'],
            textposition="middle center",
            textfont=dict(color='white', size=12, weight='bold'),
            showlegend=False
        ))
        
        # Ajouter les lignes de connexion
        fig.add_shape(type="line", x0=1, y0=1, x1=5, y1=1, line=dict(color="#ffffff", width=2))
        
        fig.update_layout(
            title='Structure Organisationnelle',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=300,
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Construire la liste des départements en HTML
        departments_html = "".join([f"<li>{dept}</li>" for dept in self.management_data['structure']['departements']])
        
        # Construire le HTML final en une seule chaîne propre
        html_card = f"""
        <div class="academic-card">
            <h4 style="color: #ffffff; text-align: center; font-weight: bold;">🏗️ STRUCTURE ORGANISATIONNELLE</h4>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div style="font-weight: 500;">
                    <strong style="color: #00FF00;">Type:</strong> {self.management_data['structure']['type']}
                </div>
                <div style="font-weight: 500;">
                    <strong style="color: #00FF00;">Effectif:</strong> {self.management_data['structure']['effectif']} personnes
                </div>
            </div>
            
            <div style="margin-top: 1rem;">
                <strong style="color: #00FF00;">Départements:</strong>
                <ul style="color: #ffffff; font-weight: 500;">
                    {departments_html}
                </ul>
            </div>
            
            <div style="margin-top: 1rem;">
                <strong style="color: #00FF00;">Culture d'entreprise:</strong>
                <div style="color: #ffffff; font-weight: 500;">{self.management_data['structure']['culture_entreprise']}</div>
            </div>
        </div>
        """
        
        # Afficher le HTML avec le composant dédié
        components.html(html_card, height=250)

    def create_economic_model(self):
        """Modèle économique"""
        # Créer un graphique pour le modèle économique
        categories = ['Revenus', 'Coûts', 'Marge', 'Réinvestissement']
        valeurs = [100, 75, 25, 22]  # Valeurs en pourcentage
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=categories,
            y=valeurs,
            marker_color=['#00FF00', '#FF4500', '#9370DB', '#FFD700'],
            text=[f"{v}%" for v in valeurs],
            textposition='auto',
            textfont=dict(color='white', size=12, weight='bold')
        ))
        
        fig.update_layout(
            title='Répartition Économique',
            xaxis_title='Catégories',
            yaxis_title='Pourcentage (%)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=300,
            showlegend=False,
            xaxis=dict(tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Construire le HTML final en une seule chaîne propre
        html_card = f"""
        <div class="academic-card">
            <h4 style="color: #ffffff; text-align: center; font-weight: bold;">💼 MODÈLE ÉCONOMIQUE</h4>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div style="font-weight: 500;">
                    <strong style="color: #FF4500;">Modèle:</strong> {self.management_data['finances']['model_economique']}
                </div>
                <div style="font-weight: 500;">
                    <strong style="color: #FF4500;">Marge nette:</strong> {self.management_data['finances']['marge_nette']}
                </div>
            </div>
            
            <div style="margin-top: 1rem;">
                <strong style="color: #FF4500;">Investissement:</strong>
                <div style="color: #ffffff; font-weight: 500;">{self.management_data['finances']['investissement_artistes']}</div>
            </div>
            
            <div style="margin-top: 1rem;">
                <strong style="color: #FF4500;">Gestion du risque:</strong>
                <div style="color: #ffffff; font-weight: 500;">{self.management_data['finances']['risque']}</div>
            </div>
        </div>
        """
        
        # Afficher le HTML avec le composant dédié
        components.html(html_card, height=250)

    def create_swot_analysis(self):
        """Analyse SWOT"""
        # Créer un graphique radar pour l'analyse SWOT
        categories = ['Forces', 'Faiblesses', 'Opportunités', 'Menaces']
        valeurs = [9, 4, 8, 6]  # Scores sur 10
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=valeurs + [valeurs[0]],
            theta=categories + [categories[0]],
            fill='toself',
            line=dict(color='#00FF00', width=3),
            marker=dict(size=8, color='#00FF00'),
            name='Analyse SWOT'
        ))
        
        fig.update_layout(
            polar=dict(
                bgcolor='#1a1a1a',
                radialaxis=dict(
                    visible=True, 
                    range=[0, 10],
                    gridcolor='#333333',
                    tickfont=dict(color='#ffffff', size=12),
                    linecolor='#444444'
                ),
                angularaxis=dict(
                    gridcolor='#333333',
                    tickfont=dict(color='#ffffff', size=12),
                    linecolor='#444444'
                )
            ),
            paper_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            showlegend=False,
            height=400,
            title="Analyse SWOT du Label"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Afficher les détails de l'analyse SWOT
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="academic-card eminem-card">
                <h4 style="color: #00FF00; text-align: center; font-weight: bold;">FORCES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Eminem - artiste le plus vendu</li>
                    <li>Réputation d'excellence lyrique</li>
                    <li>Management stable et loyal</li>
                    <li>Distribution mondiale via Universal</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="academic-card fifty-card">
                <h4 style="color: #FF4500; text-align: center; font-weight: bold;">FAIBLESSES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Dépendance à Eminem</li>
                    <li>Difficulté à lancer de nouveaux artistes</li>
                    <li>Style de niche (horrorcore)</li>
                    <li>Sorties irrégulières</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="academic-card obietrice-card">
                <h4 style="color: #9370DB; text-align: center; font-weight: bold;">OPPORTUNITÉS</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Streaming du catalogue historique</li>
                    <li>Collaborations intergénérationnelles</li>
                    <li>Expansion internationale</li>
                    <li>Contenus exclusifs digital</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="academic-card cashis-card">
                <h4 style="color: #FFD700; text-align: center; font-weight: bold;">MENACES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Concurrence des nouveaux labels</li>
                    <li>Évolution des goûts musicaux</li>
                    <li>Vieillissement du public cible</li>
                    <li>Changements dans l'industrie</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    def create_timeline_analysis(self):
        """Analyse chronologique"""
        st.markdown('<h3 class="section-title">📅 ANALYSE CHRONOLOGIQUE</h3>', unsafe_allow_html=True)
        
        # Créer un DataFrame pour la timeline
        df_timeline = pd.DataFrame(self.timeline_data)
        
        fig = go.Figure()
        
        # Ajouter les événements par type
        for event_type in df_timeline['type'].unique():
            df_type = df_timeline[df_timeline['type'] == event_type]
            fig.add_trace(go.Scatter(
                x=df_type['annee'],
                y=df_type['importance'],
                mode='markers+text',
                marker=dict(
                    size=df_type['importance'] * 8,
                    color=self.data_colors.get(event_type, '#ffffff'),
                    opacity=0.8,
                    line=dict(width=2, color='#ffffff')
                ),
                text=df_type['evenement'],
                textposition="top center",
                textfont=dict(color='white', size=10),
                name=event_type,
                showlegend=True
            ))
        
        fig.update_layout(
            title='Timeline Événements Clés du Label',
            xaxis_title='Année',
            yaxis_title='Importance (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#00FF00',
                borderwidth=1,
                font=dict(color='white', size=12)
            ),
            xaxis=dict(range=[1998, 2023], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[0, 11], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tableau détaillé des événements
        st.markdown('<div class="subsection-title">📋 Détail des Événements</div>', unsafe_allow_html=True)
        
        # Formatage du tableau avec style
        st.markdown("""
        <style>
            .event-table {
                background-color: #1a1a1a;
                border-radius: 8px;
                padding: 1rem;
                margin-top: 1rem;
            }
            .event-row {
                display: grid;
                grid-template-columns: 80px 150px 1fr 100px;
                gap: 1rem;
                padding: 0.5rem 0;
                border-bottom: 1px solid #333333;
                color: #ffffff;
            }
            .event-header {
                font-weight: bold;
                color: #00FF00;
                border-bottom: 2px solid #00FF00;
                padding-bottom: 0.5rem;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="event-table">', unsafe_allow_html=True)
        st.markdown('<div class="event-row event-header"><div>Année</div><div>Type</div><div>Événement</div><div>Importance</div></div>', unsafe_allow_html=True)
        
        for event in self.timeline_data:
            color = self.data_colors.get(event['type'], '#ffffff')
            st.markdown(f"""
            <div class="event-row">
                <div style="color: {color}; font-weight: bold;">{event['annee']}</div>
                <div style="color: {color};">{event['type']}</div>
                <div>{event['evenement']}</div>
                <div style="color: {color};">{'⭐' * event['importance']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def create_conclusions(self):
        """Conclusions et recommandations"""
        st.markdown('<h3 class="section-title">📝 CONCLUSIONS ET RECOMMANDATIONS</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="academic-card eminem-card">
                <h4 style="color: #00FF00; text-align: center; font-weight: bold;">🎯 POINTS CLÉS</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Eminem est l'artiste hip-hop le plus vendu de l'histoire</li>
                    <li>Shady Records a lancé des carrières majeures (50 Cent)</li>
                    <li>Focus sur l'excellence lyrique et technique</li>
                    <li>Gestion artist-friendly et familiale</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="academic-card fifty-card">
                <h4 style="color: #FF4500; text-align: center; font-weight: bold;">💡 LEÇONS APPRISES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>L'importance du développement artistique à long terme</li>
                    <li>La valeur des collaborations stratégiques</li>
                    <li>La nécessité de diversifier le portefeuille d'artistes</li>
                    <li>L'équilibre entre art pur et succès commercial</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="academic-card obietrice-card">
                <h4 style="color: #9370DB; text-align: center; font-weight: bold;">🚀 RECOMMANDATIONS STRATÉGIQUES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Développer de nouveaux talents via le mentorat Eminem</li>
                    <li>Explorer les rééditions et contenus inédits</li>
                    <li>Capitaliser sur le streaming avec remasterisations</li>
                    <li>Créer des partenariats avec jeunes labels</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="academic-card cashis-card">
                <h4 style="color: #FFD700; text-align: center; font-weight: bold;">🔮 PERSPECTIVES D'AVENIR</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Transition vers un label de catalogue premium</li>
                    <li>Opportunités dans le documentaire et biopic</li>
                    <li>Expansion dans le merchandising et NFT</li>
                    <li>Positionnement comme académie du rap</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    def run(self):
        """Fonction principale pour exécuter le dashboard"""
        self.display_header()
        
        # Créer les onglets principaux
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🎤 Artistes", 
            "🏭 Production", 
            "🎯 Marketing", 
            "🏢 Gestion", 
            "📅 Timeline", 
            "📝 Conclusions"
        ])
        
        with tab1:
            self.create_artist_analysis()
        
        with tab2:
            self.create_production_analysis()
        
        with tab3:
            self.create_marketing_analysis()
        
        with tab4:
            self.create_management_analysis()
        
        with tab5:
            self.create_timeline_analysis()
        
        with tab6:
            self.create_conclusions()
        
        # Footer
        st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%); border-radius: 10px; border: 1px solid #444444;">
            <p style="color: #00FF00; font-weight: bold; font-size: 1.2rem; font-family: 'Courier New', monospace;">SHADY RECORDS - Dashboard Stratégique</p>
            <p style="color: #cccccc; margin-top: 0.5rem; font-family: 'Courier New', monospace;">Analyse complète 1999-2024 | Label de hip-hop américain</p>
            <div style="margin-top: 1rem;">
                <span class="shady-badge">EMINEM</span>
                <span class="shady-badge">50 CENT</span>
                <span class="shady-badge">SHADY FAMILY</span>
            </div>
            <p style="color: #999999; margin-top: 1rem; font-size: 0.9rem;">© 2024 - Tous droits réservés</p>
        </div>
        """, unsafe_allow_html=True)

# Point d'entrée principal
if __name__ == "__main__":
    analyzer = ShadyAnalyzer()
    analyzer.run()
