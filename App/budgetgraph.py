import plotly.graph_objects as go

def add_trace(fig, y, net, color, title, green_num=0, red_num=0,blue_num=0, negative=1, fill2='tonexty'):
  fig.add_trace(go.Scatter(x=[i for i in range(0,len(net))], y=[negative*y[i] + net[i] for i in range(0,len(net))],
    fill=fill2,
    mode='lines',
    line_color='black',
    fillcolor = 'rgba('+str(red_num)+', '+str(green_num)+', 0, 0.5)',
    name=title
    ))
  #print('rgba('+str(red_num)+', '+str(green_num)+', '+str(blue_num)+', 0.5)')
def collection2(fig, collection, total, labels, net,color):
  sum = [i for i in total]
  add_trace(fig, total, net,'green', labels[0],155,0,0,1,None)
  for i in range(1,len(collection)):
    sum = [sum[j] - collection[i-1][j] for j in range(0,len(total))]
    add_trace(fig, sum, net,'green',labels[i], (100*i)% 255)

def collection3(fig, collection, total, labels, net,color):
  sum = [0 for i in total]
  #add_trace(fig, total, net,'green', labels[0],color,0,1,None)
  for i in range(0,len(collection)):
    sum = [sum[j] + collection[i][j] for j in range(0,len(total))]
    add_trace(fig, sum, net,'green',labels[i], (80*(i)) % 255, 255, (80*(i)) % 255,-1)


def budget_graph(country, start, file, add_line=False):
  
  Corporate_Tax = country.CorporateTaxArr[start:]
  #print(Corporate_Tax)
  Income_Tax = country.IncomeTaxArr[start:]
  Tarriffs = country.TarriffRevenuArr[start:]
  revenues = [Corporate_Tax[i] + Income_Tax[i] + Tarriffs[i] + country.pos_interest_payments[i] for i in range(0,len(Corporate_Tax))]
  
  net = [country.Government_SavingsArr[i] - country.GovDebtArr[i] for i in range(0,len(country.Government_SavingsArr))][start:] #[1000, 1200, 1100, 800]
  collection = [country.pos_interest_payments, Corporate_Tax, Income_Tax, Tarriffs]
  expense = [country.WelfareArr[start:],country.InfrastructureArr[start:],country.ScienceBudgetArr[start:],country.MilitaryArr[start:],country.EducationArr[start:], country.neg_interest_payments[start:]]
  expenses = [sum([expense[j][i] for j in range(0,len(expense))]) for i in range(0,len(expense[0]))]
  #print(expenses)
  #debt = [1000, -800, -900, -1100]
  fig = go.Figure()
  fig.update_layout(title_text='Debt and Budget', title_x=0.5)
  collection2(fig, collection, revenues, ['Savings Interest','Tarriffs','Income Tax','Corporate Tax'], net, 255)
  fig.add_trace(go.Scatter(
      x=[i for i in range(0,len(Corporate_Tax))],
      y=net,
      fill='tonexty', # fill area between trace0 and trace1
      name='Net Savings',
      mode='lines', line_color='black',
      fillcolor = 'green',
      line=dict(width=10)
      ))

  collection3(fig, expense, expenses, ['Welfare', 'Infrastructure', 'Science', 'Military', 'Education','Debt Interest'], net, 255)
  fig.update_layout(legend_traceorder="normal")
  if add_line:
    fig.add_vline(x=country.time - 23)
  fig.write_html(file)
