import pandas as pd
import numpy as np
import yfinance as yf
from pypfopt import objective_functions
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
import warnings
from datetime import date
warnings.filterwarnings("ignore")




def get_optimal_portfolio(capital, term , risk):
    result = pd.read_excel("risk_result_v1.19.xlsx")
    
    result = result.dropna()
    print(result.head())
    
    #data_m = result[['ticker','short_term_returns','short_term_risk']].iloc[:20,:].set_index('ticker')
    
    ret_data = result.loc[:,result.columns.str.contains(term)]
    ret_data.index = result.ticker
    
    if risk == 'low':
        data_m = ret_data.sort_values([ret_data.columns[1]]).iloc[:15,0]
    else:
        data_m = ret_data.sort_values([ret_data.columns[0]],ascending=False).iloc[:15,0]
        
     
    start_date = pd.to_datetime('2014-10-01')
    end_date = pd.to_datetime(date.today())
    end_date = result.end_date.max()
    data = yf.download(list(data_m.index), start=start_date, end=end_date)['Adj Close']
    print(end_date)
    data = data.dropna()
    S = CovarianceShrinkage(data).ledoit_wolf()
        
    ef = EfficientFrontier(data_m, S)
    ef.add_objective(objective_functions.L2_reg, gamma=0.1)
    weights = ef.max_sharpe()
    
    cleaned_weights = ef.clean_weights()
    latest_prices = get_latest_prices(data)
    #print(latest_prices)
    print(term)
    print(ef.portfolio_performance(verbose=True))
    da = DiscreteAllocation(cleaned_weights, latest_prices, total_portfolio_value=capital)
    # print(latest_prices)
    allocation, leftover = da.greedy_portfolio()
    dct = {k:[v] for k,v in allocation.items()}  # WORKAROUND
    df = pd.DataFrame(dct)
    weigths =pd.DataFrame({k:[v] for k,v in cleaned_weights.items()})
   # result = pd.concat([df.T.rename(columns={0:'qty'}),weigths.T.rename(columns={0:'weights'}),latest_prices],axis=1).reset_index().dropna()
    #result.columns = ['Company','Quantity','weights','Current Price']
    result = pd.concat([df.T.rename(columns={0:'qty'}),latest_prices],axis=1).reset_index().dropna()
    result.columns = ['Company','Quantity','Current Price']
   # print(result)
    #print(cleaned_weights)

    
    return result


def get_invested_amount(result):
  return np.round(np.sum(result['Quantity']*result['Current Price']),2)
  
  
