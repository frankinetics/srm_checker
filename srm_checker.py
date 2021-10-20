def srm_pivot(df):
    
    df_new_control = []
    df_new_variant = []
    
    for row in df:
        total = data_pivot.Control + data_pivot.Variant
        control = data_pivot.Control / total
        variant = data_pivot.Variant / total
        df_new_control.append(control)
        df_new_variant.append(variant)
        
    control_x = df_new_control[1]

    variant_x = df_new_variant[1]
    
    df_pivot_new = pd.DataFrame()
    
    df_pivot_new['Date'] =    pd.to_datetime(df['date']).dt.date
    df_pivot_new['Control'] = df.Control
    df_pivot_new['Variant'] = df.Variant
    df_pivot_new['Total'] = df.Variant + df.Control
    
    df_pivot_new['Control_%'] = control_x
    df_pivot_new['Variant_%'] = variant_x
    
    df_pivot_new['Expected'] = (df.Control + df.Variant)/2
    
    chi_f = []
    chi_p = []
    
    for index, row in df_pivot_new.iterrows():
        control_x_x = row.Control
        variant_x_x = row.Variant
        
        observed_x = (row.Control, row.Variant)
        expected_x = (row.Control + row.Variant) / 2
        
        chi = chisquare(observed_x, f_exp = expected_x)
        
        chi_f.append(chi[0])
        chi_p.append(round(chi[1],20))
        
    df_pivot_new['chi_f'] = chi_f
    df_pivot_new['chi_p'] = chi_p
    
    
    df_plot_perc = df_pivot_new[['Date','Control_%', 'Variant_%']]
    
    dates = df_plot_perc['Date']
    
    plt.figure(figsize=(15,10))
    
    plot_perc = sb.lineplot(data = df_plot_perc)
    plot_perc.set_xticklabels(dates)
    plot_perc.set(ylim=(0.45, 0.55))
    
    df_plot_p = df_pivot_new[['Date','chi_p']]
    
    total_users_in_test = sum(df_pivot_new['Control']) + sum(df_pivot_new['Variant'])
    
    control = sum(df_pivot_new['Control']) / total_users_in_test
    variant = sum(df_pivot_new['Variant']) / total_users_in_test
    
    print(100*round(control,5),"% users are in the Control group.")
    print(100*round(variant,5),"% users are in the Variant group")
    
    observed = [sum(df_pivot_new['Control']), sum(df_pivot_new['Variant'])]
    
    total_traffic = sum(observed)
    
    expected = [total_traffic/2, total_traffic/2]
    
    chi = chisquare(observed, f_exp = expected)
    
    if chi[1] < 0.01:
        print("Sample ratio mismatch (SRM) may be present")
    else:
        print("Sample ratio mismatch (SRM) probably not present")
        
    return(df_pivot_new)   