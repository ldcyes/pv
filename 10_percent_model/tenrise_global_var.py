# trainning and test following stocks
x_stocks=['SOXX','TSLA']
y_stock ='TSLA'
train_targets = [1,3,5,10,20]
data_targets = [1,3,5,10,20]
test_targets = ['1','3','5']
#buy_position = [10,20,30,40]
#sell_position = [10,20,30,40]
# build following stocks

test_model_name=[
#'decision tree',
'SVM',
'RandomForest', #81
'MLP',
#'SGD',
'XGboost' #93
]

gen_inc10_flag =1
features = ["7 day up","7 day down",
            "price/up day","price/mid day","price/low day",
            "price/up week","price/mid week","price/low week",
            "price/up month","price/mid month","price/low month",
            "price/20high","price/20low",

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

train              = 1
regress_start_date = 1500 # at lest 1000 days data 5 years
train_start_date = '20130617'
train_end_date   = '20241212'
test_start_date  = '20200118'
test_end_date    = '20250220'
test_size = 0.2 # train ratio