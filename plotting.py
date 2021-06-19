from script import df

from bokeh.plotting import figure,show,output_file

p=figure(x_axis_type='datetime',height=100,width=500,title='Motion graph')

q=p.quad(left=df['start'],right=df['end'],bottom=0,top=1,color='green')
output_file('detected-graph.html')
show(p)