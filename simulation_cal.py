import pandas as pd

def simulation_cal()
	df_range = pd.read_csv("data/quality_setup.csv")
	domain1=list(range(0,10))
	domain2=list(range(10,14))
	domain3=list(range(14,20))
	domain4=list(range(20,23))

	selected_rows=[0,1,2,3,4,10,11]
	domian_weight=[0.5,0.5,0,0]

	member_cnt=1000
	target_recom_pmpm=760
	msr_recom=0.02
	mlr_recom=0.02
	max_recom_savepct=0.4
	max_recom_losspct=0.4
	cap_recom_savepct=0.1
	cap_recom_losspct=0.1

	target_user_pmpm=800
	msr_user=0.02
	mlr_user=0.02
	max_user_savepct=0.4
	max_user_losspct=0.4
	cap_user_savepct=0.1
	cap_user_losspct=0.1
	quality_score_recom=[0.824583333,0.67375,0.908645833,0.762083333,0.869895833]

	twosided=False

	pmpy_mean=850*12
	pmpy_rangepct=[1,1.2,0.8,1.1,0.9] # be,worst,best,worse,better
	cost_range=[pmpy_mean*i*member_cnt for i in pmpy_rangepct]

	cost_wo_contract=864*member_cnt

	target_recom=target_recom_pmpm*12*member_cnt
	target_user=target_user_pmpm*12*member_cnt

	k=0
	for i in range(1,5):
	    selected_indomain=[ j in eval('domain'+str(i)) for j in  selected_rows]    
	    if True in selected_indomain:
	        k=k+1
	        selected_index=[j for j, e in enumerate(selected_indomain) if e == True]
	        selected_eachdomain=[selected_rows[j] for j in selected_index]
	        df_filtered=df_range[df_range['id'].isin (selected_eachdomain)][df_range.columns[11:]]
	        if k==1:
	            quality_score_user=df_filtered.sum()/(len(df_filtered)*2)*domian_weight[i-1]
	        else:
	            quality_score_user=quality_score_user+df_filtered.sum()/(len(df_filtered)*2)*domian_weight[i-1]


	sharing_recom=[]
	sharing_user=[]
	for k in ['recom','user']:
	    target=eval('target_'+k)
	    msr=eval('msr_'+k)
	    mlr=eval('mlr_'+k)
	    max_savepct=eval('max_'+k+'_savepct')
	    max_losspct=eval('max_'+k+'_losspct')
	    cap_savepct=eval('cap_'+k+'_savepct')
	    cap_losspct=eval('cap_'+k+'_losspct')
	    quality_score=eval('quality_score_'+k)
	    for i in range(0,5):
	        net=target-cost_range[i]
	        if net>=0:
	            if net>target*msr:
	                share_pct=max_savepct*quality_score[i]
	                sharing=net*share_pct
	                if sharing>target*cap_savepct:
	                    sharing=target*cap_savepct

	            else:
	                sharing=0
	        else:
	            if twosided==True and abs(net)>target*mlr:
	                sharing=net*max_share_losspct
	                if abs(sharing)>target*cap_losspct:
	                    sharing=-(target*cap_losspct)

	            else:
	                sharing=0
	        eval('sharing_'+k).append(sharing)

	df_planview_aco_totcost=pd.DataFrame(['Total Cost(before G/L share)','G/L Sharing Adj','Total Cost(after G/L share)']*3,columns=['Item'])

	df_planview_aco_totcost=df_planview_aco_totcost.reindex(columns=['Scenario','Item','Best Estimate','Worst','Best','Lower End','Higher End','Metrics'])

	df_planview_aco_totcost.iloc[[0],[2]]=cost_wo_contract
	df_planview_aco_totcost.iloc[[3,6],2:7]=cost_range
	df_planview_aco_totcost.iloc[[4],2:7]=sharing_recom
	df_planview_aco_totcost.iloc[[5],2:7]=[cost_range[i]+sharing_recom[i] for i in range(0,5)]
	df_planview_aco_totcost.iloc[[7],2:7]=sharing_user
	df_planview_aco_totcost.iloc[[8],2:7]=[cost_range[i]+sharing_user[i] for i in range(0,5)]
	df_planview_aco_totcost['Metrics']=["ACO's Total Cost"]*9

	df_planview_aco_pmpm=df_planview_aco_totcost.copy()
	df_planview_aco_pmpm.iloc[:,2:7]=df_planview_aco_totcost.iloc[:,2:7]/member_cnt/12
	df_planview_aco_pmpm['Item']=['PMPM(before G/L share)','G/L Sharing Adj','PMPM(after G/L share)']*3
	df_planview_aco_totcost['Metrics']=["ACO's PMPM"]*9

	df_acoview_totrev=df_planview_aco_totcost.copy()
	df_acoview_totrev['Item']=['Total Revenue(before G/L share)','G/L Sharing Adj','Total Revenue(after G/L share)']*3
	df_acoview_totrev['Metrics']=["ACO's Total Revenue"]*9

	df=pd.concat([df_planview_aco_totcost,df_planview_aco_pmpm,df_acoview_totrev])

	return df
