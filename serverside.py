import asyncio
import json
import websockets
from obswebsocket import obsws, requests

# create the obs websocket stuff
ws = obsws(host="localhost", port=4455, password="DBikFxnvjhsgwDYo")
ws.connect()

new_misses = 0


async def start_getting_bs_info():
    data_type = "LiveData"
    url = f"ws://localhost:2946/BSDataPuller/{data_type}"
    try:
        async with websockets.connect(url) as websocket:
            # recv data from ws
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)
                    # print("LIVEDATA:", data)
                    # print("----")
                    livedata_change_obs_text(data["Score"], data["Rank"], data["Combo"], data["NotesSpawned"],
                                             data["Accuracy"],
                                             data["TimeElapsed"], data['EventTrigger'])
                except websockets.ConnectionClosed:
                    print("LiveData Connection closed")
                    break
    except Exception as e:
        if e == ConnectionRefusedError:
            print("ConnectionRefusedError: Is your game open?")
        else:
            print("Exception:", e)


async def start_getting_map_info():
    data_type = "MapData"
    url = f"ws://localhost:2946/BSDataPuller/{data_type}"
    try:
        async with websockets.connect(url) as websocket:
            # recv data from ws
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)
                    # print("MAPDATA:", data)
                    # print("----")
                    mapinfo_change_obs_text(data['Mapper'], data['SongName'], data['SongAuthor'], data['BPM'],
                                            data['Difficulty'])

                except websockets.ConnectionClosed:
                    # print("MapData Connection closed")
                    break
    except Exception as e:
        if e == ConnectionRefusedError:
            print("ConnectionRefusedError: Is your game open?")
        else:
            print("Exception:", e)


def livedata_change_obs_text(score, rank, combo, notesspawned, acc, timepassed, eventtrigger):
    global new_misses

    # hack fix until i figure out why misses arent counting properly
    if combo == 0 and notesspawned > 0 and eventtrigger == 3:
        new_misses += 1

    # ugly code but whatever
    # overlay=True keeps the same font and stuff settings for the text
    ws.call(requests.SetInputSettings(inputName="scores_text", inputSettings={"text": str(score)}, overlay=True))
    ws.call(requests.SetInputSettings(inputName="ranks_text", inputSettings={"text": str(rank)}, overlay=True))
    ws.call(requests.SetInputSettings(inputName="combos_text", inputSettings={"text": str(combo)}, overlay=True))
    ws.call(requests.SetInputSettings(inputName="miss_text", inputSettings={"text": str(new_misses)}, overlay=True))
    ws.call(
        requests.SetInputSettings(inputName="accuracy_text", inputSettings={"text": str(round(acc, 2)) + "%"},
                                  overlay=True))

    time = f"{(timepassed // 60):02}:{(timepassed % 60):02}"
    ws.call(requests.SetInputSettings(inputName="time_text", inputSettings={"text": str(time)}, overlay=True))


def mapinfo_change_obs_text(mapper, mapname, author, bpm, difficulty):
    ws.call(requests.SetInputSettings(inputName="mapper_name_text", inputSettings={"text": str(mapper)}, overlay=True))
    ws.call(requests.SetInputSettings(inputName="map_name_text", inputSettings={"text": str(mapname)}, overlay=True))
    ws.call(requests.SetInputSettings(inputName="author_name_text", inputSettings={"text": str(author)}, overlay=True))
    ws.call(requests.SetInputSettings(inputName="bpms_text", inputSettings={"text": str(bpm) + " BPM"}, overlay=True))

    diff = "Expert+" if difficulty == "ExpertPlus" else difficulty
    ws.call(requests.SetInputSettings(inputName="diff_text", inputSettings={"text": str(diff)}, overlay=True))

    # didnt work for some reason so got rid of it
    # print(ws.call(requests.SetInputSettings(inputName="coverart", inputSettings={"source": str(cover_link)})))


async def run():
    print("Launching Websocket")
    bs_info = asyncio.create_task(start_getting_bs_info())
    map_info = asyncio.create_task(start_getting_map_info())

    await asyncio.gather(bs_info, map_info)


def create_text(scene: str, input_name: str, posx: float, posy: float, align: str):
    try:
        sceneid = ws.call(
            requests.CreateInput(sceneName=scene, inputName=input_name, inputKind="text_gdiplus_v3")).datain[
            'sceneItemId']
        ws.call(requests.SetSceneItemTransform(sceneName=scene, sceneItemId=sceneid,
                                               sceneItemTransform=
                                               {'positionX': posx, 'positionY': posy,
                                                'scaleX': 0.48076921701431274, 'scaleY': 0.48000001907348633,
                                                'sourceHeight': 100.0, 'sourceWidth': 1000.0,
                                                "height": 48.0, 'width': 480.76922607421875}))

        ws.call(requests.SetInputSettings(inputName=input_name,
                                          inputSettings=
                                          {"text": input_name,
                                           'align': align,
                                           'alignment': 'right',
                                           'antialiasing': True,
                                           'bk_opacity': 0,
                                           'extents': True,
                                           'extents_cx': 1000,
                                           'font': {
                                               'face': 'DFPPOPCorn-W12',
                                               'flags': 0, 'size': 48,
                                               'style': 'Regular'},
                                           'outline': True,
                                           'outline_color': 4278190080,
                                           'valign': 'center',
                                           }, overlay=True))
    except KeyError:
        print(f"KeyError! {input_name} probably already exists.")


def create_scene(scene: str):
    if not scene_exists_already(scene):
        ws.call(requests.CreateScene(sceneName=scene))


def create_beat_saber_display(scene: str):
    sceneid = ws.call(requests.CreateInput(sceneName=scene,
                                           inputName="beatsaber_touhou_overlay",
                                           inputKind="game_capture")).datain['sceneItemId']
    # id = ws.call(requests.GetSceneItemId(sceneName="bs_touhou", sourceName="bs")).datain
    ws.call(requests.SetSceneItemTransform(sceneName=scene, sceneItemId=sceneid,
                                           sceneItemTransform=
                                           {'height': 0.0, 'width': 0.0,
                                            'positionX': 503.0, 'positionY': 357.0,
                                            'scaleX': 0.6385416388511658, 'scaleY': 0.6388888955116272,
                                            'alignment': 0
                                            }
                                           ))
    ws.call(requests.SetSceneItemIndex(sceneName=scene, sceneItemId=sceneid, sceneItemIndex=0))
    ws.call(requests.SetInputSettings(inputName="beatsaber_touhou_overlay",
                                      inputSettings=
                                      {
                                          "capture_mode": "window",
                                          "window": "Beat Saber:UnityWndClass:Beat Saber.exe"
                                      }))
    # id = ws.call(requests.GetSceneItemId(sceneName="touhou_overlay", sourceName="beatsaber_touhou_overlay")).datain['sceneItemId']
    # print(ws.call(requests.GetSceneItemTransform(sceneName=scene, sceneItemId=id)))

def create_background(scene: str, bg_image_path: str):
    # get the resolution of the scene
    scene_data = ws.call(requests.GetVideoSettings())
    width, height = scene_data.datain['baseWidth'], scene_data.datain['baseHeight']

    # create the background
    ws.call(requests.CreateInput(sceneName=scene,
                                 inputName="background",
                                 inputKind="image_source",
                                 inputSettings={"file": bg_image_path}))

    # get the background sceneId
    bgscene = ws.call(requests.GetSceneItemId(sceneName=scene, sourceName="background"))
    background_sceneid = bgscene.datain['sceneItemId']

    # position the background accordingly
    ws.call(requests.SetSceneItemTransform(
        sceneName=scene, sceneItemId=background_sceneid, sceneItemTransform=
        {
            "scaleX": width / 1920, "scaleY": height / 1080,
            "width": width, "height": height,
            "positionX": 0, "positionY": 0}
    ))

    # set the filters for the greenscreen
    ws.call(requests.CreateSourceFilter(
        sourceName="background",
        filterName="Chroma Key",
        filterKind="chroma_key_filter_v2",
        filterSettings={}
    ))


def scene_exists_already(scene_name):
    scenes = ws.call(requests.GetSceneList()).datain['scenes']
    for scene in scenes:
        if scene['sceneName'] == scene_name:
            return True
    return False


# create_touhou_scene("touhou_overlay", "D:/Backups/Desktop/mems/touhouhscore_notext.png")
# asyncio.run(run())

# print(ws.call(requests.GetInputKindList()).datain)
