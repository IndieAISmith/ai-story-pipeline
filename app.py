from dotenv import load_dotenv
from groq import Groq
import requests
import random
import time
import json
import logging
import ast
import os


load_dotenv()
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GPT4OAssistant:
    """
    This class is responsible for interacting with the GPT-4O API.
    """
    def __init__(self):
        
        """
        Initializes the GPT4OAssistant class with the API URL and headers.
        """
        logger.info("Initializing GPT4OAssistant")
        pass

    def chat(self, prompt, conversation_history):
        """
        Sends a chat request to the GPT-4O API with the provided prompt and conversation history.
        Handles exceptions and implements a cool-down mechanism in case of errors.

        Parameters:
        prompt (str): The prompt to be sent to the GPT-4O API.
        conversation_history (list): The conversation history to be sent to the GPT-4O API.

        Returns:
        str: The response received from the GPT-4O API.
        """
        logger.info("Sending chat request to GPT-4O API")
        
        payload = json.dumps({
            "prompt": prompt,
            "conversationHistory": conversation_history
        })

        try:
            logger.info("Sending payload to GPT-4O API")
            logger.info("Waiting for response from GPT-4O API...")
           
            response = requests.request("POST", self.url, headers=self.headers, data=payload)
            json_response = response.json()
                                                                                        
            logger.info("Response received from GPT-4O API")
            
            return json_response["response"]
        
        except Exception as e:
            
            print(f"Error occurred while communicating with GPT-4O: {e}")
            print(f"Unable to generate response. RAW response received: {response}")
            print("15 Seconds cool-down phase starting...")
            time.sleep(15)
            print("Cool-down phase end...")
            return self.chat(prompt, conversation_history)

class AiForceimagger:
    """Image provider for pollinations.ai"""

    def __init__(self, timeout: int = 60, proxies: dict = {}):
        """Initializes the PollinationsAI class.

        Args:
            timeout (int, optional): HTTP request timeout in seconds. Defaults to 60.
            proxies (dict, optional): HTTP request proxies (socks). Defaults to {}.
        """
        self.image_gen_endpoint = "https://api.airforce/v1/imagine2?prompt={prompt}&size={size}&seed={seed}&model={model}"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.proxies.update(proxies)
        self.timeout = timeout
        self.image_extension: str = "png"
        self.count = 0

    def generate(self, prompt: str, amount: int = 1,max_retries: int = 3, retry_delay: int = 5):
        """Generate image from prompt

        Args:
            prompt (str): Image description.
            amount (int): Total images to be generated. Defaults to 1.
            additives (bool, optional): Try to make each prompt unique. Defaults to True.
            width (int, optional): Width of the generated image. Defaults to 768.
            height (int, optional): Height of the generated image. Defaults to 768.
            model (str, optional): The model to use for image generation. Defaults to "flux".
            max_retries (int, optional): Maximum number of retry attempts. Defaults to 3.
            retry_delay (int, optional): Delay between retries in seconds. Defaults to 5.

        Returns:
            List[bytes]: List of generated images as bytes.
        Model: 
            "flux", "flux-anime", "flux-realism", "flux-disney"
        """
        assert bool(prompt), "Prompt cannot be null"
        assert isinstance(amount, int), f"Amount should be an integer only not {type(amount)}"
        assert amount > 0, "Amount should be greater than 0"

        self.prompt = prompt
        response = []


        url = self.image_gen_endpoint.format(prompt = prompt, size = "9:16", model = "flux-disney",seed = random.randint(1000, 1000000))

        for attempt in range(max_retries):
            try:
                resp = self.session.get(url, timeout=self.timeout)
                resp.raise_for_status()
                response.append(resp.content)
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"Failed to generate image after {max_retries} attempts: {e}")
                    raise
                else:
                    print(f"Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
        return response

    def save(self,response,name: str = None):
        """Save generated images

        Args:
            response (List[bytes]): List of generated images as bytes.
            name (str): Filename for the images. Defaults to the last prompt.
            dir (str, optional): Directory for saving images. Defaults to os.getcwd().
            filenames_prefix (str, optional): String to be prefixed at each filename to be returned.

        Returns:
            List[str]: List of saved filenames.
        """
        assert isinstance(response, list), f"Response should be of {list} not {type(response)}"
        name = self.prompt if name is None else name
        filenames = []
        for image in response:
        
            self.count += 1
            with open(f"images_of_scene{self.count}.png", "wb") as fh:
                fh.write(image)
        return filenames


class Util:
    def __init__(self):
        pass
    def clean_json(self,json_str):
        """
        This function is used to clean and parse a JSON string.
        """
        json_str = json_str.strip()  # Remove leading and trailing whitespaces

        if json_str.startswith("```json") and json_str.endswith("```"):
            data = ast.literal_eval(json_str.replace("```json", "").replace("```",""))
            return data
        
        elif "```json" in json_str: 
            start = json_str.index("```json")
            end = json_str.index("```")
            return json_str[start+7:end]
        else:
            data = ast.literal_eval(json_str)
            return data


class Prompt:
    #1
    base_prompt = """
    Hi ChatGPT, I am assigning you a task and guiding you on how to work on it.
    We are creating an animated short YouTube video, and you need to help us generate prompts for the scenes. These prompts will be sent to an AI text-to-image model to generate the image. You need to work in such a way that I will give you the entire story (the script), and after that, you will analyze the script. Then, you'll tell me how many characters are in the story, focusing on the main characters.
    For each character, under their name, I want you to generate a prompt that describes their facial features, body, face shape, hair, figure, age, skin tone, and clothes. Each character's facial features, age, and clothing should be different from the others.
    Once you provide the prompts for the characters, I will then send you the scenes of the script in parts. For example, I will select a part of the story/script based on my preference, and you will look at that part and generate a image prompt based on the whole story.
    The reason I am giving you the entire script is so that you can understand the environment of the story and adjust the prompt accordingly. For instance, if it's a survival story, you should add the "Cinematic, Shot of, Wide short" keyword in the prompt according to express the scene. If it's a cartoon, you should use something like "3D Pixar cartoon style."
    Are you ready? If yes, say "Yes." The prompts for the story should be
    generated in English and not more than 4 lines. 
    
    Example: 
    input = "A young adventurer named Eira found herself stranded in a mystical forest to find the ancient Tree of Wisdom,"
    answer = "``json 
    {
        "imgprompt": "A young, determined adventurer named Eira stands at the edge of a mystical forest. The forest is filled with towering, gnarled trees with luminescent leaves, creating an otherworldly glow. Mist swirls around her feet, and in the distance, a massive, ancient tree with a shimmering aura can be seen - the Tree of Wisdom. Eira's clothing is slightly tattered, indicating her journey has been long and challenging. Her expression is a mix of awe and determination as she gazes into the depths of the magical forest. Fireflies and wisps float in the air, guiding her path. The overall atmosphere is ethereal and enchanting, with a color palette of deep greens, purples, and soft golden light."
    }
    ```
    "
    
    input = "a mischievous sprite who flitted about Eira's head, playing tricks and causing trouble."
    answer = "```json
    {
    "imgprompt":"A young, determined adventurer named Eira stands at the edge of a mystical forest. The forest is filled with towering, gnarled trees with luminescent leaves, creating an otherworldly glow. Mist swirls around her feet, and in the distance, a massive, ancient tree with a shimmering aura can be seen - the Tree of Wisdom. Eira's clothing is slightly tattered, indicating her journey has been long and challenging. Her expression is a mix of awe, determination, and slight annoyance as she tries to focus on her path.
Hovering around Eira's head is a small, glowing, mischievous sprite. The sprite has translucent wings that shimmer with iridescent colors and a impish grin on its face. It's pulling at a strand of Eira's hair with one tiny hand while the other hand is conjuring small, colorful magical sparks. The sprite's antics create a contrast between the serene, mystical forest and the chaotic energy surrounding Eira.
Fireflies and wisps float in the air, seemingly amused by the sprite's tricks. The overall atmosphere is ethereal and enchanting, with a color palette of deep greens, purples, and soft golden light, punctuated by the bright, playful glow of the troublesome sprite."
    }``` "
    
    ### Important instructions:
    Don't provide any explanations or context in the prompt.
    """

    #2
    character_prompt = "Write me prompt of the character to generate it with ai text to image generator, Make sure add facial details character style details, details about what wearing, and hairs , and everything.Don't include like 'Create a' or 'Imagine a'. OUTPUT RESPONSE MUST BE JSON like :\n "+'{(character name):(character image prompt)}'

    #3
    character_feeding_prompt = """In any scene where {character}'s name appears, you will add these details to the prompt:{description}"""

    #4
    scenes_extractor_prompt = """Your task is to provide all scene based on the story telling prespective, Analysics the whole story and look only those sentences that help me to create a storyboard images from it for my story. Extract only single line/scene from the story that used to describe situation, don't try to rephrase it. OUTPUT RESPONSE MUST BE JSON like : ["scene1","scene2","scene3"] """


class StoryFlow:
    
    def __init__(self):
        
        logger.info("Initializing StoryFlow")
        
        self.chat_history = [{"role": "user","content": Prompt.base_prompt},{"role": "assistant","content": "Yes."}]
        self.assistant = GPT4OAssistant()
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.util = Util()
        self.story = None
        self.characters = []
        
        
    def story_generation(self):
        
        logger.info("Generating story")
        
        completion = self.client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "I will provide you a formula to generate Unique a story.\nformula for synopsis: {Character} {Situation} in a {setting} to achieve {goal}, facing {obstacle}, with the help of {allies}, leading to a {climax}, and discovering that {moral}.\nuse the generate a synopsis. Don't provide any explanation."
                },
                {
                    "role": "assistant",
                    "content": "Ok, Synopsis is generated in my end. What i need to do next?"
                },
                {
                    "role": "user",
                    "content": "Use that generated Synopsis, Create a story. Don't provide any explanation."
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        
        self.story =  completion.choices[0].message.content
    
    def character_extraction(self):
        
        logger.info("Extracting characters")
        
        response = self.assistant.chat("Your task is to extract the Character from the Story you provided. OUTPUT: [{'name':'character_name','description':'character's short description in 3 to 4 words only'}]", [{"role": "assistant", "content": self.story}])
        self.characters = self.util.clean_json(json_str=response)

    def character_ingestion(self):
        logger.info("Ingesting characters")
        
        for character in self.characters:
            
            _charater_data = self.assistant.chat(prompt=f"Character name: {character['name']} \n Key features: {character['description']} " + Prompt.character_prompt, conversation_history=[])
            charater_data = self.util.clean_json(json_str=_charater_data)
            
            temp_prompt = Prompt.character_feeding_prompt.format(character=character['name'], description=charater_data[character['name']])
            gptresponse = self.assistant.chat(temp_prompt,self.chat_history)
                        
            self.chat_history.append({"role": "user","content":temp_prompt})
            self.chat_history.append({"role": "assistant","content": gptresponse})
    
    def scene_extraction(self):
        logger.info("Extracting scenes")
        
        response = self.assistant.chat(prompt=Prompt.scenes_extractor_prompt, conversation_history=[{"role": "assistant", "content": self.story}])   
        scenes = self.util.clean_json(json_str=response)
        
        return scenes
    
    def consolidate_chat_history(self):
        logger.info("Consolidating chat history")
        
        _chat_history  = self.assistant.chat("Extract All intructions including context, characters prompts in most acurate and exact way as possible and Summarize them.",self.chat_history)
        return _chat_history

    def scene_imagination(self, scene, instructions = None, chat_history= []):
        logger.info("Generating scene imagination")
        
        if instructions and instructions != "":
            gptresponse = self.assistant.chat(prompt=scene, conversation_history= [{"role": "assistant","content": instructions}])
        else:
            gptresponse = self.assistant.chat(prompt=scene, conversation_history= chat_history)
             
        self.chat_history.append({"role": "user","content": scene})
        self.chat_history.append({"role": "assistant","content": gptresponse})
        
        return gptresponse

    def save_chat_history(self):
        logger.info("Saving chat history")
        
        # Specify the filename
        filename = 'history.json'

        # Save the dictionary to a JSON file
        with open(filename, 'w') as json_file:
            json.dump(self.chat_history, json_file, indent=4)

        print(f"Data saved to {filename}")
        
        
    def pipeline(self):
        
        self.story_generation()
        
        self.character_extraction()
        self.character_ingestion()
            
        scenes = self.scene_extraction()
            
        print("Summarized Chat History:")
        chat_history = self.consolidate_chat_history()
        print(chat_history)
        
        imagger = AiForceimagger()
        images_prompts = []
        
        
        print("Character Image Prompts:")
        for character in self.characters:
            print(f"{character}")
        
        print("\nScene Imagination:")
        for scene in scenes:
            #o =  input(f"Do you want to generate an image for scene '{scene}'? (y/n): ")
            o = 'y'
            
            print("Sleeping for 5 seconds...")
            time.sleep(5)
            
            print(f"Instructions for Scene: {scene}")
            if o.lower() == 'y':
                prompt = self.scene_imagination(scene, instructions=chat_history + """
                                                  OUTPUT RESPONSE MUST BE A JSON: 
                                                like: 
                                                ```json
                                                {"imgprompt":"image prompt is here"}
                                                ```
                                                """)
                images_prompts.append(prompt)
            else:
                continue
            
        for prompt in images_prompts:
            _prompt = self.util.clean_json(json_str=prompt)
            print(f"Generating Image....for Prompt: ")
            print(_prompt["imgprompt"])
            
            resp = imagger.generate(str(_prompt["imgprompt"]))
            print(f"Generated Image: {imagger.save(resp)}")
        
        self.save_chat_history()
        
        
story_flow = StoryFlow()
story_flow.pipeline()
