1 gen training data 
2 for day in start_day... end day
        training model
        predict next day
        buy or sell?

3 get regression result

Alpha 表示投资组合相对于市场的超额收益
一个资产的 beta 值越高，意味着它的价格波动相对于市场波动更为剧烈
beta是资产或投资组合相对于市场的系统性风险的度量。
如果一个资产的beta为1，它的价格波动与市场一致；
如果beta大于1，它的价格波动相对于市场更为剧烈；如果beta小于1，它的价格波动相对较小。
夏普比率衡量了每单位风险所带来的超额回报。一个高夏普比率意味着资产或投资组合相对于风险的表现较好。投资者通常希望选择夏普比率较高的资产或投资组合


已经有的数据
df[key,'day']['日期'][day]
df[key,'day']['成交量'][day]
df[key,'day']['收盘'][day]
df[key,'day']['开盘'][day]
df[key,'day']['最高'][day]
df[key,'day']['最低'][day]


day
2023-12-11
2023-12-12
2023-12-13
2023-12-14
2023-12-15
week last day
2023-12-15  实际需要2023-12-08, 数据结构中是2023-12-17
month last day
2023-12-29  实际需要2023-11-30，数据结构中是2023-12-29