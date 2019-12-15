import collections
from google.cloud import vision
from google.cloud import translate
from google.cloud.vision import types
import requests
import subprocess

WordBox = collections.namedtuple('WordBox', ['word', 'geometry'])


class ImageTranslator:
    """Handles requests to the Google Cloud Vision and Translate APIs
    """

    __vision_client = vision.ImageAnnotatorClient()
    __translate_client = translate.Client()
    __language_codes = {'Kannada': 'kn','Hindi':'hi','Tamil':'ta','Telugu':'te','Korean':'ko'}
    __mode_types  = {'Word Detection':True,'Sentence Detection':False}

    def __init__(self, target_language='Kannada',target_mode='Word Detection') -> None:
        self.__target_language = ImageTranslator.__language_codes[target_language]
        self.__target_mode = ImageTranslator.__mode_types[target_mode]

    def set_target_mode(self, target_mode: str) -> None:
        """Set the target language for translation requests sent to Google's Cloud Translate API
        """

        self.__target_mode = ImageTranslator.__mode_types[target_mode]

    def set_target_language(self, target_language: str) -> None:
        """Set the target language for translation requests sent to Google's Cloud Translate API
        """

        self.__target_language = ImageTranslator.__language_codes[target_language]

    def translate_image_text(self, image_data: bytes) -> list:
        """Detect and translate each word in the image, and construct a list of WordBox namedtuples.
        """
        image = types.Image(content=image_data)
        # Performs label detection on the image file
        response = ImageTranslator.__vision_client.text_detection(image=image)

        texts = response.text_annotations
        
        if len(texts) == 0:
            # sending post request and saving response as response object
            API_ENDPOINT = "http://mile.ee.iisc.ernet.in:8080/tts_demo/rest/"
            data = {'inputText':"ಬರಹ ಲಭ್ಯ ಇಲ್ಲ"}
            r = requests.post(url = API_ENDPOINT, data = data)
            
            # extracting response text 
            datar = r.text.split('"')
            #print(datar)
            wavFile = requests.get(url = "http://mile.ee.iisc.ernet.in:8080/" + datar[1])
            open('audio.wav', 'wb').write(wavFile.content)
            return [],"Text No Found",True

        all_text = texts[0]
        translated_all = ImageTranslator.__translate_client.translate(all_text.description,
                                                                           target_language=self.__target_language)
        print(u'Text: {}'.format(translated_all['input']))
        print(u'Translation: {}'.format(translated_all['translatedText']))
        print(u'Detected source language: {}'.format(translated_all['detectedSourceLanguage']))                                                     
        
        if self.__target_language == "kn":
            # sending post request and saving response as response object
            API_ENDPOINT = "http://mile.ee.iisc.ernet.in:8080/tts_demo/rest/"
            data = {'inputText':translated_all['translatedText']}
            r = requests.post(url = API_ENDPOINT, data = data)
            
            # extracting response text 
            datar = r.text.split('"')
            #print(datar)
            wavFile = requests.get(url = "http://mile.ee.iisc.ernet.in:8080/" + datar[1])
            open('audio.wav', 'wb').write(wavFile.content)
        word_boxes = []
        if self.__target_mode:
            for word_data in texts[1:]:
                translated_word = ImageTranslator.__translate_client.translate(word_data.description,
                                                                            target_language=self.__target_language)
                
                boundary_vertices = word_data.bounding_poly.vertices
                box = []
                for vertex in boundary_vertices:
                    box.append((vertex.x, vertex.y))
                word_boxes.append(WordBox(word=translated_word['translatedText'], geometry=box))
        else:
            boundary_vertices = texts[0].bounding_poly.vertices
            box = []
            for vertex in boundary_vertices:
                box.append((vertex.x, vertex.y))
            word_boxes.append(WordBox(word=translated_all['translatedText'], geometry=box))

        if self.__target_language == "kn":
            return word_boxes,translated_all['translatedText'],True
        else:
            return word_boxes,translated_all['translatedText'],False
