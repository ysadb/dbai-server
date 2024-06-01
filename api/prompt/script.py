import asyncio
import json
import random

from jsonschema import validate
from api.prompt.themes import use_state_theme

from utils.index import get_completion

locations = [
    "Kami's Lookout",
    "Kame House",
    "Planet Namek",
    "Capsule Corp",
    "Galactic Arena",
    "Hero Town",
    "Hyperbolic Time Chamber",
    "Other World Tournament",
    "Space Stage",
]

characters = [
    "Narrator",
    "Goku",
    "Vegeta",
    "Piccolo",
    "Frieza",
    "Cell",
    "Beerus",
    "Whis",
    "Trunks",
    "Gohan",
    "Yamcha",
    "Tien",
    "Bulma",
    "Broly",
    "Krillin",
    "Videl",
    "Android 16",
    "Android 17",
    "Android 18",
    "Nappa",
    "Bardock",
    "Majin Buu",
    "Cooler",
    "Goku Black",
]


async def fix_locations(script, topic):
    support_locations = []
    for scene in script["scenes"]:
        loc = scene["location"]
        if not loc in locations and loc not in support_locations:
            support_locations.append(loc)

    if len(support_locations) == 0:
        return []
    systemPrompt = "Add a visual description to the users locations that is based on the given topic. The visual description should be in one sentence and should not include or reference any of the characters and should be described generically."
    userPrompt = (
        "Story topic is: '''"
        + topic
        + "'''. Locations that need a visual description: "
        + ", ".join(support_locations)
        + "."
    )
    function_schema = {
        "name": "describe_locations",
        "parameters": {
            "type": "object",
            "properties": {
                "locations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "enum": support_locations},
                            "description": {
                                "type": "string",
                                "description": "The visual description of the location, based on the topic. DO NOT leave empty.",
                            },
                        },
                        "required": ["name", "description"],
                    },
                },
            },
            "required": ["locations"],
        },
    }
    data = await get_completion(
        systemPrompt,
        [{"role": "user", "content": userPrompt}],
        function_schema,
        function_schema["name"],
        0.85,
    )
    return data["locations"]


def generate_function_schema(_characters, _locations, list: bool = False):
    return {
        "name": "create_episode_script",
        "parameters": {
            "type": "object",
            "properties": (
                {
                    "title": {"type": "string"},
                    "location": _locations,
                    "conversation": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "character": {
                                    "type": "string",
                                    "enum": _characters,
                                },
                                "dialogue": {"type": "string"},
                            },
                            "required": ["character", "dialogue"],
                        },
                    },
                }
                if not list
                else {
                    "scenes": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "location": _locations,
                                "conversation": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "character": {
                                                "type": "string",
                                                "enum": _characters,
                                            },
                                            "dialogue": {"type": "string"},
                                        },
                                        "required": ["character", "dialogue"],
                                    },
                                },
                            },
                            "required": ["location", "conversation", "title"],
                        },
                    },
                }
            ),
            "required": (
                ["location", "conversation", "title"] if not list else ["scenes"]
            ),
        },
    }


def system_prompt(_characters, _locations, additional_prompt, plustopic=False):
    if plustopic:
        with open("prompts/system_prompt_plus.txt", "r") as file:
            prompt_template = file.read()
    else:
        with open("prompts/system_prompt.txt", "r") as file:
            prompt_template = file.read()
    prompt = prompt_template.replace("$$CHARACTERS$$", "- " + "\n- ".join(_characters))
    prompt = prompt.replace("$$LOCATIONS$$", "- " + "\n- ".join(_locations))
    prompt = prompt.replace("$$ADDITIONAL$$", additional_prompt)
    return prompt


def verifyScript(data, _characters, _locations):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "scenes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "location": _locations,
                        "conversation": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "character": _characters,
                                    "dialogue": {"type": "string"},
                                },
                                "required": ["character", "dialogue"],
                            },
                        },
                    },
                    "required": ["location", "conversation", "title"],
                },
            },
        },
        "required": ["scenes"],
    }
    validate(instance=data, schema=schema)


async def generateScript(topic, state, themeIndex=0):
    plustopic = False
    sceneCount = 1

    splittedTopics = []

    if themeIndex > 0:
        plustopic = True
        if themeIndex > 100:
            sceneCount = themeIndex - 100
            if themeIndex > 101:
                splittedTopics = topic.split("|")
                topic = splittedTopics[0] if len(splittedTopics) > 0 else topic
            themeIndex = 0

    setCharacters = set(characters)

    (mainCharacter, additionalPrompt) = use_state_theme(themeIndex, state)

    if mainCharacter:
        setCharacters.add(mainCharacter.get("name"))

    current_characters = list(setCharacters)
    systemPrompt = system_prompt(
        current_characters, locations, additionalPrompt, plustopic
    )
    userPrompt = "Topic: " + topic + "\n"
    function_schema = generate_function_schema(
        current_characters,
        (
            {
                "type": "string",
            }
            if plustopic
            else {
                "type": "string",
                "enum": locations,
            }
        ),
        plustopic,
    )

    script = {
        "scenes": [],
    }

    messages = [{"role": "user", "content": userPrompt}]

    for index in range(sceneCount):
        genscript = await get_completion(
            systemPrompt,
            messages,
            function_schema,
            function_schema["name"],
            0.7,
            model="gpt-4o" if plustopic else "gpt-3.5-turbo",
        )

        script["scenes"].extend(genscript["scenes"] if plustopic else [genscript])

        messages.extend(
            [
                {
                    "role": "assistant",
                    "function_call": {
                        "name": "create_episode_script",
                        "arguments": json.dumps(genscript),
                    },
                },
                {
                    "role": "user",
                    "content": (
                        (
                            "Create the next scene. Next scene topic: "
                            + splittedTopics[index + 1]
                        )
                        if (len(splittedTopics) > index + 1)
                        else "Create the next scene"
                    ),
                },
            ]
        )

    verifyScript(
        script,
        {
            "type": "string",
        },
        {
            "type": "string",
        },
    )
    if len(script["scenes"]) == 0:
        raise ValueError("Scenes cannot be empty. Please try again.")
    for scene in script["scenes"]:
        if len(scene["conversation"]) == 0:
            raise ValueError("Conversations cannot be empty. Please try again.")

    toRephrase = []
    for scene in script["scenes"]:
        for conversation in scene["conversation"]:
            if conversation["character"] not in current_characters:
                toRephrase.append(conversation)
    if len(toRephrase) > 0:
        with open("prompts/system_prompt_rephrase.txt", "r") as file:
            systemPrompt = file.read()
        userPrompt = "Topic: " + topic + "\n"
        userPrompt += "Current script:\n"
        for scene in script["scenes"]:
            for conversation in scene["conversation"]:
                userPrompt += (
                    f"{conversation['character']}: \"{conversation['dialogue']}\"\n"
                )
        userPrompt += "\n\n\nThe following dialogues need to be rephrased:\n"
        for index, conversation in enumerate(toRephrase):
            userPrompt += f"{index}. {conversation['character']}: \"{conversation['dialogue']}\"\n"
        function_schema = {
            "name": "change_dialogues",
            "parameters": {
                "type": "object",
                "properties": {
                    "dialogues": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "character": {
                                    "type": "string",
                                    "enum": ["Narrator"],
                                },
                                "index": {"type": "integer"},
                                "dialogue": {"type": "string"},
                            },
                            "required": ["character", "dialogue"],
                        },
                    },
                },
                "required": ["dialogues"],
            },
        }
        for _ in range(2):
            data = await get_completion(
                systemPrompt,
                [{"role": "user", "content": userPrompt}],
                function_schema,
                function_schema["name"],
                0.7,
            )
            if len(data["dialogues"]) != len(toRephrase):
                continue
            break
        if len(data["dialogues"]) != len(toRephrase):
            raise ValueError("Error rephrasing dialogues. Please try again.")
        for scene in script["scenes"]:
            for i, conversation in enumerate(scene["conversation"]):
                if conversation in toRephrase:
                    scene["conversation"][i] = {
                        "character": "Narrator",
                        "dialogue": data["dialogues"].pop(0)["dialogue"],
                    }

    verifyScript(
        script,
        {"type": "string", "enum": current_characters},
        {
            "type": "string",
        },
    )

    name_prediction_ids = {}
    if plustopic:
        pass
        # unique_support_locations = await fix_locations(script, topic)
        # all_locations = [loc["name"] for loc in unique_support_locations] + locations
        # verifyScript(
        #     script,
        #     {"type": "string", "enum": current_characters},
        #     {
        #         "type": "string",
        #         "enum": all_locations,
        #     },
        # )
        # prediction_ids = await asyncio.gather(
        #     *[
        #         generate_location(loc["description"], loc["name"])
        #         for loc in unique_support_locations
        #     ]
        # )
        # name_prediction_ids = {
        #     loc["name"]: prediction_id
        #     for loc, prediction_id in zip(unique_support_locations, prediction_ids)
        # }
    else:
        for scene in script["scenes"]:
            if scene["location"] not in locations:
                scene["location"] = random.choice(locations)
        verifyScript(
            script,
            {"type": "string", "enum": current_characters},
            {
                "type": "string",
                "enum": locations,
            },
        )

    # Add characters to scenes

    for scene in script["scenes"]:
        characters_in_scene = set()
        for conversation in scene["conversation"]:
            if mainCharacter and conversation["character"] == mainCharacter.get("name"):
                conversation["character"] = mainCharacter.get("altName")
            characters_in_scene.add(conversation["character"])
        if mainCharacter:
            characters_in_scene.add(mainCharacter.get("altName"))
        scene["characters"] = [
            {"name": character, "type": "main", "variant": 0}
            for character in characters_in_scene
        ]
        scene["location"] = {
            "name": scene["location"],
            "type": (
                "main" if scene["location"] in locations else "support"
            ),  # main or support
            "path": (
                ""
                if scene["location"] in locations
                else scene["location"]  # name_prediction_ids[scene["location"]]
            ),
        }

    script["state"] = state
    script["topic"] = topic
    script["theme"] = themeIndex

    return script
