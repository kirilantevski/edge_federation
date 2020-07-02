import altair as alt
import json
import time
import pandas as pd
import sys
import os


results_path= "../../results/"
file_type = ".html"

def reduce_data(data):
    data = list(data)
    data = data[2:]
    return data

def reverse_data(data):
    data_reversed = [None]*len(data)
    for i,e, in reversed(list(enumerate(data))):
        if i>0:
            data_reversed[i] = data[i]-data[i-1]
        else:
            data_reversed[i]=data[i]
    return data_reversed

def generateProcedureLabels(data, domain, field):
    fed_label = [str("federation procedure")]*len(data)
    if domain == 'consumer':
        fed_label[:data.index(field)] = [str("deployment procedure")]*len(data[:data.index(field)])
        return fed_label
    elif domain == 'provider':
        fed_label[data.index(field):] = [str("deployment procedure")]*len(data[data.index(field):])
        return fed_label
    else:
        return data
    

def plot_data(data):
    data_values = reduce_data(data.values())
    data_keys = reduce_data(data.keys())
    
    field = "federation_start" if data["domain"] == 'consumer' else "trusty_info_get"
    procedure = generateProcedureLabels(data_keys, data["domain"], field)

    print(field, data["domain"], procedure)
    plot_data = pd.DataFrame({'time':data_values, 'phases':data_keys, 'procedure':procedure})

    plot = alt.Chart(plot_data).mark_bar().encode( x= 'time', y= alt.Y('phases',sort='x'), color='procedure')
    # plot = alt.Chart(plot_data).mark_line(point=True).encode( x= 'time', y= alt.Y('phases',sort='x'), color='phases')

    return plot


def combine_plots(consumer_data, provider_data):
    consumer_values = reduce_data(consumer_data.values())
    provider_values = reduce_data(provider_data.values())
    provider_keys = reduce_data(provider_data.keys())
    consumer_keys = reduce_data(consumer_data.keys())
    
    consumer_values = reverse_data(consumer_values)
    provider_values = reverse_data(provider_values)

    consumer_label = ['consumer']*len(consumer_keys)
    provider_label = ['provider']*len(provider_keys)

    c_fed_label = [str("federation procedure")]*len(consumer_keys)
    c_fed_label[:consumer_keys.index("federation_start")] = [str("deployment procedure")]*len(consumer_keys[:consumer_keys.index("federation_start")])
    
    p_fed_label = [str("federation procedure")]*len(provider_keys)
    p_fed_label[provider_keys.index("trusty_info_get"):] = [str("deployment procedure")]*len(provider_keys[provider_keys.index("trusty_info_get"):])
  

    c_plot_data = pd.DataFrame({'time':consumer_values, 'phases':consumer_keys, 'domain':consumer_label, 'procedure':c_fed_label})
    p_plot_data = pd.DataFrame({'time':provider_values, 'phases':provider_keys, 'domain':provider_label, 'procedure':p_fed_label})

    # c_plot = alt.Chart(c_plot_data).mark_bar().encode( x= 'time', y= alt.Y('domain', sort='x'), color='phases')
    # p_plot = alt.Chart(p_plot_data).mark_bar().encode( x= 'time', y= alt.Y('domain', sort='x'), color='phases')
    # c_plot = alt.Chart(c_plot_data).mark_bar().encode( x= 'time', y= alt.Y('domain', sort='x'), color=alt.Color('procedure', legend= None))
    # p_plot = alt.Chart(p_plot_data).mark_bar().encode( x= 'time', y= alt.Y('domain', sort='x'), color=alt.Color('procedure', legend= None))
    
    c_plot = alt.Chart(c_plot_data).mark_bar().encode( x= 'time', y= alt.Y('domain', sort='x'), color=alt.Color('procedure', legend= alt.Legend(orient="bottom")))
    p_plot = alt.Chart(p_plot_data).mark_bar().encode( x= 'time', y= alt.Y('domain', sort='x'), color=alt.Color('procedure', legend= alt.Legend(orient="bottom")))
    
    plot = c_plot + p_plot

    return plot




if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('[Usage] {} result_consumer result_provider'.format(
            sys.argv[0]))
        exit(0)
    else:
        with open(results_path+sys.argv[1]+".json") as consumer_file:
            consumer_data = json.load(consumer_file)

        with open(results_path+sys.argv[2]+".json") as provider_file:
            provider_data = json.load(provider_file)

    plot_consumer = plot_data(consumer_data)
    plot_provider = plot_data(provider_data)

    cobined_plot = combine_plots(consumer_data, provider_data)
    combined_file_string = sys.argv[1].split('_')[0] + "_combined"
    plot_consumer.save(results_path+sys.argv[1]+file_type, scale_factor=2.0)
    plot_provider.save(results_path+sys.argv[2]+file_type, scale_factor=2.0)
    cobined_plot.save(results_path+combined_file_string+file_type, scale_factor=2.0)