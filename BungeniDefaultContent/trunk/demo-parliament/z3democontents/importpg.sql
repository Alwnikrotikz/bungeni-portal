copy public.countries from '/home/undesa/Documents/countries.csv' csv ;
copy public.provinces from '/home/undesa/Documents/provinces.csv' csv ;
copy public.regions from '/home/undesa/Documents/regions.csv' csv ;
copy public.constituencies (constituency_id, name, province, region, start_date) from '/home/undesa/Documents/constituencies.csv' csv ;

copy public.constituency_details (constituency_id, voters, "date", population) from
'/home/undesa/Documents/constituency_details.csv' csv ;

copy public.users ( user_id, first_name, middle_name, last_name, date_of_birth, date_of_death, 
email, birth_country, gender, national_id, active_p, type) 
from  '/home/undesa/Documents/users.csv' with delimiter ';' csv ;

update public.users set active_p = 'D' where date_of_death is not null;


copy public.groups ( group_id, short_name, full_name, start_date, end_date, type) 
from '/home/undesa/Documents/parliament_group.csv' with delimiter ';' csv ;

copy public.parliaments (parliament_id, election_date) from '/home/undesa/Documents/parliaments.csv'
with delimiter ';' csv;

copy public.groups ( group_id, short_name, full_name, start_date, end_date, type) 
from '/home/undesa/Documents/government_group.csv'
csv ;

copy public.government from  '/home/undesa/Documents/governments.csv'
csv ;

copy public.groups ( group_id, short_name, full_name, description, start_date, end_date, type) 
from '/home/undesa/Documents/ministry_group.csv'
csv ;

copy public.ministries ( government_id, ministry_id ) 
from '/home/undesa/Documents/ministries.csv'
csv ; 



copy public.user_group_memberships (membership_id, user_id, group_id, start_date, end_date, notes)
from '/home/undesa/Documents/parliament_group_members.csv'
csv;

copy public.parliament_members (membership_id, constituency_id,  elected_nominated , start_date, end_date, leave_reason)
    from '/home/undesa/Documents/parliament_members.csv'
csv ;

update public.parliament_members set elected_nominated ='N' where constituency_id = 0; 

copy public.sessions (session_id, parliament_id, short_name, start_date, end_date, notes)
from '/home/undesa/Documents/sessions.csv'
csv ;

copy public.groups( group_id, short_name, start_date, type )
from '/home/undesa/Documents/parties.csv'
csv ;

copy public.political_parties (party_id)
from '/home/undesa/Documents/party_groups.csv'
csv ;

copy public.committee_types
from '/home/undesa/Documents/committee_types.csv'
csv;

copy public.groups ( group_id, start_date, end_date, short_name, full_name, description, type)
from '/home/undesa/Documents/committee_groups.csv'
csv ;

copy public.committees ( committee_id, parliament_id, committee_type_id, no_members, min_no_members,
quorum, proportional_representation)
from '/home/undesa/Documents/committees.csv'
csv;



/*get all sequences */
select  sequence_name from information_schema.sequences
where sequence_schema='public';

/*set the sequences to a new value*/
 
 SELECT setval('groups_group_id_seq', 1000);
 SELECT setval('sessions_session_id_seq', 1000);
 SELECT setval('item_sequence', 1000);
 SELECT setval('group_sittings_sitting_id_seq', 1000);
 SELECT setval('items_schedule_schedule_id_seq', 1000);
 SELECT setval('question_changes_change_id_seq', 1000);
 SELECT setval('bill_versions_version_id_seq', 1000);
 SELECT setval('question_versions_version_id_seq', 1000);
 SELECT setval('responses_response_id_seq', 1000);
 SELECT setval('bill_changes_change_id_seq', 1000);
 SELECT setval('object_subscriptions_subscriptions_id_seq', 1000);
 SELECT setval('group_assignments_assignment_id_seq', 1000);
 SELECT setval('item_votes_vote_id_seq', 1000);
 SELECT setval('provinces_province_id_seq', 1000);
 SELECT setval('users_user_id_seq', 1000);
 SELECT setval('takes_take_id_seq', 1000);
 SELECT setval('user_group_memberships_membership_id_seq', 1000);
 SELECT setval('take_media_media_id_seq', 1000);
 SELECT setval('rotas_rota_id_seq', 1000);
 SELECT setval('transcripts_transcript_id_seq', 1000);
 SELECT setval('regions_region_id_seq', 1000);
 SELECT setval('motion_amendments_amendment_id_seq', 1000);
 SELECT setval('motion_changes_change_id_seq', 1000);
 SELECT setval('committee_types_committee_type_id_seq', 1000);
 SELECT setval('constituencies_constituency_id_seq', 1000);
 SELECT setval('motion_versions_version_id_seq', 1000);
 SELECT setval('constituency_details_constituency_detail_id_seq', 1000);


copy public.user_group_memberships ( user_id, group_id, start_date, end_date)
from '/home/undesa/Documents/partymembers.csv'
csv;



