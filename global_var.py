# trainning and test following stocks
x_stocks=['QQQ']#113.cum
y_stock ='SOXX'
train_targets = [3,5,10,20]
regression_train_targtes = [[3],[5],[10],[20]]
data_targets = ['3','5','10','20']
test_targets = ['3','5','10','20']
back_times =[5,7,9,11]
#buy_position = [10,20,30,40]
#sell_position = [10,20,30,40]
# build following stocks
# bigger shreshold will increase trade rate, but decrease profit
reg_inc_pcent = {'3':0.01,'5':0.015,'10':0.02,'20':0.02}
changes = [1,0.5]
cnt_sell = 0
cnt_buy = 0
test_model_name=[
#'decision tree',
#'SVM',
'RandomForest', #81
#'MLP',
#'SGD',
'XGboost' #93
]

sell_stock = 0
gen_inc10_flag =1
scale_type = 1

features = ["7dayup","7daydown",
            "price_vs_up_day","price_vs_mid_day","price_vs_low_day",
            "price_vs_up_week","price_vs_mid_week","price_vs_low_week",
            "price_vs_up_month","price_vs_mid_month","price_vs_low_month",
            "price_vs_20high","price_vs_20low",
            'near1d_open','near1d_close','near1d_high','near1d_low','near1d_volume',
            'near2d_open','near2d_close','near2d_high','near2d_low','near2d_volume',
            'near3d_open','near3d_close','near3d_high','near3d_low','near3d_volume',
            'near4d_open','near4d_close','near4d_high','near4d_low','near4d_volume',
            'near5d_open','near5d_close','near5d_high','near5d_low','near5d_volume',

            'near1w_open','near1w_close','near1w_high','near1w_low','near1w_volume',
            'near2w_open','near2w_close','near2w_high','near2w_low','near2w_volume',
            'near3w_open','near3w_close','near3w_high','near3w_low','near3w_volume',
            'near4w_open','near4w_close','near4w_high','near4w_low','near4w_volume',
            'near5w_open','near5w_close','near5w_high','near5w_low','near5w_volume',

            'near1m_open','near1m_close','near1m_high','near1m_low','near1m_volume',
            'near2m_open','near2m_close','near2m_high','near2m_low','near2m_volume',
            'near3m_open','near3m_close','near3m_high','near3m_low','near3m_volume',
            'near4m_open','near4m_close','near4m_high','near4m_low','near4m_volume',
            'near5m_open','near5m_close','near5m_high','near5m_low','near5m_volume'
       ]

features_norm = ["price_vs_up_day","price_vs_mid_day","price_vs_low_day",
                 "price_vs_up_week","price_vs_mid_week","price_vs_low_week",
                 "price_vs_up_month","price_vs_mid_month","price_vs_low_month",
            "price_vs_20high","price_vs_20low",
            'near1d_open','near1d_close','near1d_high','near1d_low','near1d_volume',
            'near2d_open','near2d_close','near2d_high','near2d_low','near2d_volume',
            'near3d_open','near3d_close','near3d_high','near3d_low','near3d_volume',
            'near4d_open','near4d_close','near4d_high','near4d_low','near4d_volume',
            'near5d_open','near5d_close','near5d_high','near5d_low','near5d_volume',

            'near1w_open','near1w_close','near1w_high','near1w_low','near1w_volume',
            'near2w_open','near2w_close','near2w_high','near2w_low','near2w_volume',
            'near3w_open','near3w_close','near3w_high','near3w_low','near3w_volume',
            'near4w_open','near4w_close','near4w_high','near4w_low','near4w_volume',
            'near5w_open','near5w_close','near5w_high','near5w_low','near5w_volume',

            'near1m_open','near1m_close','near1m_high','near1m_low','near1m_volume',
            'near2m_open','near2m_close','near2m_high','near2m_low','near2m_volume',
            'near3m_open','near3m_close','near3m_high','near3m_low','near3m_volume',
            'near4m_open','near4m_close','near4m_high','near4m_low','near4m_volume',
            'near5m_open','near5m_close','near5m_high','near5m_low','near5m_volume']

features_norm_all = []
for x_stock in x_stocks:
    for feature in features_norm:
            features_norm_all.append(x_stock+feature)
            
train = 1
is_xueqiu = 1
is_futures = 0
regress_start_date = 1500 # at lest 1000 days data 5 years
# xueqiu '2012-06-17'
# efinance '20140618'

if(is_xueqiu):
    train_start_date = '2012-06-17'
    train_end_date   = '2024-03-21'
    test_start_date  = '2014-06-18'
    test_end_date    = '2018-03-30'
else:
    train_start_date = '20140618'
    train_end_date   = '20240321'
    test_start_date  = '20140618'
    test_end_date    = '20180330'

test_size = 0.2 # train ratio

NASDAQ_100 = \
['AAPL'\
,'ABNB'\
,'ADBE'\
,'ADI'\
,'ADP'
,'ADSK'
,'AEP'
,'AMAT'
,'AMD'
,'AMGN'
,'AMZN'
,'ANSS'
,'ASML'
,'AVGO'
,'AZN'
,'BIIB'
,'BKNG'
,'BKR'
,'CCEP'
,'CDNS'
,'CDW'
,'CEG'
,'CHTR'
,'CMCSA'
,'COST'
,'CPRT'
,'CRWD'
,'CSCO'
,'CSGP'
,'CSX'
,'CTAS'
,'CTSH'
,'DASH'
,'DDOG'
,'DLTR'
,'DXCM'
,'EA'
,'EXC'
,'FANG'
,'FAST'
,'FTNT'
,'GEHC'
,'GFS'
,'GILD'
,'GOOG'
,'GOOGL'
,'HON'
,'IDXX'
,'ILMN'
,'INTC'
,'INTU'
,'ISRG'
,'KDP'
,'KHC'
,'KLAC'
,'LIN'
,'LRCX'
,'LULU'
,'MAR'
,'MCHP'
,'MDB'
,'MDLZ'
,'MELI'
,'META'
,'MNST'
,'MRNA'
,'MRVL'
,'MSFT'
,'MU'
,'NFLX'
,'NVDA'
,'NXPI'
,'ODFL'
,'ON'
,'ORLY'
,'PANW'
,'PAYX'
,'PCAR'
,'PDD'
,'PEP'
,'PYPL'
,'QCOM'
,'REGN'
,'ROP'
,'ROST'
,'SBUX'
,'SIRI'
,'SNPS'
,'TEAM'
,'TMUS'
,'TSLA'
,'TTD'
,'TTWO'
,'TXN'
,'VRSK'
,'VRTX'
,'WBA'
,'WBD'
,'WDAY'
,'XEL'
,'ZS']
