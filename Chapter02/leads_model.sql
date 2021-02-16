CREATE model 
	`Leads.lead_model_optimum` 
	options 
	(model_type = 'logistic_reg') as
	SELECT 
	Lead_Stage as label, 
	lead_origin, 
	lead_source, 
	source_medium,
	source_campaign,
	do_not_email,
	do_not_call,
	lead_stage,
	lead_score,
	engagement_score,
	totalvisits,
	page_views_per_visit,
	last_activity,
	cityold,
	state,
	country,
	specialization,
	How_did_you_hear_about_SomeSchool,
	search,
	magazine,
	newspaper_article,
	welearn_forums, 
	newspaper,
	digital_advertisement, 
	through_recommendations, 
	receive_more_updates_about_our_courses,
	update_me_on_supply_chain_content,
	Get_updates_on_PGDMHBSCM,
	city_new,
	Asymmetrique_Activity_Index,
	Asymmetrique_Profile_Index,
	Asymmetrique_Activity_Score,
	Asymmetrique_Profile_Score,
	Last_Notable_Activity
	
FROM Leads.Leads_Training_Data;
