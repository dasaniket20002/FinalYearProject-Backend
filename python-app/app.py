from googleapiclient.discovery import build
from recommendationSystem import getRecommendations
from utils import consts
import json
import time

start_time = time.perf_counter()

youtube = build(consts.API_NAME, consts.API_VERSION, developerKey=consts.YT_API_KEY)

tags = ['gamers',
   'vctth',
   'valorant',
   'vct',
   'vct masters',
   'xerxia',
   'sScary',
   'foxz',
   'Sushiboys',
   'Crws',
   'Surf',
   'Zeus',
   'XIA',
   'BLEED',
   'Esports',
   'Pro player',
   'วาโลแรนต์',
   'crazyguy',
   'Deryeon',
   'Juicy',
   'LEGIJA',
   'Bleed',
   'Aim',
   'routine',
   'games',
   'valorant moment',
   'MickiePP',
   'Superbuss',
   'Boomburapa',
   'Viperdemon',
   'Mith',
   'nephh',
   'Fullsense',
    'yourenotjustin',
   'Justin',
   'valorant',
   'overdrive bundle',
   'what does overdrive bundle have',
   'what skins are in overdrive bundle',
   'overdrive',
   'when does overdrive come out',
   'overdrive reveal valorant',
   'new skins valorant',
   'overdrive price valorant',
   'how much is overdrive valorant',
   'when does overdrive valorant',
   'valorant update',
   'is overdrive bundle worth it',
   'all upgrades',
   'valorant overdrive phantom',
   'overdrive blade',
   'overdrive bundle showcase',
   'review',
   'overdrive sheriff',
   'upgraded',
   'overdrive',
   'valorant overdrive vandal',
   'valorant skins',
   'valorant new skin bundle',
   'bundle overdrive',
   'overdrive katana',
   'overdrive knife',
   'valorant katana',
   'valorant skin bundle',
   'valorant new',
   'valorant new skins',
   'valorant new aimbot',
   'valorant aimbot skin',
   'valorant points',
   'free valorant skins',
   'valorant points free',
   'valorant',
   'dark and darker is better game',
   'valorant overdrive skin',
   'valorant overdrive gameplay',
   'valorant gameplay',
   'valorant yoru',
   'valorant aimbot',
   'valorant',
   'valorant highlights',
   'horcus',
   'gaming',
   'radiant',
   'vlorant',
   'valorant live',
   'live valorant',
   'valorant español',
   'vvalorant',
   'alorant',
   'vaorant',
   'valorat',
   'valorant españa',
   'valorant latam',
   'valornt',
   'valoant',
   'valorant gameplay',
   'valorant competir',
   'competir valorant',
   'competir en valorant',
   'competitivo valorant',
   'valorant competitivo',
   'no competir en valorant',
   'nunca valorant',
   'valorant nunca',
   'compito valorant',
   'compito en valorant',
   'valorant compito',
   'no competir valorant',
   'valorant no competir']
topics = ['Action_game',
   'Role-playing_video_game',
   'Video_game_culture','Action_game',
   'Strategy_video_game',
   'Video_game_culture','Action_game',
   'Role-playing_video_game',
   'Video_game_culture']
channelIDs = ['abc0',
 'abc1',
 'abc2','abc11',
 'abc3',
 'abc4','abc6','abc5',
 'abc5',
 'abc6',
 'abc7','abc11','abc0',
 'abc8',
 'abc9',
 'abc10','abc6','abc6','abc6','abc6','abc0',
 'abc11',
 'abc12','abc11','abc0',
 'abc13','abc0',
 'abc14','abc6','abc5','abc0',
 'abc15',
 'abc16',
 'abc17','abc11',
 'abc18',
 'abc19']

videos = getRecommendations.get_recommendations(youtube, [], topics, tags)
print('num videos found = ', len(videos['videos']))
print('SEARCH_LIST_API_CALL_COUNT = ', consts.SEARCH_LIST_API_CALL_COUNT)
print('VIDEO_LIST_API_CALL_COUNT = ', consts.VIDEO_LIST_API_CALL_COUNT) 
print('CHANNEL_SEARCH_CALL_COUNT = ', consts.CHANNEL_SEARCH_CALL_COUNT)
print('TOPIC_SEARCH_CALL_COUNT = ', consts.TOPIC_SEARCH_CALL_COUNT)

print('\n')
with open('python-app/videos_list.json', 'w', encoding='UTF-8') as file:
    json.dump(videos['videos'], file)

end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")

print('------------------------------------------------------------------------------------')
print('\n')